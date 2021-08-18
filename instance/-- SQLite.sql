-- SQLite
SELECT id, author_id, created, cloudname, description, image
FROM cloud;

SELECT cloudname, created
FROM cloud
INNER JOIN user on user.id = cloud.author_id
WHERE user.id = 1
ORDER by created ASC;