import os
import logging

import pandas as pd
import mysql.connector


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


DBHOST = os.getenv("DBHOST")
DBNAME = os.getenv("DBNAME")
DBUSER = os.getenv("DBUSER")
DBPASS = os.getenv("DBPASS")


def read_data(filename):
    """Read a CSV file and return it as a pandas DataFrame."""
    logging.info("Reading data from %s", filename)
    data = pd.read_csv(filename)
    logging.info("Data loaded successfully")
    return data


def clean_data(data):
    """Remove rows with missing values and return the cleaned DataFrame."""
    logging.info("Cleaning data")
    cleaned_data = data.dropna()
    logging.info(
        "Data cleaned successfully: %d rows remain",
        len(cleaned_data)
    )
    return cleaned_data


def load_data(data, table):
    """Create the destination table and load cleaned data into MySQL."""
    logging.info("Connecting to MySQL")

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

        # Create the mock table if it does not already exist.
        create_table_query = """
        CREATE TABLE IF NOT EXISTS mock (
            id BIGINT PRIMARY KEY,
            `group` VARCHAR(255),
            first_name VARCHAR(255),
            email VARCHAR(255),
            age BIGINT,
            city VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)

        # Use placeholders instead of inserting values into the SQL string.
        insert_query = """
        INSERT INTO mock (id, `group`, first_name, email, age, city)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        for _, row in data.iterrows():
            values = (
                int(row["id"]),
                row["group"],
                row["first_name"],
                row["email"],
                int(row["age"]),
                row["city"],
            )
            cursor.execute(insert_query, values)

        connection.commit()
        logging.info(
            "Successfully loaded %d rows into %s",
            len(data),
            table
        )

    except mysql.connector.Error as error:
        logging.error("Database error: %s", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

        logging.info("Database connection closed")


def main():
    """Read, clean, and load the mock data into MySQL."""
    logging.info("Starting data processing")

    data = read_data("MOCK_DATA.csv")
    cleaned_data = clean_data(data)
    load_data(cleaned_data, "mock")

    logging.info("Data processing complete")


if __name__ == "__main__":
    main()