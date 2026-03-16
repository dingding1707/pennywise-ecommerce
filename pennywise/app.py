from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3
import hashlib
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'pennywise_cosmetics_secret_2024'

DB_PATH = os.path.join(os.path.dirname(__file__), 'pennywise.db')

# ─── Database Setup ───────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            original_price REAL,
            category TEXT NOT NULL,
            subcategory TEXT,
            image_url TEXT,
            image_emoji TEXT,
            image_color TEXT,
            stock INTEGER DEFAULT 100,
            is_bestseller INTEGER DEFAULT 0,
            is_new INTEGER DEFAULT 0,
            is_value_set INTEGER DEFAULT 0,
            is_mini INTEGER DEFAULT 0,
            rating REAL DEFAULT 4.0,
            review_count INTEGER DEFAULT 0,
            size TEXT,
            brand TEXT
        );

        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            user_id INTEGER,
            user_name TEXT,
            rating INTEGER,
            comment TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            email TEXT,
            first_name TEXT,
            last_name TEXT,
            address TEXT,
            city TEXT,
            phone TEXT,
            items TEXT,
            subtotal REAL,
            delivery REAL,
            total REAL,
            payment_last4 TEXT,
            status TEXT DEFAULT 'confirmed',
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS favourites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            UNIQUE(user_id, product_id)
        );
    ''')

    # Check if products already seeded
    count = c.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    if count == 0:
        seed_products(c)

    conn.commit()
    conn.close()

def seed_products(c):
    # Real Unsplash image URLs — beauty/cosmetics category
    IMG = {
        'eyeliner':     'https://images.unsplash.com/photo-1631214524020-3c69c4d87bbf?w=400&h=400&fit=crop&q=80',
        'lipstick':     'https://images.unsplash.com/photo-1586495777744-4e6b8c3dc7d8?w=400&h=400&fit=crop&q=80',
        'foundation':   'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop&q=80',
        'mascara':      'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=400&fit=crop&q=80',
        'eyeshadow':    'https://images.unsplash.com/photo-1571781926291-522674b64303?w=400&h=400&fit=crop&q=80',
        'lip_gloss':    'https://images.unsplash.com/photo-1599305445671-ac291c95aaa9?w=400&h=400&fit=crop&q=80',
        'concealer':    'https://images.unsplash.com/photo-1631215305858-f5a3f1a8cb73?w=400&h=400&fit=crop&q=80',
        'powder':       'https://images.unsplash.com/photo-1596704017254-79a5e0c0d4c4?w=400&h=400&fit=crop&q=80',
        'blush':        'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400&h=400&fit=crop&q=80',
        'lip_liner':    'https://images.unsplash.com/photo-1625093830878-748c0f4b3a1d?w=400&h=400&fit=crop&q=80',
        'moisturizer':  'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400&h=400&fit=crop&q=80',
        'cleanser':     'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=400&fit=crop&q=80',
        'serum':        'https://images.unsplash.com/photo-1571875257727-256c39da42af?w=400&h=400&fit=crop&q=80',
        'toner':        'https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400&h=400&fit=crop&q=80',
        'night_cream':  'https://images.unsplash.com/photo-1629732051926-699d041d0b85?w=400&h=400&fit=crop&q=80',
        'sunscreen':    'https://images.unsplash.com/photo-1556228999-ef2ac3b8a2b0?w=400&h=400&fit=crop&q=80',
        'face_scrub':   'https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?w=400&h=400&fit=crop&q=80',
        'facial_mist':  'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop&q=80',
        'shampoo':      'https://images.unsplash.com/photo-1585232351009-aa39e4e96e74?w=400&h=400&fit=crop&q=80',
        'conditioner':  'https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=400&h=400&fit=crop&q=80',
        'hair_mask':    'https://images.unsplash.com/photo-1522337360826-43e96abb4e12?w=400&h=400&fit=crop&q=80',
        'heat_spray':   'https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=400&h=400&fit=crop&q=80',
        'hair_oil':     'https://images.unsplash.com/photo-1604176354204-9268737828e4?w=400&h=400&fit=crop&q=80',
        'hair_kit':     'https://images.unsplash.com/photo-1585232351009-aa39e4e96e74?w=400&h=400&fit=crop&q=80',
        'perfume_floral':'https://images.unsplash.com/photo-1557053910-d9eadeed1c58?w=400&h=400&fit=crop&q=80',
        'perfume_citrus':'https://images.unsplash.com/photo-1588776814546-1ffbb3cd32a0?w=400&h=400&fit=crop&q=80',
        'perfume_oud':  'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=400&h=400&fit=crop&q=80',
        'body_mist':    'https://images.unsplash.com/photo-1563170351-be75ed7b33d0?w=400&h=400&fit=crop&q=80',
        'perfume_set':  'https://images.unsplash.com/photo-1547887538-e3a2f32cb1cc?w=400&h=400&fit=crop&q=80',
        'body_lotion':  'https://images.unsplash.com/photo-1611080626919-7cf5a9dbab12?w=400&h=400&fit=crop&q=80',
        'body_wash':    'https://images.unsplash.com/photo-1556760544-74068565f05c?w=400&h=400&fit=crop&q=80',
        'body_scrub':   'https://images.unsplash.com/photo-1608248097266-8bcac5e85b13?w=400&h=400&fit=crop&q=80',
        'bath_bomb':    'https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=400&h=400&fit=crop&q=80',
        'hand_cream':   'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=400&h=400&fit=crop&q=80',
        'liquid_soap':  'https://images.unsplash.com/photo-1547496502-affa22d38842?w=400&h=400&fit=crop&q=80',
        'body_oil':     'https://images.unsplash.com/photo-1612817288484-6f916006741a?w=400&h=400&fit=crop&q=80',
    }

    products = [
        # ── Cosmetics ──
        ('Precision Eyeliner Pen', 'Long-lasting waterproof formula for precise lines. Smudge-resistant and fade-proof for all-day wear.', 24.99, 29.99, 'Cosmetics', 'Eyes', IMG['eyeliner'], None, '#2D1B4E', 150, 1, 0, 0, 0, 4.8, 324, '0.01 oz', 'L\'Oréal'),
        ('Matte Velvet Lipstick', 'Ultra-pigmented matte lipstick. Stays put for 12 hours without drying out your lips.', 18.99, None, 'Cosmetics', 'Lips', IMG['lipstick'], None, '#C0392B', 200, 1, 0, 0, 0, 4.7, 218, '0.12 oz', 'Maybelline'),
        ('Full Coverage Foundation', 'Buildable coverage foundation with SPF 20. Suitable for all skin types. Lasts 24 hours.', 34.99, 42.00, 'Cosmetics', 'Face', IMG['foundation'], None, '#E8C99A', 120, 1, 0, 0, 0, 4.5, 412, '30ml', 'L\'Oréal'),
        ('Volume Mascara', 'Dramatic volume and length mascara. Clump-free formula, buildable for intense lashes.', 19.99, None, 'Cosmetics', 'Eyes', IMG['mascara'], None, '#1A1A2E', 180, 0, 1, 0, 0, 4.6, 289, '10ml', 'Maybelline'),
        ('18-Shade Eyeshadow Palette', 'Highly pigmented palette with matte, shimmer, and glitter shades perfect for any look.', 39.99, 55.00, 'Cosmetics', 'Eyes', IMG['eyeshadow'], None, '#8E44AD', 80, 0, 0, 1, 0, 4.9, 156, 'Full Size', 'NYX'),
        ('Mini Lip Gloss Set', 'Set of 6 high-shine lip glosses in trending shades. Perfect for on-the-go touch-ups.', 22.99, None, 'Cosmetics', 'Lips', IMG['lip_gloss'], None, '#FF69B4', 95, 0, 0, 0, 1, 4.4, 87, 'Mini Set', 'NYX'),
        ('Concealer Stick', 'Full-coverage concealer that hides dark circles and blemishes. Blendable, long-lasting formula.', 16.99, 20.00, 'Cosmetics', 'Face', IMG['concealer'], None, '#DEB887', 110, 0, 1, 0, 0, 4.3, 198, '8ml', 'Revlon'),
        ('Setting Powder', 'Translucent finishing powder for a flawless matte look. Reduces shine all day.', 14.99, None, 'Cosmetics', 'Face', IMG['powder'], None, '#FAD7A0', 90, 0, 0, 0, 0, 4.2, 145, '10g', 'e.l.f.'),
        ('Blush & Bronzer Duo', 'Two-in-one compact with a natural blush and warm bronzer. Buildable color, silky texture.', 27.99, 35.00, 'Cosmetics', 'Face', IMG['blush'], None, '#E07B54', 75, 1, 0, 1, 0, 4.7, 201, '8g', 'Milani'),
        ('Nude Lip Liner', 'Define and shape your lips with this long-lasting nude liner. Works with any lip color.', 11.99, None, 'Cosmetics', 'Lips', IMG['lip_liner'], None, '#D4A574', 130, 0, 0, 0, 0, 4.1, 112, '1.5g', 'Revlon'),

        # ── Skincare ──
        ('Hydrating Day Moisturizer', 'Lightweight SPF 30 moisturizer with hyaluronic acid. Plumps and protects all day.', 29.99, 38.00, 'Skincare', 'Moisturizers', IMG['moisturizer'], None, '#AED6F1', 160, 1, 0, 0, 0, 4.8, 387, '50ml', 'Neutrogena'),
        ('Gentle Foaming Cleanser', 'Sulfate-free cleanser that removes makeup and impurities without stripping moisture.', 17.99, None, 'Skincare', 'Cleansers', IMG['cleanser'], None, '#D5F5E3', 140, 1, 0, 0, 0, 4.6, 256, '150ml', 'CeraVe'),
        ('Vitamin C Brightening Serum', '20% Vitamin C serum that brightens skin, fades dark spots, and boosts radiance overnight.', 44.99, 60.00, 'Skincare', 'Serums', IMG['serum'], None, '#F9E79F', 70, 0, 1, 0, 0, 4.9, 523, '30ml', 'TruSkin'),
        ('Balancing Toner', 'Alcohol-free toner with niacinamide to minimize pores, balance oil, and prep skin for serums.', 15.99, None, 'Skincare', 'Toners', IMG['toner'], None, '#A9DFBF', 120, 0, 0, 0, 0, 4.4, 178, '200ml', 'Thayers'),
        ('Retinol Night Cream', 'Powerful retinol cream that reduces fine lines and wrinkles overnight. Gentle enough for sensitive skin.', 36.99, 48.00, 'Skincare', 'Moisturizers', IMG['night_cream'], None, '#D7BDE2', 85, 1, 0, 0, 0, 4.7, 304, '50ml', 'RoC'),
        ('SPF 50 Sunscreen Lotion', 'Broad-spectrum UVA/UVB protection. Lightweight, non-greasy formula. Water resistant 80 minutes.', 22.99, None, 'Skincare', 'Sunscreen', IMG['sunscreen'], None, '#FDEBD0', 200, 0, 0, 0, 0, 4.5, 241, '90ml', 'Banana Boat'),
        ('Exfoliating Face Scrub', 'Micro-bead-free scrub with AHA/BHA to remove dead skin cells and unclog pores.', 19.99, 25.00, 'Skincare', 'Cleansers', IMG['face_scrub'], None, '#FAD7A0', 95, 0, 1, 0, 0, 4.3, 167, '75ml', "St. Ives"),
        ('Hyaluronic Acid Mist', 'Hydrating facial mist with hyaluronic acid and rosewater for instant moisture throughout the day.', 18.99, None, 'Skincare', 'Mists & Essence', IMG['facial_mist'], None, '#FADBD8', 110, 0, 0, 0, 0, 4.6, 198, '100ml', 'Mario Badescu'),

        # ── Hair ──
        ('Argan Oil Shampoo', 'Sulfate-free shampoo infused with argan oil. Cleanses, nourishes, and adds shine to all hair types.', 16.99, None, 'Hair', 'Shampoo', IMG['shampoo'], None, '#85C1E9', 170, 1, 0, 0, 0, 4.5, 289, '400ml', 'OGX'),
        ('Deep Repair Conditioner', 'Intense moisture conditioner with shea butter and keratin. Detangles and softens damaged hair.', 17.99, 22.00, 'Hair', 'Conditioner', IMG['conditioner'], None, '#73C6B6', 150, 1, 0, 0, 0, 4.7, 312, '400ml', 'OGX'),
        ('Coconut Hair Mask', 'Weekly deep conditioning mask with coconut oil. Restores elasticity and reduces breakage.', 24.99, 30.00, 'Hair', 'Treatment', IMG['hair_mask'], None, '#F9E79F', 90, 0, 0, 1, 0, 4.8, 187, '300ml', 'SheaMoisture'),
        ('Heat Protection Spray', 'Lightweight spray that protects hair from heat damage up to 450°F. Adds shine and reduces frizz.', 19.99, None, 'Hair', 'Styling', IMG['heat_spray'], None, '#F1948A', 115, 0, 1, 0, 0, 4.4, 154, '250ml', 'TRESemmé'),
        ('Castor Oil Hair Growth Serum', 'Stimulates hair growth and strengthens roots. Reduces thinning and promotes thicker hair.', 28.99, 36.00, 'Hair', 'Treatment', IMG['hair_oil'], None, '#82E0AA', 80, 1, 0, 0, 0, 4.6, 421, '60ml', 'Mielle'),
        ('Mini Haircare Starter Kit', 'Travel-sized shampoo, conditioner, and leave-in cream. Perfect for on-the-go hair care.', 21.99, None, 'Hair', 'Styling', IMG['hair_kit'], None, '#D7BDE2', 70, 0, 0, 0, 1, 4.3, 96, 'Mini Kit', 'OGX'),

        # ── Perfumes ──
        ('Floral Bloom EDP 100ml', 'A feminine fragrance with notes of rose, jasmine, and white musk. Long-lasting, elegant, and refined.', 79.99, 95.00, 'Perfumes', 'Eau de Parfum', IMG['perfume_floral'], None, '#FF85A2', 60, 1, 0, 0, 0, 4.9, 234, '100ml', 'Pennywise Select'),
        ('Fresh Citrus EDT 50ml', 'A vibrant unisex fragrance with bursts of bergamot, lemon, and green tea. Light and refreshing.', 49.99, None, 'Perfumes', 'Eau de Toilette', IMG['perfume_citrus'], None, '#F9E79F', 85, 0, 1, 0, 0, 4.6, 178, '50ml', 'Pennywise Select'),
        ('Oud & Amber Intense', 'A rich, oriental fragrance with oud, amber, and sandalwood. Sophisticated and long-lasting.', 89.99, 110.00, 'Perfumes', 'Eau de Parfum', IMG['perfume_oud'], None, '#8B4513', 45, 1, 0, 0, 0, 4.8, 145, '75ml', 'Pennywise Select'),
        ('Caribbean Breeze Body Mist', 'A light, refreshing body mist with coconut, vanilla, and sea salt. Tropical and carefree.', 19.99, None, 'Perfumes', 'Body Mist', IMG['body_mist'], None, '#85C1E9', 120, 0, 0, 0, 0, 4.4, 201, '250ml', 'Pennywise Select'),
        ('Mini Perfume Discovery Set', 'Five mini perfumes in our bestselling scents. Perfect for travel or discovering your signature scent.', 44.99, 60.00, 'Perfumes', 'Gift Sets', IMG['perfume_set'], None, '#D7BDE2', 55, 0, 0, 1, 1, 4.7, 312, 'Mini Set 5x10ml', 'Pennywise Select'),

        # ── Bath & Body ──
        ('Shea Butter Body Lotion', 'Rich, deeply moisturizing lotion with shea butter and vitamin E. Absorbs quickly for soft, glowing skin.', 15.99, None, 'Bath & Body', 'Body Lotion', IMG['body_lotion'], None, '#FDEBD0', 190, 1, 0, 0, 0, 4.7, 356, '400ml', 'Vaseline'),
        ('Lavender Body Wash', 'Calming lavender body wash that cleanses and soothes skin. Gentle enough for daily use.', 12.99, 16.00, 'Bath & Body', 'Body Wash', IMG['body_wash'], None, '#D7BDE2', 210, 1, 0, 0, 0, 4.5, 298, '500ml', "Aveeno"),
        ('Coffee Sugar Body Scrub', 'Exfoliating scrub with coffee grounds and raw sugar. Removes dead skin, smooths, and energizes.', 22.99, 28.00, 'Bath & Body', 'Body Scrub', IMG['body_scrub'], None, '#8B4513', 100, 0, 1, 0, 0, 4.8, 214, '250g', 'Frank Body'),
        ('Luxe Bath Bomb Set', 'Set of 6 fizzing bath bombs in various scents and colors. Turn your bath into a spa experience.', 28.99, None, 'Bath & Body', 'Bath Treats', IMG['bath_bomb'], None, '#F1948A', 75, 0, 0, 1, 0, 4.9, 187, 'Set of 6', 'Da Bomb'),
        ('Hand Cream Trio', 'Three rich hand creams in rose, vanilla, and coconut scents. Moisturizes and repairs dry hands.', 19.99, 25.00, 'Bath & Body', 'Hand Care', IMG['hand_cream'], None, '#FAD7A0', 88, 0, 0, 1, 0, 4.6, 142, 'Trio 3x75ml', "L'Occitane"),
        ('Antibacterial Liquid Soap', 'Moisturizing antibacterial hand soap with aloe vera. Kills 99.9% of germs while keeping hands soft.', 8.99, None, 'Bath & Body', 'Hand Care', IMG['liquid_soap'], None, '#AED6F1', 250, 0, 0, 0, 0, 4.3, 178, '250ml', 'Dettol'),
        ('Coconut & Lime Body Oil', 'Lightweight, non-greasy body oil with coconut and lime. Adds luminous glow and deep moisture.', 24.99, 32.00, 'Bath & Body', 'Body Oil', IMG['body_oil'], None, '#A9DFBF', 95, 0, 1, 0, 0, 4.7, 165, '150ml', 'Kopari'),
    ]

    c.executemany('''
        INSERT INTO products 
        (name, description, price, original_price, category, subcategory, image_url, image_emoji, image_color,
         stock, is_bestseller, is_new, is_value_set, is_mini, rating, review_count, size, brand)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', products)

    # Seed some reviews
    reviews = [
        (1, None, 'Alicia M.', 5, 'Best eyeliner I\'ve ever used! Stays on all day even in the humidity.'),
        (1, None, 'Priya S.', 5, 'Arrived quickly and exactly as described. Will definitely buy again!'),
        (2, None, 'Keisha R.', 4, 'Beautiful color, stays on for hours. Slightly drying but great for the price.'),
        (11, None, 'Sandra T.', 5, 'My skin has never felt so soft. I use this every morning and love it.'),
        (13, None, 'Maria G.', 5, 'Noticed a difference in my dark spots within two weeks. Worth every penny!'),
        (25, None, 'Renee P.', 5, 'This perfume gets me so many compliments. Smells absolutely divine.'),
        (29, None, 'Tricia F.', 4, 'Great gift set! All five scents are lovely. Perfect for travel.'),
        (30, None, 'Diane W.', 5, 'My skin is so soft and moisturized. Best body lotion I\'ve tried.'),
    ]
    c.executemany('''
        INSERT INTO reviews (product_id, user_id, user_name, rating, comment)
        VALUES (?,?,?,?,?)
    ''', reviews)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def get_cart():
    return session.get('cart', {})

