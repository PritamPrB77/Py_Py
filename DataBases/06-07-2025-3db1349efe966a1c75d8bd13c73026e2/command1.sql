select artist_id As id_artist From Album;
--HAVING filter  grouops after Group by
--Where Filter rows Before Group By
Select artist_id,count(album_id)
from album
where artist_id<100
Group by artist_id
Having count(album_id)>5;
