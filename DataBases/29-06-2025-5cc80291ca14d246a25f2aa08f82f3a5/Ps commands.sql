select * from album
SELECT title FROM album
select * from album where artist_id=2
select * from album where title like 'L%'
select * from album where title like '%L'
select * from album where title like '%L%'
--Unique artist /distinct Artist Id
select distinct artist_id from album
--COUNT It Countd Rows
select count(distinct artist_id)  from album
select count(1) from album
select count(title) from album--for column counting
select distinct artist_id from album order by artist_id ASC
select album_id,artist_id from album order by title ASC;
select distinct artist_id from album order by title ASC
select  artist_id from album order by title ASC


select artist_id,count(*) 
from album 
group by  artist_id 
order by artist_id;