Create View big_invoice As
select invoice_id, customer_id, total
from invoice 
where total>20;

select *from big_invoice
--Drop view viewname

select * from pg_views
where viewname='big_invoices';