def cart_count():
    cart = get_cart()
    return sum(item['qty'] for item in cart.values())

def cart_subtotal():
    cart = get_cart()
    return sum(item['price'] * item['qty'] for item in cart.values())

def get_favourites():
    if 'user_id' not in session:
        return session.get('fav_ids', [])
    conn = get_db()
    rows = conn.execute('SELECT product_id FROM favourites WHERE user_id=?', (session['user_id'],)).fetchall()
    conn.close()
    return [r['product_id'] for r in rows]

def inject_globals():
    return dict(
        cart_count=cart_count(),
        cart_subtotal=cart_subtotal(),
        current_user=session.get('user_name'),
        user_id=session.get('user_id'),
        fav_ids=get_favourites()
    )

app.context_processor(inject_globals)


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    conn = get_db()
    bestsellers = conn.execute('SELECT * FROM products WHERE is_bestseller=1 LIMIT 8').fetchall()
    new_arrivals = conn.execute('SELECT * FROM products WHERE is_new=1 LIMIT 6').fetchall()
    categories = conn.execute('SELECT DISTINCT category FROM products').fetchall()
    conn.close()
    return render_template('home.html', bestsellers=bestsellers, new_arrivals=new_arrivals, categories=categories)

@app.route('/products')
def products():
    category = request.args.get('category', '')
    subcategory = request.args.get('subcategory', '')
    filter_type = request.args.get('filter', '')
    sort = request.args.get('sort', 'default')
    search = request.args.get('q', '')
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 9999, type=float)

    conn = get_db()
    query = 'SELECT * FROM products WHERE 1=1'
    params = []

    if category:
        query += ' AND category=?'
        params.append(category)
    if subcategory:
        query += ' AND subcategory=?'
        params.append(subcategory)
    if filter_type == 'bestsellers':
        query += ' AND is_bestseller=1'
    elif filter_type == 'new':
        query += ' AND is_new=1'
    elif filter_type == 'value_sets':
        query += ' AND is_value_set=1'
    elif filter_type == 'mini':
        query += ' AND is_mini=1'
    if search:
        query += ' AND (name LIKE ? OR description LIKE ? OR brand LIKE ?)'
        params += [f'%{search}%', f'%{search}%', f'%{search}%']
    query += ' AND price >= ? AND price <= ?'
    params += [min_price, max_price]

    if sort == 'price_asc':
        query += ' ORDER BY price ASC'
    elif sort == 'price_desc':
        query += ' ORDER BY price DESC'
    elif sort == 'rating':
        query += ' ORDER BY rating DESC'
    elif sort == 'name':
        query += ' ORDER BY name ASC'
    else:
        query += ' ORDER BY is_bestseller DESC, rating DESC'

    items = conn.execute(query, params).fetchall()
    all_categories = conn.execute('SELECT DISTINCT category FROM products').fetchall()
    conn.close()
    return render_template('products.html', products=items, selected_category=category,
                           selected_filter=filter_type, sort=sort, search=search,
                           all_categories=all_categories, subcategory=subcategory)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db()
    product = conn.execute('SELECT * FROM products WHERE id=?', (product_id,)).fetchone()
    if not product:
        return redirect(url_for('products'))
    reviews = conn.execute('SELECT * FROM reviews WHERE product_id=? ORDER BY created_at DESC', (product_id,)).fetchall()
    related = conn.execute('SELECT * FROM products WHERE category=? AND id!=? LIMIT 4', (product['category'], product_id)).fetchall()
    conn.close()
    return render_template('product_detail.html', product=product, reviews=reviews, related=related)

