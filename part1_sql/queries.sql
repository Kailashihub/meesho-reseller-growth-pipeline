SELECT month,
       category,
       ROUND(SUM(quantity * unit_price), 2) AS revenue,
       COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END,
         category;

-- 2. Region-wise total revenue and order count
SELECT r.region,
       ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
       COUNT(*) AS n_orders
FROM orders AS o
JOIN resellers AS r ON r.reseller_id = o.reseller_id
GROUP BY r.region
ORDER BY r.region;

-- 3. Top resellers by total spend
SELECT o.reseller_id,
       r.reseller_name,
       ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders AS o
JOIN resellers AS r ON r.reseller_id = o.reseller_id
GROUP BY o.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

-- 4a. Resellers with no orders
SELECT r.reseller_id,
       r.reseller_name,
       r.region,
       r.city
FROM resellers AS r
LEFT JOIN orders AS o ON o.reseller_id = r.reseller_id
WHERE o.order_id IS NULL
ORDER BY r.reseller_id;

-- 4b. COUNT(*) vs COUNT(order_id) diagnostic for the zero-order reseller
SELECT r.reseller_id,
       COUNT(*) AS left_join_rows,
       COUNT(o.order_id) AS matched_order_rows
FROM resellers AS r
LEFT JOIN orders AS o ON o.reseller_id = r.reseller_id
WHERE r.reseller_id IN (
    SELECT r2.reseller_id
    FROM resellers AS r2
    LEFT JOIN orders AS o2 ON o2.reseller_id = r2.reseller_id
    WHERE o2.order_id IS NULL
)
GROUP BY r.reseller_id;

-- 5. June Delivered AOV
SELECT ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
