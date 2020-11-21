INSERT INTO book(
	title,
	author,
	--publication_year,
	isbn,
	visible,
	user_id)
VALUES (
	'Clean Code: A Handbook of Agile Software Craftsmanship',
	'Robert Martin',
	-- 1970
	'978-0132350884',
	1,
	1);



--
-- users...
--
INSERT INTO users (
	username,
	password)
VALUES(
	'paavo',
	'paavi123');

