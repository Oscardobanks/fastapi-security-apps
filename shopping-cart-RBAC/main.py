from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Dict
import json
import os
from auth import get_current_user, require_admin_role, User

app = FastAPI(title="Secure Shopping Cart API",
              description="A simple shopping cart API with admin and customer roles")


class CartItem(BaseModel):
    product_id: str
    quantity: int


class CartResponse(BaseModel):
    username: str
    items: List[Dict]
    total: float


class Product(BaseModel):
    id: str
    name: str
    price: float
    description: str
    stock: int = 0


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str
    stock: int = 0


def load_products() -> Dict[str, Product]:
    try:
        if not os.path.exists("products.json"):
            return {}
        with open("products.json", "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading products: {e}")
        return {}


def save_products(products: Dict[str, Product]) -> bool:
    try:
        with open("products.json", "w") as file:
            json.dump(products, file, indent=2)
        return True
    except Exception as e:
        print(f"Error saving products: {e}")
        return False


def load_carts() -> Dict:
    try:
        if not os.path.exists("carts.json"):
            return {}
        with open("cart.json", "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading carts: {e}")
        return {}


def save_carts(carts: Dict) -> bool:
    try:
        with open("cart.json", "w") as file:
            json.dump(carts, file, indent=2)
        return True
    except Exception as e:
        print(f"Error saving carts: {e}")
        return False


@app.post("/admin/add_product/", response_model=Product)
def add_product(Product: ProductCreate, current_user: User = Depends(require_admin_role)):
    try:
        products = load_products()

        if products:
            max_id = max([int(item['id']) for item in products.values()])
            new_id = max_id + 1
        else:
            new_id = 1

        new_product = Product(
            id=str(new_id),
            name=Product.name,
            price=Product.price,
            description=Product.description,
            stock=Product.stock
        )

        products[str(new_id)] = new_product
        save_products(products)
        return Product
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product already exists")
    except Exception as e:
        print(f"Error adding product: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@app.get("/products", response_model=List[Product])
def get_products():
    try:
        products = load_products()
        return list(products.values())
    except Exception as e:
        print(f"Error getting products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    try:
        products = load_products()
        if str(product_id) in products:
            return products[str(product_id)]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except Exception as e:
        print(f"Error getting product: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@app.post("/cart/add")
def add_to_cart(cart_item: CartItem, current_user: User = Depends(get_current_user)):
    try:
        products = load_products()
        if str(cart_item.product_id) not in products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        product = products[str(cart_item.product_id)]
        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient stock. Available: {product.stock}")

        carts = load_carts()
        if current_user.username not in carts:
            carts[current_user.username] = []

        # Check if item already exist in cart
        user_cart = carts[current_user.username]
        existing_item = None
        for item in user_cart:
            if item['product_id'] == cart_item.product_id:
                existing_item = item
                break

        if existing_item:
            # Update quantity of existing item
            new_quantity = existing_item['quantity'] + cart_item.quantity
            if product.stock < new_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient stock. Available stock: {product.stock}")
            existing_item['quantity'] = new_quantity
        else:
            # Add new item to cart
            user_cart.append({
                'product_id': cart_item.product_id,
                'quantity': cart_item.quantity
            })

    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid cart item data")
    except Exception as e:
        print(f"Error adding to cart: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
