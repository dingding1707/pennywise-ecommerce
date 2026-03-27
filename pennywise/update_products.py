"""
update_products.py
──────────────────
A general-purpose script for updating product data in the Pennywise database.
Run with a command flag to perform different operations.

Usage:
  python update_products.py --list                     List all products
  python update_products.py --update-price 1 19.99     Update price of product ID 1
  python update_products.py --update-stock 1 50        Set stock of product ID 1 to 50
  python update_products.py --update-name 1 "New Name" Rename product ID 1
  python update_products.py --add-sale 1 29.99         Set original_price (shows sale tag)
  python update_products.py --remove-sale 1            Remove sale price from product ID 1
  python update_products.py --set-bestseller 1 1       Mark product ID 1 as bestseller (0 to unmark)
  python update_products.py --set-new 1 1              Mark product ID 1 as new arrival
  python update_products.py --bulk-update              Apply all edits in BULK_UPDATES below
  python update_products.py --clear-reviews            Delete ALL reviews (use with caution)
  python update_products.py --list-reviews             Show all reviews
  python update_products.py --delete-review 3          Delete review with ID 3
  python update_products.py --list-orders              Show all orders
"""

import sqlite3
import os
import argparse
import json

DB_PATH = os.path.join(os.path.dirname(__file__), 'pennywise.db')


def get_conn():
    if not os.path.exists(DB_PATH):
        print("ERROR: pennywise.db not found.")
        print("Run 'python app.py' first to create the database.")
        raise SystemExit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ─────────────────────────────────────────────────────────────────────────────
# BULK_UPDATES — edit this dict to update multiple fields at once.
# Format: { product_id: { field: value, ... }, ... }
#
# Available fields: name, description, price, original_price, brand,
#                   size, stock, is_bestseller, is_new, is_value_set,
#                   is_mini, image_url
# ─────────────────────────────────────────────────────────────────────────────
BULK_UPDATES = {
    # Example:
    # 1: {'price': 22.99, 'original_price': 29.99, 'is_bestseller': 1},
    # 5: {'price': 34.99, 'image_url': 'https://images.unsplash.com/photo-XXX?w=400&h=400&fit=crop'},
}


def list_products(conn=None):
    close = conn is None
    if conn is None:
        conn = get_conn()
    rows = conn.execute(
        'SELECT id, name, brand, price, original_price, stock, is_bestseller, is_new FROM products ORDER BY category, id'
    ).fetchall()
    if close:
        conn.close()
    print(f"\n{'ID':<4}  {'Brand':<16}  {'Name':<35}  {'Price':>8}  {'Was':>8}  {'Stock':>5}  {'Best':>4}  {'New':>3}")
    print("-" * 100)
    for r in rows:
        orig = f"TT${r['original_price']:.2f}" if r['original_price'] else ''
        print(f"{r['id']:<4}  {(r['brand'] or ''):<16}  {r['name']:<35}  TT${r['price']:>6.2f}  {orig:>8}  {r['stock']:>5}  {'Y' if r['is_bestseller'] else '':>4}  {'Y' if r['is_new'] else '':>3}")
    print()


def update_price(pid, new_price):
    conn = get_conn()
    r = conn.execute('UPDATE products SET price=? WHERE id=?', (float(new_price), pid))
    name = conn.execute('SELECT name FROM products WHERE id=?', (pid,)).fetchone()
    conn.commit(); conn.close()
    if r.rowcount:
        print(f"Updated price of '{name['name']}' (ID {pid}) to TT${float(new_price):.2f}")
    else:
        print(f"No product found with ID {pid}")


def update_stock(pid, qty):
    conn = get_conn()
    r = conn.execute('UPDATE products SET stock=? WHERE id=?', (int(qty), pid))
    name = conn.execute('SELECT name FROM products WHERE id=?', (pid,)).fetchone()
    conn.commit(); conn.close()
    if r.rowcount:
        print(f"Updated stock of '{name['name']}' (ID {pid}) to {qty}")
    else:
        print(f"No product found with ID {pid}")


