-- Join users with their posts and show posts from users age 20 or older
SELECT
    users.name,
    users.age,
    posts.content,
    posts.created_at
FROM users
JOIN posts ON users.user_id = posts.user_id
WHERE users.age >= 20;