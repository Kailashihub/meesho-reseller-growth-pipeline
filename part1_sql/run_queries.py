import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "meesho_reseller.db"
OUT = ROOT / "part1_sql" / "output"
OUT.mkdir(parents=True, exist_ok=True)

def write_csv(name, headers, rows):
    path = OUT / name
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)
    return path

conn = sqlite3.connect(DB)
cur = conn.cursor()

# 1
rows = cur.execute("""
SELECT month, category, ROUND(SUM(quantity * unit_price), 2) AS revenue, COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END, category
""").fetchall()
write_csv("monthly_category_revenue.csv", ["month","category","revenue","n_orders"], rows)

# 2
rows = cur.execute("""
SELECT r.region, ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue, COUNT(*) AS n_orders
FROM orders o JOIN resellers r ON r.reseller_id=o.reseller_id
GROUP BY r.region ORDER BY r.region
""").fetchall()
write_csv("region_revenue.csv", ["region","revenue","n_orders"], rows)

# 3
rows = cur.execute("""
SELECT o.reseller_id, r.reseller_name, ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o JOIN resellers r ON r.reseller_id=o.reseller_id
GROUP BY o.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC LIMIT 5
""").fetchall()
write_csv("top_resellers.csv", ["reseller_id","reseller_name","total_spend"], rows)

# 4a
rows = cur.execute("""
SELECT r.reseller_id, r.reseller_name, r.region, r.city
FROM resellers r LEFT JOIN orders o ON o.reseller_id=r.reseller_id
WHERE o.order_id IS NULL ORDER BY r.reseller_id
""").fetchall()
write_csv("zero_order_resellers.csv", ["reseller_id","reseller_name","region","city"], rows)

# 4b
rows = cur.execute("""
SELECT r.reseller_id, COUNT(*) AS left_join_rows, COUNT(o.order_id) AS matched_order_rows
FROM resellers r LEFT JOIN orders o ON o.reseller_id=r.reseller_id
WHERE r.reseller_id IN (
    SELECT r2.reseller_id FROM resellers r2
    LEFT JOIN orders o2 ON o2.reseller_id=r2.reseller_id
    WHERE o2.order_id IS NULL
)
GROUP BY r.reseller_id
""").fetchall()
write_csv("zero_order_count_diagnostic.csv", ["reseller_id","left_join_rows","matched_order_rows"], rows)

# 5
row = cur.execute("""
SELECT ROUND(SUM(quantity * unit_price) / COUNT(*), 2)
FROM orders WHERE month='June' AND status='Delivered'
""").fetchone()
write_csv("june_delivered_aov.csv", ["june_delivered_aov"], [row])

conn.close()
print("Part 1 outputs written to part1_sql/output/")
