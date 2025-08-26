# Task 2: Secure Shopping Cart API with Admin Access

A FastAPI-based shopping cart API with role-based access control. Admins can manage products, while all authenticated users can browse and shop.

## Features

- User authentication with roles (admin/customer)
- Role-based access control using dependency injection
- Admin-only product management
- Public product browsing
- Authenticated shopping cart functionality
- JSON file storage for users, products, and carts

## Project Structure

```
shopping-cart-rbac/
├── main.py          # Main FastAPI application
├── auth.py          # Authentication and authorization module
├── users.json       # User data (created automatically)
├── products.json    # Product data (created automatically)
├── cart.json        # Shopping cart data (created automatically)
└── README.md        # This file
```

## Installation

1. Install required packages:

```bash
pip install fastapi uvicorn
```

2. Run the application:

```bash
cd shopping-cart-rbac
python main.py
```

## Default Users

The system creates default users on first run:

- **Admin**: username: `admin`, password: `admin123`
- **Customer**: username: `customer1`, password: `password123`

## API Endpoints

### Public Endpoints

#### Get All Products

- **GET** `/products/`
- **Description**: View all available products
- **Authentication**: None required

#### Get Specific Product

- **GET** `/products/{product_id}`
- **Description**: View details of a specific product
- **Authentication**: None required

### Admin-Only Endpoints

#### Add Product

- **POST** `/admin/add_product/`
- **Authentication**: Admin role required
- **Body**:

```json
{
  "name": "Laptop",
  "price": 999.99,
  "description": "High-performance laptop",
  "stock": 10
}
```

### Authenticated User Endpoints

#### Add to Cart

- **POST** `/cart/add/`
- **Authentication**: Any authenticated user
- **Body**:

```json
{
  "product_id": 1,
  "quantity": 2
}
```

#### View Cart

- **GET** `/cart/`
- **Authentication**: Any authenticated user
- **Response**: Cart with product details and total

#### Clear Cart

- **DELETE** `/cart/clear/`
- **Authentication**: Any authenticated user

## How to Test

### 1. View Products (No authentication required)

```bash
curl -X GET "http://localhost:8000/products/"
```

### 2. Add Product (Admin only)

```bash
curl -X POST "http://localhost:8000/admin/add_product/" \
-H "Content-Type: application/json" \
-u "admin:admin123" \
-d '{
    "name": "Smartphone",
    "price": 699.99,
    "description": "Latest smartphone model",
    "stock": 15
}'
```

### 3. Add to Cart (Any authenticated user)

```bash
curl -X POST "http://localhost:8000/cart/add/" \
-H "Content-Type: application/json" \
-u "customer1:password123" \
-d '{
    "product_id": 1,
    "quantity": 1
}'
```

### 4. View Cart

```bash
curl -X GET "http://localhost:8000/cart/" \
-u "customer1:password123"
```

## Interactive Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation.

## Authentication & Authorization

### Role-Based Access Control

- **Admin**: Can add products + all customer features
- **Customer**: Can browse products and manage their cart

### Dependencies Used

- `get_current_user`: Authenticates any user
- `require_admin_role`: Requires admin role
- `require_customer_or_admin_role`: Allows both roles

## File Storage

### users.json

```json
{
  "admin": {
    "password": "hashed_password",
    "role": "admin"
  },
  "customer1": {
    "password": "hashed_password",
    "role": "customer"
  }
}
```

### products.json

```json
{
  "1": {
    "id": 1,
    "name": "Laptop",
    "price": 999.99,
    "description": "High-performance laptop",
    "stock": 10
  }
}
```

### cart.json

```json
{
  "customer1": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

## Security Features

- Password hashing using SHA-256
- Role-based access control
- HTTP Basic Authentication
- Input validation with Pydantic
- Proper error handling and status codes
