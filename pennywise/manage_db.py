"""
manage_db.py — Pennywise Cosmetics Database Management Utility
Run from inside the pennywise/ folder: python manage_db.py
"""

import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), 'pennywise.db')


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ─── View All Products ────────────────────────────────────────────────────────

def list_products():
    conn = get_conn()
    rows = conn.execute('SELECT id, name, category, image_url FROM products ORDER BY id').fetchall()
    conn.close()
    print(f"\n{'ID':<4} {'Name':<38} {'Category':<14} {'Image URL'}")
    print("-" * 110)
    for r in rows:
        url = r['image_url'] or 'NO IMAGE'
        url_display = url[:55] + '...' if len(url) > 55 else url
        print(f"{r['id']:<4} {r['name']:<38} {r['category']:<14} {url_display}")
    print()


# ─── Update Single Product Image ─────────────────────────────────────────────

def update_image(product_id, new_url):
    conn = get_conn()
    product = conn.execute('SELECT name FROM products WHERE id=?', (product_id,)).fetchone()
    if not product:
        print(f"No product found with ID {product_id}")
        conn.close()
        return
    conn.execute('UPDATE products SET image_url=? WHERE id=?', (new_url, product_id))
    conn.commit()
    conn.close()
    print(f"Updated product {product_id} ({product['name']}) image URL.")


# ─── Bulk Update Images from JSON ────────────────────────────────────────────

def bulk_update_images(json_file):
    """
    JSON format: [ {"id": 1, "url": "https://..."}, ... ]
    """
    if not os.path.exists(json_file):
        print(f"File not found: {json_file}")
        return
    with open(json_file) as f:
        updates = json.load(f)
    conn = get_conn()
    updated = 0
    for item in updates:
        pid = item.get('id')
        url = item.get('url')
        if pid and url:
            conn.execute('UPDATE products SET image_url=? WHERE id=?', (url, pid))
            updated += 1
    conn.commit()
    conn.close()
    print(f"Bulk updated {updated} product image URLs.")


# ─── Update Product Price ─────────────────────────────────────────────────────

def update_price(product_id, new_price, original_price=None):
    conn = get_conn()
    product = conn.execute('SELECT name FROM products WHERE id=?', (product_id,)).fetchone()
    if not product:
        print(f"No product found with ID {product_id}")
        conn.close()
        return
    conn.execute('UPDATE products SET price=?, original_price=? WHERE id=?',
                 (new_price, original_price, product_id))
    conn.commit()
    conn.close()
    print(f"Updated price for product {product_id} ({product['name']}): TT${new_price:.2f}"
          + (f" (was TT${original_price:.2f})" if original_price else ""))


# ─── Update Product Details ───────────────────────────────────────────────────

def update_product(product_id, **fields):
    """
    Update any product fields. Example:
      update_product(1, name="New Name", description="New desc", brand="New Brand")
    """
    allowed = {'name', 'description', 'price', 'original_price', 'category',
               'subcategory', 'image_url', 'stock', 'brand', 'size',
               'is_bestseller', 'is_new', 'is_value_set', 'is_mini'}
    valid = {k: v for k, v in fields.items() if k in allowed}
    if not valid:
        print("No valid fields to update.")
        return
    conn = get_conn()
    product = conn.execute('SELECT name FROM products WHERE id=?', (product_id,)).fetchone()
    if not product:
        print(f"No product found with ID {product_id}")
        conn.close()
        return
    set_clause = ', '.join(f'{k}=?' for k in valid)
    values = list(valid.values()) + [product_id]
    conn.execute(f'UPDATE products SET {set_clause} WHERE id=?', values)
    conn.commit()
    conn.close()
    print(f"Updated product {product_id} ({product['name']}): {list(valid.keys())}")


# ─── View Orders ─────────────────────────────────────────────────────────────

def list_orders():
    conn = get_conn()
    rows = conn.execute(
        'SELECT id, first_name, last_name, total, payment_method, status, created_at FROM orders ORDER BY id DESC LIMIT 20'
    ).fetchall()
    conn.close()
    print(f"\n{'ID':<6} {'Name':<25} {'Total':<12} {'Payment':<20} {'Status':<12} {'Date'}")
    print("-" * 100)
    for r in rows:
        name = f"{r['first_name']} {r['last_name']}"
        print(f"{r['id']:<6} {name:<25} TT${r['total']:<9.2f} {r['payment_method']:<20} {r['status']:<12} {r['created_at'][:16]}")
    print()


