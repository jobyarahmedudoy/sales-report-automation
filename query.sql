select 
  sale_id,
  sale_date,
  customer_name,
  product_name,
  quantity,
  unit_price,
  total_amount
from public.sales
where sale_date = current_date;