def update_name(pid, new_name):
    conn = get_conn()
    old = conn.execute('SELECT name FROM products WHERE id=?', (pid,)).fetchone()
    r = conn.execute('UPDATE products SET name=? WHERE id=?', (new_name, pid))
    conn.commit(); conn.close()
    if r.rowcount:
        print(f"Renamed product ID {pid}: '{old['name']}' -> '{new_name}'")
    else:
        print(f"No product found with ID {pid}")


def add_sale(pid, original_price):
    conn = get_conn()
    r = conn.execute('UPDATE products SET original_price=? WHERE id=?', (float(original_price), pid))
    name = conn.execute('SELECT name, price FROM products WHERE id=?', (pid,)).fetchone()
    conn.commit(); conn.close()
    if r.rowcount:
        saving = float(original_price) - name['price']
        print(f"Set sale on '{name['name']}' (ID {pid}): was TT${float(original_price):.2f}, now TT${name['price']:.2f} (saves TT${saving:.2f})")
    else:
        print(f"No product found with ID {pid}")


def remove_sale(pid):
    conn = get_conn()
    name = conn.execute('SELECT name FROM products WHERE id=?', (pid,)).fetchone()
    r = conn.execute('UPDATE products SET original_price=NULL WHERE id=?', (pid,))
    conn.commit(); conn.close()
    if r.rowcount and name:
        print(f"Removed sale price from '{name['name']}' (ID {pid})")
    else:
        print(f"No product found with ID {pid}")


def set_flag(pid, field, val):
    if field not in ('is_bestseller', 'is_new', 'is_value_set', 'is_mini'):
        print(f"Invalid flag: {field}")
        return
    conn = get_conn()
    r = conn.execute(f'UPDATE products SET {field}=? WHERE id=?', (int(val), pid))
    name = conn.execute('SELECT name FROM products WHERE id=?', (pid,)).fetchone()
    conn.commit(); conn.close()
    if r.rowcount:
        state = "enabled" if int(val) else "disabled"
        print(f"{field} {state} for '{name['name']}' (ID {pid})")
    else:
        print(f"No product found with ID {pid}")


def apply_bulk():
    if not BULK_UPDATES:
        print("BULK_UPDATES is empty. Add entries to this dict in the script.")
        return
    conn = get_conn()
    total = 0
    allowed = {'name','description','price','original_price','brand','size',
               'stock','is_bestseller','is_new','is_value_set','is_mini','image_url'}
    for pid, fields in BULK_UPDATES.items():
        bad = set(fields) - allowed
        if bad:
            print(f"  WARNING: Skipping unknown fields for ID {pid}: {bad}")
            fields = {k:v for k,v in fields.items() if k in allowed}
        if not fields:
            continue
        set_clause = ', '.join(f'{k}=?' for k in fields)
        vals = list(fields.values()) + [pid]
        r = conn.execute(f'UPDATE products SET {set_clause} WHERE id=?', vals)
        name = conn.execute('SELECT name FROM products WHERE id=?', (pid,)).fetchone()
        if r.rowcount:
            print(f"  Updated ID {pid} ({name['name'] if name else '?'}): {list(fields.keys())}")
            total += 1
        else:
            print(f"  WARNING: No product found with ID {pid}")
    conn.commit(); conn.close()
    print(f"\nBulk update complete — {total} product(s) updated.")


def list_reviews():
    conn = get_conn()
    rows = conn.execute(
        '''SELECT r.id, r.user_name, r.rating, substr(r.comment,1,50) as snippet,
                  p.name as product_name, r.created_at
           FROM reviews r JOIN products p ON r.product_id=p.id
           ORDER BY r.created_at DESC'''
    ).fetchall()
    conn.close()
    if not rows:
        print("No reviews in the database.")
        return
    print(f"\n{'ID':<4}  {'User':<16}  {'Stars':<5}  {'Product':<30}  {'Comment'}")
    print("-" * 100)
    for r in rows:
        stars = '*' * r['rating']
        print(f"{r['id']:<4}  {r['user_name']:<16}  {stars:<5}  {r['product_name']:<30}  {r['snippet']}")
    print()