# ─── Cart ─────────────────────────────────────────────────────────────────────

@app.route('/cart')
def cart():
    cart = get_cart()
    return render_template('cart.html', cart=cart)

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    pid = str(data.get('product_id'))
    qty = int(data.get('qty', 1))
    conn = get_db()
    product = conn.execute('SELECT * FROM products WHERE id=?', (pid,)).fetchone()
    conn.close()
    if not product:
        return jsonify({'success': False})
    cart = get_cart()
    if pid in cart:
        cart[pid]['qty'] += qty
    else:
        cart[pid] = {
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'emoji': product['image_emoji'],
            'color': product['image_color'],
            'image_url': product['image_url'],
            'qty': qty
        }
    session['cart'] = cart
    session.modified = True
    return jsonify({'success': True, 'count': cart_count(), 'message': f'{product["name"]} added to cart!'})

@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    data = request.get_json()
    pid = str(data.get('product_id'))
    qty = int(data.get('qty', 1))
    cart = get_cart()
    if pid in cart:
        if qty <= 0:
            del cart[pid]
        else:
            cart[pid]['qty'] = qty
    session['cart'] = cart
    session.modified = True
    subtotal = cart_subtotal()
    delivery = 30.00 if subtotal > 0 else 0
    return jsonify({'success': True, 'count': cart_count(), 'subtotal': subtotal, 'total': subtotal + delivery})

