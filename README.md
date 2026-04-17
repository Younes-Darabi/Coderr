# 📝 Coderr API - Freelance Marketplace Backend

Coderr is a powerful **Django REST Framework** backend for a freelance marketplace platform. It connects **Customers** and **Businesses** (freelancers/agencies) through offers, orders, reviews, and professional profiles.

---

## 🚀 Key Features

### 🔐 Authentication
- **User Registration & Login:** Supports both `customer` and `business` user types.
- **Token-based Authentication:** Secure access for all protected endpoints.

### 👤 Profile Management
- Detailed customer and business profiles with rich information.
- Separate endpoints for listing all business or customer profiles.
- Full CRUD support for own profile (including profile picture, description, working hours, etc.).

### 📦 Offers & Packages
- Businesses can create multi-tier offers (Basic, Standard, Premium).
- Each offer includes multiple **Offer Details** with price, delivery time, revisions, and features.
- Advanced filtering, search, and sorting.
- Dynamic calculation of `min_price` and `min_delivery_time`.

### 🛒 Orders
- Customers can place orders directly from an Offer Detail.
- Order status management (`in_progress`, `completed`, `cancelled`).
- Business users can update order status.
- Order history for both customers and businesses.

### ⭐ Reviews & Ratings
- Customers can leave one review per business.
- Edit and delete own reviews.
- Filtering and ordering support.

### 📊 Platform Insights
- Base information endpoint with total reviews, average rating, number of businesses, and offers.

---

## 🛠 Tech Stack
- **Framework:** Django + Django REST Framework
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **Authentication:** DRF Token Authentication
- **Pagination:** PageNumberPagination

---

## 🔧 Installation & Setup

1. **Clone the project:**

        git clone https://github.com/Younes-Darabi/Coderr
        cd Coderr


3. Set up a Virtual Environment:

        python -m venv .venv
   
# Windows:

        .venv\Scripts\activate
        
# Linux/Mac:
   
        source .venv/bin/activate

3. Environment Configuration:
   Create a `.env` file in the root directory and add your secret key:
   ```env
   SECRET_KEY=your_secret_key_here

4. Install Dependencies:

        pip install -r requirements.txt

5. Apply Database Migrations:

        python manage.py migrate

6. Run the Development Server:

        python manage.py runserver


---

## 📍 API Endpoints Overview
### 🔐 Authentication

- POST /api/registration/ — Register new user (customer or business)
- POST /api/login/ — Login and receive token

### 👤 Profile

- GET /api/profile/{pk}/ — Get user profile
- PATCH /api/profile/{pk}/ — Update own profile
- GET /api/profiles/business/ — List all business profiles
- GET /api/profiles/customer/ — List all customer profiles

### 📦 Offers

- GET /api/offers/ — List offers (with filters, search, ordering)
- POST /api/offers/ — Create new offer (Business only)
- GET /api/offers/{id}/ — Get specific offer
- PATCH /api/offers/{id}/ — Update offer (Owner only)
- DELETE /api/offers/{id}/ — Delete offer (Owner only)
- GET /api/offerdetails/{id}/ — Get offer detail

### 🛒 Orders

- GET /api/orders/ — List user's orders (as customer or business)
- POST /api/orders/ — Create new order (Customer only)
- PATCH /api/orders/{id}/ — Update order status (Business only)
- DELETE /api/orders/{id}/ — Delete order (Admin only)
- GET /api/order-count/{business_user_id}/ — Count active orders
- GET /api/completed-order-count/{business_user_id}/ — Count completed orders

### ⭐ Reviews

- GET /api/reviews/ — List reviews (with filters)
- POST /api/reviews/ — Create review (Customer only)
- PATCH /api/reviews/{id}/ — Update own review
- DELETE /api/reviews/{id}/ — Delete own review

### 📊 Others

- GET /api/base-info/ — Get platform statistics


### 🛡 Permissions Summary

- Business users can create and manage offers.
- Customer users can create orders and reviews.
- Users can only modify their own content (profile, offers, reviews, orders status).
- Proper ownership and role-based permissions applied across all endpoints.

---

### 🔗 Related Projects
This repository is the Backend API of the Coderr platform.
* **Frontend Repository:** [https://github.com/Developer-Akademie-Backendkurs/project.Coderr](https://github.com/Developer-Akademie-Backendkurs/project.Coderr)

---

Developed with ❤️ by Younes