def delete_review(review_id):
    conn = get_conn()
    r = conn.execute('DELETE FROM reviews WHERE id=?', (review_id,))
    conn.commit(); conn.close()
    if r.rowcount:
        print(f"Deleted review ID {review_id}")
    else:
        print(f"No review found with ID {review_id}")


def clear_reviews():
    confirm = input("This will delete ALL reviews. Type YES to confirm: ")
    if confirm.strip() == 'YES':
        conn = get_conn()
        count = conn.execute('SELECT COUNT(*) FROM reviews').fetchone()[0]
        conn.execute('DELETE FROM reviews')
        conn.execute('UPDATE products SET rating=4.0, review_count=0')
        conn.commit(); conn.close()
        print(f"Deleted {count} review(s) and reset all product ratings.")
    else:
        print("Cancelled.")


def list_orders():
    conn = get_conn()
    rows = conn.execute(
        'SELECT id, first_name, last_name, total, payment_method, status, created_at FROM orders ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    if not rows:
        print("No orders yet.")
        return
    print(f"\n{'ID':<6}  {'Customer':<22}  {'Total':>10}  {'Payment':<20}  {'Status':<12}  Date")
    print("-" * 90)
    for r in rows:
        name = f"{r['first_name']} {r['last_name']}"
        method = r['payment_method'].replace('_', ' ').title()
        print(f"#PW{r['id']:05d}  {name:<22}  TT${r['total']:>8.2f}  {method:<20}  {r['status']:<12}  {r['created_at'][:10]}")
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage the Pennywise Cosmetics database.')
    parser.add_argument('--list',            action='store_true',  help='List all products')
    parser.add_argument('--update-price',    nargs=2, metavar=('ID','PRICE'), help='Update product price')
    parser.add_argument('--update-stock',    nargs=2, metavar=('ID','QTY'),   help='Update product stock')
    parser.add_argument('--update-name',     nargs=2, metavar=('ID','NAME'),  help='Rename a product')
    parser.add_argument('--add-sale',        nargs=2, metavar=('ID','WAS'),   help='Set original (was) price')
    parser.add_argument('--remove-sale',     nargs=1, metavar='ID',           help='Remove sale price')
    parser.add_argument('--set-bestseller',  nargs=2, metavar=('ID','0/1'),   help='Set bestseller flag')
    parser.add_argument('--set-new',         nargs=2, metavar=('ID','0/1'),   help='Set new arrival flag')
    parser.add_argument('--bulk-update',     action='store_true',  help='Apply BULK_UPDATES dict')
    parser.add_argument('--list-reviews',    action='store_true',  help='List all reviews')
    parser.add_argument('--delete-review',   nargs=1, metavar='ID',           help='Delete a review by ID')
    parser.add_argument('--clear-reviews',   action='store_true',  help='Delete ALL reviews')
    parser.add_argument('--list-orders',     action='store_true',  help='List all orders')

    args = parser.parse_args()

    if args.list:             list_products()
    elif args.update_price:   update_price(int(args.update_price[0]), args.update_price[1])
    elif args.update_stock:   update_stock(int(args.update_stock[0]), args.update_stock[1])
    elif args.update_name:    update_name(int(args.update_name[0]), args.update_name[1])
    elif args.add_sale:       add_sale(int(args.add_sale[0]), args.add_sale[1])
    elif args.remove_sale:    remove_sale(int(args.remove_sale[0]))
    elif args.set_bestseller: set_flag(int(args.set_bestseller[0]), 'is_bestseller', args.set_bestseller[1])
    elif args.set_new:        set_flag(int(args.set_new[0]), 'is_new', args.set_new[1])
    elif args.bulk_update:    apply_bulk()
    elif args.list_reviews:   list_reviews()
    elif args.delete_review:  delete_review(int(args.delete_review[0]))
    elif args.clear_reviews:  clear_reviews()
    elif args.list_orders:    list_orders()
    else:                     parser.print_help()