@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    pid = str(data.get('product_id'))
    cart = get_cart()
    if pid in cart:
        del cart[pid]
    session['cart'] = cart
    session.modified = True
    subtotal = cart_subtotal()
    delivery = 30.00 if subtotal > 0 else 0
    return jsonify({'success': True, 'count': cart_count(), 'subtotal': subtotal, 'total': subtotal + delivery})

# ─── Checkout ─────────────────────────────────────────────────────────────────

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not get_cart():
        return redirect(url_for('cart'))
    if request.method == 'POST':
        session['checkout_info'] = {
            'email': request.form.get('email'),
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'address': request.form.get('address'),
            'city': request.form.get('city'),
            'phone': request.form.get('phone'),
            'newsletter': request.form.get('newsletter') == 'on'
        }
        return redirect(url_for('checkout_payment'))
    info = session.get('checkout_info', {})
    if session.get('user_id'):
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
        conn.close()
        if user and not info:
            info = {'email': user['email'], 'first_name': user['first_name'], 'last_name': user['last_name']}
    return render_template('checkout.html', info=info, cart=get_cart())

@app.route('/checkout/payment', methods=['GET', 'POST'])
def checkout_payment():
    if not get_cart():
        return redirect(url_for('cart'))
    if 'checkout_info' not in session:
        return redirect(url_for('checkout'))
    if request.method == 'POST':
        card_number = request.form.get('card_number', '').replace(' ', '')
        last4 = card_number[-4:] if len(card_number) >= 4 else '****'
        info = session['checkout_info']
        cart = get_cart()
        subtotal = cart_subtotal()
        delivery = 30.00
        total = subtotal + delivery
        items_json = json.dumps([{'name': v['name'], 'price': v['price'], 'qty': v['qty']} for v in cart.values()])
        conn = get_db()
        conn.execute('''
            INSERT INTO orders (user_id, email, first_name, last_name, address, city, phone,
                                items, subtotal, delivery, total, payment_last4)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            session.get('user_id'), info['email'], info['first_name'], info['last_name'],
            info['address'], info['city'], info['phone'],
            items_json, subtotal, delivery, total, last4
        ))
        order_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.commit()
        conn.close()
        session['cart'] = {}
        session.pop('checkout_info', None)
        session['last_order'] = {
            'id': order_id,
            'total': total,
            'first_name': info['first_name'],
            'last4': last4
        }
        return redirect(url_for('order_confirmation'))
    subtotal = cart_subtotal()
    return render_template('checkout_payment.html', subtotal=subtotal, delivery=30.00, total=subtotal + 30.00, info=session.get('checkout_info', {}))

@app.route('/order-confirmation')
def order_confirmation():
    order = session.pop('last_order', None)
    if not order:
        return redirect(url_for('home'))
    return render_template('order_confirmation.html', order=order)

# ─── Auth ─────────────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = hash_password(request.form.get('password', ''))
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['first_name']
            flash('Welcome back, ' + user['first_name'] + '!', 'success')
            return redirect(request.args.get('next') or url_for('home'))
        flash('Invalid email or password.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = hash_password(request.form.get('password', ''))
        conn = get_db()
        existing = conn.execute('SELECT id FROM users WHERE email=?', (email,)).fetchone()
        if existing:
            conn.close()
            flash('An account with that email already exists.', 'error')
        else:
            conn.execute('INSERT INTO users (first_name, last_name, email, password) VALUES (?,?,?,?)',
                         (first_name, last_name, email, password))
            conn.commit()
            user = conn.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
            conn.close()
            session['user_id'] = user['id']
            session['user_name'] = user['first_name']
            flash('Account created! Welcome to Pennywise Cosmetics, ' + first_name + '!', 'success')
            return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('home'))

# ─── Favourites ───────────────────────────────────────────────────────────────

@app.route('/favourites')
def favourites():
    fav_ids = get_favourites()
    products = []
    if fav_ids:
        conn = get_db()
        placeholders = ','.join('?' * len(fav_ids))
        products = conn.execute(f'SELECT * FROM products WHERE id IN ({placeholders})', fav_ids).fetchall()
        conn.close()
    return render_template('favourites.html', products=products)

@app.route('/api/favourites/toggle', methods=['POST'])
def toggle_favourite():
    data = request.get_json()
    pid = int(data.get('product_id'))
    if 'user_id' not in session:
        fav_ids = session.get('fav_ids', [])
        if pid in fav_ids:
            fav_ids.remove(pid)
            added = False
        else:
            fav_ids.append(pid)
            added = True
        session['fav_ids'] = fav_ids
        session.modified = True
        return jsonify({'success': True, 'added': added})
    uid = session['user_id']
    conn = get_db()
    existing = conn.execute('SELECT id FROM favourites WHERE user_id=? AND product_id=?', (uid, pid)).fetchone()
    if existing:
        conn.execute('DELETE FROM favourites WHERE user_id=? AND product_id=?', (uid, pid))
        added = False
    else:
        conn.execute('INSERT INTO favourites (user_id, product_id) VALUES (?,?)', (uid, pid))
        added = True
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'added': added})

# ─── Reviews ──────────────────────────────────────────────────────────────────

@app.route('/api/review/add', methods=['POST'])
def add_review():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Login required'})
    data = request.get_json()
    pid = data.get('product_id')
    rating = int(data.get('rating', 5))
    comment = data.get('comment', '').strip()
    if not comment:
        return jsonify({'success': False, 'message': 'Comment required'})
    conn = get_db()
    conn.execute('INSERT INTO reviews (product_id, user_id, user_name, rating, comment) VALUES (?,?,?,?,?)',
                 (pid, session['user_id'], session['user_name'], rating, comment))
    # Update product rating
    stats = conn.execute('SELECT AVG(rating) as avg, COUNT(*) as cnt FROM reviews WHERE product_id=?', (pid,)).fetchone()
    conn.execute('UPDATE products SET rating=?, review_count=? WHERE id=?',
                 (round(stats['avg'], 1), stats['cnt'], pid))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'user_name': session['user_name'], 'rating': rating, 'comment': comment})

# ─── Contact & Other Pages ────────────────────────────────────────────────────

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you for your message! We\'ll get back to you within 24 hours.', 'success')
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    q = request.args.get('q', '')
    return redirect(url_for('products', q=q))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
