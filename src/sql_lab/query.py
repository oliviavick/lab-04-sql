import os
import logging

import mysql.connector


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


DBHOST = os.getenv("DBHOST")
DBNAME = os.getenv("DBNAME")
DBUSER = os.getenv("DBUSER")
DBPASS = os.getenv("DBPASS")


def get_data_by_group(value):
    """Return all rows where the group column equals the given value."""
    logging.info("Getting rows for group: %s", value)

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=DBHOST,
            database=DBNAME,
            user=DBUSER,
            password=DBPASS,
        )
        cursor = connection.cursor()

        # Use a parameterized query to safely filter by group.
        query = """
        SELECT id, `group`, first_name, email, age, city
        FROM mock
        WHERE `group` = %s
        """

        cursor.execute(query, (value,))
        results = cursor.fetchall()

        logging.info("Found %d matching rows", len(results))
        return results

    except mysql.connector.Error as error:
        logging.error("Database error: %s", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

        logging.info("Database connection closed")


def plot_counts(groupby):
    """Count rows for each distinct value of the specified column."""
    logging.info("Counting rows grouped by %s", groupby)

    # Only allow known column names in the GROUP BY query.
    allowed_columns = {
        "group": "`group`",
        "first_name": "first_name",
        "email": "email",
        "age": "age",
        "city": "city",
    }

    if groupby not in allowed_columns:
        raise ValueError("Invalid column name")

    column = allowed_columns[groupby]

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=DBHOST,
            database=DBNAME,
            user=DBUSER,
            password=DBPASS,
        )
        cursor = connection.cursor()

        # Column names cannot use %s placeholders, so use the validated name.
        query = (
            f"SELECT {column}, COUNT(*) "
            f"FROM mock GROUP BY {column} "
            f"ORDER BY COUNT(*) DESC"
        )

        cursor.execute(query)
        results = cursor.fetchall()

        logging.info("Count query completed successfully")
        return results

    except mysql.connector.Error as error:
        logging.error("Database error: %s", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

        logging.info("Database connection closed")


def main():
    """Run example queries against the mock table."""
    group_results = get_data_by_group("Finance")

    print("\nRows in the Finance group:")
    for row in group_results:
        print(row)

    count_results = plot_counts("group")

    print("\nCounts by group:")
    for row in count_results:
        print(row)


if __name__ == "__main__":
    main()