# ─── View Users ───────────────────────────────────────────────────────────────

def list_users():
    conn = get_conn()
    rows = conn.execute('SELECT id, first_name, last_name, email, created_at FROM users ORDER BY id').fetchall()
    conn.close()
    print(f"\n{'ID':<5} {'Name':<25} {'Email':<35} {'Joined'}")
    print("-" * 90)
    for r in rows:
        name = f"{r['first_name']} {r['last_name']}"
        print(f"{r['id']:<5} {name:<25} {r['email']:<35} {r['created_at'][:10]}")
    print()


# ─── Reset Database ───────────────────────────────────────────────────────────

def reset_db():
    confirm = input("WARNING: This will delete all data and re-seed. Type YES to confirm: ")
    if confirm.strip() == 'YES':
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print("Database deleted.")
        # Re-import and re-init
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        import importlib
        import app as app_module
        importlib.reload(app_module)
        app_module.init_db()
        print("Database re-created and seeded successfully.")
    else:
        print("Reset cancelled.")


# ─── Add New Product ─────────────────────────────────────────────────────────

def add_product(name, price, category, brand, description='', image_url='',
                original_price=None, subcategory='', size='',
                is_bestseller=0, is_new=0):
    conn = get_conn()
    conn.execute('''
        INSERT INTO products (name, description, price, original_price, category, subcategory,
                              image_url, image_emoji, image_color, stock, is_bestseller, is_new,
                              is_value_set, is_mini, rating, review_count, size, brand)
        VALUES (?,?,?,?,?,?,?,NULL,NULL,100,?,?,0,0,0.0,0,?,?)
    ''', (name, description, price, original_price, category, subcategory,
          image_url, is_bestseller, is_new, size, brand))
    pid = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.commit()
    conn.close()
    print(f"Added product ID {pid}: {name}")


# ─── Delete Product ───────────────────────────────────────────────────────────

def delete_product(product_id):
    conn = get_conn()
    product = conn.execute('SELECT name FROM products WHERE id=?', (product_id,)).fetchone()
    if not product:
        print(f"No product found with ID {product_id}")
        conn.close()
        return
    confirm = input(f"Delete '{product['name']}'? Type YES to confirm: ")
    if confirm.strip() == 'YES':
        conn.execute('DELETE FROM products WHERE id=?', (product_id,))
        conn.commit()
        print(f"Deleted product {product_id}.")
    else:
        print("Cancelled.")
    conn.close()


# ─── CLI Menu ─────────────────────────────────────────────────────────────────

def menu():
    while True:
        print("\n" + "="*50)
        print("  Pennywise Cosmetics — Database Manager")
        print("="*50)
        print("  1. List all products (with image URLs)")
        print("  2. Update a product image URL")
        print("  3. Bulk update images from JSON file")
        print("  4. Update product price")
        print("  5. List recent orders")
        print("  6. List registered users")
        print("  7. Add a new product")
        print("  8. Delete a product")
        print("  9. Reset & reseed database")
        print("  0. Exit")
        print()
        choice = input("Choose an option: ").strip()

        if choice == '1':
            list_products()
        elif choice == '2':
            pid = int(input("Product ID: "))
            url = input("New image URL: ").strip()
            update_image(pid, url)
        elif choice == '3':
            jf = input("Path to JSON file (e.g. image_updates.json): ").strip()
            bulk_update_images(jf)
        elif choice == '4':
            pid = int(input("Product ID: "))
            price = float(input("New price (TT$): "))
            orig = input("Original/was price (leave blank if none): ").strip()
            update_price(pid, price, float(orig) if orig else None)
        elif choice == '5':
            list_orders()
        elif choice == '6':
            list_users()
        elif choice == '7':
            name = input("Product name: ").strip()
            price = float(input("Price (TT$): "))
            category = input("Category (Cosmetics/Skincare/Hair/Perfumes/Bath & Body): ").strip()
            brand = input("Brand: ").strip()
            desc = input("Description: ").strip()
            image_url = input("Image URL: ").strip()
            add_product(name, price, category, brand, desc, image_url)
        elif choice == '8':
            pid = int(input("Product ID to delete: "))
            delete_product(pid)
        elif choice == '9':
            reset_db()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        print("Start the app first with: python app.py")
    else:
        menu()
