"""
update_images.py
────────────────
Run this script to update product image URLs in the database.
Usage: python update_images.py

Steps:
  1. Run the app once first so pennywise.db is created (python app.py).
  2. Find replacement image URLs from unsplash.com or pexels.com.
  3. Add/edit rows in the UPDATES list below.
  4. Run: python update_images.py

To find a product's current ID and image, run:
  python update_images.py --list
"""

import sqlite3
import os
import argparse

DB_PATH = os.path.join(os.path.dirname(__file__), 'pennywise.db')


def get_conn():
    if not os.path.exists(DB_PATH):
        print("ERROR: pennywise.db not found.")
        print("Run 'python app.py' first to create and seed the database, then re-run this script.")
        raise SystemExit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def list_products():
    """Print all products with their current image URLs."""
    conn = get_conn()
    rows = conn.execute('SELECT id, name, brand, image_url FROM products ORDER BY id').fetchall()
    conn.close()
    print(f"\n{'ID':<4}  {'Brand':<20}  {'Name':<38}  {'Current Image URL'}")
    print("-" * 110)
    for r in rows:
        url = (r['image_url'] or 'NO IMAGE')[:55]
        print(f"{r['id']:<4}  {(r['brand'] or ''):<20}  {r['name']:<38}  {url}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# EDIT THIS LIST to update images.
# Format: (product_id, new_image_url)
#
# Tips for finding good URLs:
#   • Go to unsplash.com, find the image, right-click → Copy image address
#   • Append  ?w=400&h=400&fit=crop&q=80  for consistent square crops
#   • Or use pexels.com → right-click the photo → Open in new tab → copy URL
# ─────────────────────────────────────────────────────────────────────────────
UPDATES = [
   ('https://images.unsplash.com/photo-1616592079624-575de673daff?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 1), 
    ('https://images.unsplash.com/photo-1773372238324-e9cffa5f45b7?q=80&w=396&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 2),  
    ('https://images.unsplash.com/photo-1557205465-f3762edea6d3?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 3),  
    ('https://images.unsplash.com/photo-1631214540553-ff044a3ff1d4?q=80&w=774&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 4), 
    ('https://images.unsplash.com/photo-1768983224486-b4dcd179b4a5?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 5),  
    ('https://images.unsplash.com/photo-1631214499500-2e34edcaccfe?q=80&w=415&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 6),  
    ('https://images.unsplash.com/photo-1547887538-e3a2f32cb1cc?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 7),  
    ('https://images.unsplash.com/photo-1704621354783-15f5741ff4de?q=80&w=1374&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 8), 
    ('https://images.unsplash.com/photo-1515688594390-b649af70d282?q=80&w=806&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 9),  
    ('https://images.unsplash.com/photo-1752245818739-890854ca3b81?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 10),  
    ('https://images.unsplash.com/photo-1583334529937-bc4761d2cdad?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8bW9pc3RlcmlzZXJ8ZW58MHx8MHx8fDA%3D', 11),  
    ('https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Y2xlYW5zZXJ8ZW58MHx8MHx8fDA%3D', 12),  
    ('https://images.unsplash.com/photo-1679394270597-e90694d70350?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8c2VydW18ZW58MHx8MHx8fDA%3D', 13),  
    ('https://images.unsplash.com/photo-1616986953793-2e6159b78580?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dG9uZXJ8ZW58MHx8MHx8fDA%3D', 14),  # Shampoo
    ('https://images.unsplash.com/photo-1582020738577-2e7a48043902?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTh8fG5pZ2h0JTIwY3JlYW18ZW58MHx8MHx8fDA%3D', 15),  # Perfume
    ('https://images.unsplash.com/photo-1594332322527-08753d4473c1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8c3Vuc2NyZWVuJTIwbG90aW9ufGVufDB8fDB8fHww', 16),  # Eyeliner
    ('https://images.unsplash.com/photo-1606874576257-5400d9711ce1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8ZmFjZSUyMHNjcnVifGVufDB8fDB8fHww', 17),  # Lipstick
    ('https://images.unsplash.com/photo-1743926959711-73960c2a7b4e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8aHlhbHVyb25pYyUyMGFjaWQlMjBtaXN0fGVufDB8fDB8fHww', 18),  # Moisturizer
    ('https://images.unsplash.com/photo-1700709678003-01941f72fb92?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHNoYW1wb298ZW58MHx8MHx8fDA%3D', 19),  # Shampoo
    ('https://images.unsplash.com/photo-1730115656817-92eb256f2c01?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 20),  # Perfume
    ('https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8aGFpciUyMG1hc2t8ZW58MHx8MHx8fDA%3D', 21),  # Eyeliner
    ('https://images.unsplash.com/photo-1701977501667-20c0e38f5a9d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8aGFpciUyMHByb3RlY3Rpb24lMjBzcHJheXxlbnwwfHwwfHx8MA%3D%3D', 22),  # Lipstick
    ('https://images.unsplash.com/photo-1515377905703-c4788e51af15?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aGFpciUyMG9pbHxlbnwwfHwwfHx8MA%3D%3D', 23),  # Moisturizer
    ('https://images.unsplash.com/photo-1770801153497-959241fce3ae?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aGFpcmNhcmUlMjBraXR8ZW58MHx8MHx8fDA%3D', 24),  # Shampoo
    ('https://images.unsplash.com/photo-1541643600914-78b084683601?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cGVyZnVtZXxlbnwwfHwwfHx8MA%3D%3D', 25),  # Perfume
    ('https://images.unsplash.com/photo-1623085080484-623ff2873922?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8Y2l0cnVzJTIwcGVyZnVtZXxlbnwwfHwwfHx8MA%3D%3D', 26),  # Eyeliner
    ('https://images.unsplash.com/photo-1693734464091-09942cdb6ca0?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZWF1JTIwZGUlMjBwYXJmdW18ZW58MHx8MHx8fDA%3D', 27),  # Lipstick
    ('https://images.unsplash.com/photo-1671642605304-2a0a812b5529?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Ym9keSUyMG1pc3R8ZW58MHx8MHx8fDA%3D', 28),  # Moisturizer
    ('https://images.unsplash.com/photo-1636833777376-4487142e8e17?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cGVyZnVtZSUyMHNldHxlbnwwfHwwfHx8MA%3D%3D', 29),  # Shampoo
    ('https://images.unsplash.com/photo-1703174323653-0455deaf7f11?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8c2hlYSUyMGJ1dHRlciUyMGJvZHklMjBsb3Rpb258ZW58MHx8MHx8fDA%3D', 30),  # Perfume
    ('https://images.unsplash.com/photo-1669212408959-fdde3b2ed6a2?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Ym9keSUyMHdhc2h8ZW58MHx8MHx8fDA%3D', 31),  # Eyeliner
    ('https://images.unsplash.com/photo-1683944433023-027a3f443ae4?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Ym9keSUyMHNjcnVifGVufDB8fDB8fHww', 32),  # Lipstick
    ('https://images.unsplash.com/photo-1621483942660-48b49739ac3b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YmF0aCUyMGJvbWIlMjBzZXR8ZW58MHx8MHx8fDA%3D', 33),  # Moisturizer
    ('https://images.unsplash.com/photo-1601065732058-029db52c86b4?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aGFuZCUyMGNyZWFtfGVufDB8fDB8fHww', 34),  # Shampoo
    ('https://images.unsplash.com/photo-1627495395570-d2c94e3319f5?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bGlxdWlkJTIwc29hcHxlbnwwfHwwfHx8MA%3D%3D', 35),  # Perfume
    ('https://images.unsplash.com/photo-1637524725461-bff1afdb946e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8Ym9keSUyMG9pbHxlbnwwfHwwfHx8MA%3D%3D', 36),  # Eyeliner
]


def apply_updates():
    if not UPDATES:
        print("No updates defined. Add (product_id, url) rows to the UPDATES list in this file.")
        return

    conn = get_conn()
    updated = 0
    for pid, url in UPDATES:
        result = conn.execute('UPDATE products SET image_url=? WHERE id=?', (url, pid))
        if result.rowcount:
            name = conn.execute('SELECT name FROM products WHERE id=?', (pid,)).fetchone()
            print(f"  Updated ID {pid}: {name['name'] if name else 'unknown'}")
            updated += 1
        else:
            print(f"  WARNING: No product found with ID {pid}")
    conn.commit()
    conn.close()
    print(f"\nDone — {updated} product(s) updated.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update product image URLs in the Pennywise database.')
    parser.add_argument('--list', action='store_true', help='List all products and their current image URLs')
    args = parser.parse_args()

    if args.list:
        list_products()
    else:
        apply_updates()
