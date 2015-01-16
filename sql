INSERT INTO person(name, fb_id) VALUES("10204949449471253", "Clint Thomas Muriyaickal");


SELECT * FROM movies.person;

SELECT * FROM movies.post;

SELECT * FROM movies.comment;

SELECT * FROM movies.post_description;

SELECT count(*) FROM movies.fb_like;

SELECT * FROM movies.post where message LIKE "%Hachi%";

SELECT fb_id FROM movies.post;

SELECT post.id, post.message, post.language, post_description.movie_id FROM post inner join post_description on post.id = post_description.post_id where post_description.movie_id is NULL and post.message > '';

SELECT post.id, post.message, post.language, post_description.movie_id FROM post inner join post_description on post.id = post_description.post_id where post_description.movie_id is not NULL and post.message > '';