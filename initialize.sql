-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    age INT
);

-- Create the posts table
CREATE TABLE IF NOT EXISTS posts (
    post_id INT PRIMARY KEY,
    user_id INT,
    content TEXT,
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Insert 10 users
INSERT INTO users (user_id, name, email, age) VALUES
(1, 'Emma Johnson', 'emma@example.com', 20),
(2, 'Liam Smith', 'liam@example.com', 21),
(3, 'Sophia Brown', 'sophia@example.com', 19),
(4, 'Noah Davis', 'noah@example.com', 22),
(5, 'Ava Wilson', 'ava@example.com', 20),
(6, 'Ethan Miller', 'ethan@example.com', 21),
(7, 'Mia Taylor', 'mia@example.com', 19),
(8, 'Lucas Anderson', 'lucas@example.com', 22),
(9, 'Isabella Thomas', 'isabella@example.com', 20),
(10, 'James Moore', 'james@example.com', 21);

-- Insert 10 posts
INSERT INTO posts (post_id, user_id, content, created_at) VALUES
(1, 1, 'Studying for my SQL class!', '2026-09-20 10:00:00'),
(2, 2, 'Learning about databases today.', '2026-09-21 11:30:00'),
(3, 3, 'Working on my data science lab.', '2026-09-22 09:15:00'),
(4, 4, 'SQL is starting to make sense.', '2026-09-23 14:20:00'),
(5, 5, 'Enjoying a beautiful day outside.', '2026-09-24 16:45:00'),
(6, 6, 'Finishing up some homework.', '2026-09-25 18:00:00'),
(7, 7, 'Getting ready for class.', '2026-09-26 08:30:00'),
(8, 8, 'Practicing SQL queries.', '2026-09-27 13:10:00'),
(9, 9, 'Learning about JOIN operations.', '2026-09-28 15:25:00'),
(10, 10, 'Almost finished with the lab!', '2026-09-29 19:00:00');