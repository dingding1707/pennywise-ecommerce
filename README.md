# Pennywise Cosmetics - E-Commerce Web App

A full-stack e-commerce web application for Pennywise Cosmetics Ltd, built with Flask (Python) and SQLite.

## Features

- **Product Catalogue**: 37 products across 5 categories (Cosmetics, Skincare, Hair, Perfumes, Bath & Body)
- **Product Detail Pages**: Descriptions, ratings, reviews, size/brand info, related products
- **Shopping Cart**: Add/remove/update quantities, real-time price calculation
- **Full Checkout Flow**: Delivery info → Payment info → Order confirmation
- **User Authentication**: Register, login, logout with session management
- **Favourites**: Save/unsave products (works for guests too)
- **Reviews**: Logged-in users can submit star ratings and comments
- **Search & Filter**: Filter by category, Bestsellers, New, Value Sets, Mini; sort by price/rating
- **Contact Page**: Contact form with pharmacy WhatsApp numbers
- **About Page**: Company history and mission
- **Responsive Design**: Works on mobile and desktop
- **Pink Pennywise Branding**: Matches real Pennywise Cosmetics colour scheme

## Tech Stack

- **Backend:** Flask 3.x (Python), SQLite
- **Frontend:** Jinja2 templates, vanilla HTML/CSS/JS
- **Fonts:** Playfair Display + Nunito (Google Fonts)

## Setup

```bash
pip install flask
cd pennywise
python app.py
# Visit: http://localhost:5000
```
## Hosting
Hosted by PythonAnywhere at **https://dariah1707.pythonanywhere.com**
The SQLite DB is auto-created and seeded on first run.

## Project Structure

```
pennywise/
├── app.py                     # All routes, DB init, helpers
├── templates/
│   ├── base.html              # Navbar, footer, cart badge, toast
│   ├── home.html              # Hero, categories, bestsellers, new arrivals
│   ├── products.html          # Catalogue with filters & sorting
│   ├── product_detail.html    # Product page with reviews
│   ├── cart.html              # Shopping cart
│   ├── checkout.html          # Step 1: Delivery address
│   ├── checkout_payment.html  # Step 2: Payment
│   ├── order_confirmation.html
│   ├── login.html / register.html
│   ├── favourites.html
│   ├── contact.html
│   └── about.html
```
