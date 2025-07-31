select artist_id,count(album_id) AS album_count
from album
where artist_id id>100
group by artist_id
having count(album_id)>5;
-- Where - Filter Rows before groups are aggregated
--Having - filter rows after groups are aggregated

--In--In-- let you check if a vlue matches any value in a 
--List Or  Subquery 
select * 
from album
where artist_id IN (1,2,3,4,5)
order by artist_id
---Executing multiple Query Using In

Select *
from album
where artist_id IN(
select artist_id
from artist
where name ilike 'L%'
)order by artist_id


SELECT *
FROM album
WHERE title ILIKE 'L%'
ORDER BY artist_id;