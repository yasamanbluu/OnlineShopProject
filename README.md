# Online Biotech Shop

## Project Overview

Online Biotech Shop is a desktop-based e-commerce application developed in Python using Object-Oriented Programming (OOP) principles and the Tkinter library.

Tاhis project is a small biotechnology product store where customers can browse laboratory products, search for items, place orders, and submit reviews. Admins can manage products, apply discounts, monitor inventory, and generate sales reports. All application data is stored using CSV files without relying on a database management system.

## Features

### Customer Features
- Browse 12 biotech products with images
- Search products by name or category
- View product ratings and customer reviews
- Add products to shopping cart
- See discount prices automatically calculated
- Leave reviews/ratings for products (1-5 stars)
- See other customers' reviews in real-time
- Checkout and place orders

### Admin Features
- Add new products to the system
- Edit existing products (name, price, stock, discount)
- Delete products
- View all orders and sales reports
- Filter orders by date
- Changes automatically saved to CSV

### Data Management
- CSV-based database (no SQL needed)
- Automatic data reload on login/logout
- Product images stored locally
- Customer reviews persistent in database

## Extra Features

The following features were implemented in addition to the required project specifications:

- Product image display
- Product discount system
- Customer review and rating system
- Product search
- Shopping cart
- Sales report based on dates
- Automatic CSV synchronization

## Project Structure

```
OnlineShopProject2/
├── gui_complete_main.py           # Main application entry point
├── gui_complete_login.py          # Login screen
├── gui_complete_customer.py       # Customer panel (with reviews)
├── gui_complete_admin.py          # Admin panel
├── gui_complete_simple_styles.py  # Colors and fonts
│
├── user.py                         # User class
├── product.py                      # Product class
├── customer.py                     # Customer logic
├── admin.py                        # Admin logic
├── order.py                        # Order class
├── comment.py                      # Review/Comment class
│
├── database.py                     # CSV database handler
├── file.py                         # CSV operations (alternative)
├── validators.py                   # Input validation
├── exceptions.py                   # Custom exceptions
├── features.py                     # Extra features (cart, discounts, search, reviews)
│
└── data/
    ├── users.csv                   # User accounts
    ├── products.csv                # Product catalog
    ├── orders.csv                  # Order history
    ├── reviews.csv                 # Customer reviews
    └── Product_images/             # Product photos (1.png - 12.png)
```

## Installation

### Requirements
- Python 3.8+
- Tkinter (usually comes with Python)
- Pillow (for images)

### Setup

1. **Install Python packages:**
```bash
pip install pillow
```

2. **Copy project files:**
- All Python files in same folder
- `data/` folder with CSV files and images


## How to Run

### Option 1: Spyder IDE
```python
%runfile C:/path/to/OnlineShopProject2/gui_complete_main.py --wdir
```

### Option 2: Terminal/Command Prompt
```bash
cd OnlineShopProject2
python gui_complete_main.py
```

### Option 3: Direct Run
Double-click `gui_complete_main.py`

## Default Accounts

### Admin Account
```
Username: soltani
Password: soltani123
```

### Customer Accounts
```
Username: hamidi       Password: hamidi123
Username: rahmani      Password: rahmani123
Username: karimi       Password: karimi123
```

## How to Use

### As a Customer

1. **Login**
   - Enter username and password
   - Click Login

2. **Browse Products**
   - See all 12 products with images
   - View prices with applied discounts
   - Read customer reviews (⭐ rating)

3. **Search**
   - Type product name in search box
   - Click Search to filter

4. **Shopping**
   - Click "Add to Cart" for any product
   - See items in cart on right side
   - Cart shows total with discounts

5. **Leave Review**
   - Click "💬 Review" on any product
   - Select rating (1-5 stars)
   - Type your comment
   - Click "Post Review"
   - Your review appears for all customers

6. **Checkout**
   - Click "Checkout" when done shopping
   - See order summary
   - Order saved to system

### As an Admin

1. **Login**
   - Use soltani account

2. **Manage Products**
   - Click a product to select it
   - Edit name, price, stock, discount
   - Click "Edit Selected" to save (auto-saves to CSV)
   - Use "Delete Selected" to remove

3. **Add New Product**
   - Fill in product details
   - Click "Add Product"
   - New product appears in system

4. **View Reports**
   - Go to "Orders & Report" tab
   - See all customer orders
   - Filter by date if needed
   - View total sales

## Features Explained

### Automatic Discount Application
When admin sets discount in product form, it's immediately:
- Saved to CSV
- Applied to prices shown to customers
- Used in cart total calculations

### Reviews
- Any customer can write a review
- Review saved to reviews.csv
- All customers can read it
- Shows username, rating, comment, date

### Image Display
- Products show 150x150px images
- Images from `data/Product_images/` folder
- If image missing, shows placeholder

### Price Calculations
- Final price = Price × (100 - Discount%) ÷ 100
- Applied automatically in cart
- Shown next to original price

## Project Requirements Met

✅ Customer role with browse/search/cart/checkout  
✅ Admin role with add/edit/view features  
✅ CSV data files (users, products, orders)  
✅ Product images display  
✅ Discount system  
✅ Customer reviews with ratings  
✅ Sales reports and filtering  
✅ Error handling  
✅ Tkinter/GUI  
✅ All team members contributed  

## Known Limitations

- No database (uses CSV files only)
- No user registration (fixed accounts only)
- No payment integration
- Images must be in Product_images folder
- Single user login at a time

## Notes

- All changes by admin are permanent (saved to CSV)
- Customer reviews appear for all users immediately
- Products reload from CSV on each login
- Balance and orders tracked in database
- Multiple customers can leave reviews on same product

## Team Members

- **Ayda Mardane (Backend):** OOP classes (User, Product, Order, etc.)
- **Mahdieh Soltani (Database):** CSV handling and data management
- **Kimia Hasanzadeh(GUI):** Tkinter interface and user experience
- **Yasaman Khatibi(Features):** Shopping cart, discounts, search, reports

## GitHub Repository

Repository Link:

```
https://github.com/yasamanbluu/OnlineShopProject
```

Last Updated: June 2026  
