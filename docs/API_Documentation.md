# StoreLoop API Documentation

## API Endpoints

### Product Endpoints

#### List All Products
- **URL**: `/products/`
- **Method**: GET
- **Description**: Retrieves a paginated list of all products
- **Query Parameters**:
  - `page`: Page number for pagination
- **Response**:
  ```json
  {
    "products": [
      {
        "id": 1,
        "title": "Product 1",
        "description": "Description of product 1",
        "price": "99.99",
        "image_url": "/media/products/product1.jpg",
        "store": {
          "id": 1,
          "name": "Store 1",
          "slug": "store-1"
        }
      }
    ],
    "page": 1,
    "total_pages": 5
  }
  ```

#### Get Product Details
- **URL**: `/products/<int:pk>/`
- **Method**: GET
- **Description**: Retrieves details of a specific product
- **URL Parameters**:
  - `pk`: Product ID
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Product 1",
    "description": "Detailed description of product 1",
    "price": "99.99",
    "image_url": "/media/products/product1.jpg",
    "qr_code_url": "/media/qrcodes/product_1.png",
    "store": {
      "id": 1,
      "name": "Store 1",
      "slug": "store-1"
    },
    "related_products": [
      {
        "id": 2,
        "title": "Related Product",
        "price": "79.99"
      }
    ]
  }
  ```

### Order Endpoints

#### Create Order
- **URL**: `/orders/create/<int:product_id>/`
- **Method**: POST
- **Description**: Creates a new order for a product and initiates payment
- **URL Parameters**:
  - `product_id`: Product ID
- **Request Body**: None required
- **Response**:
  ```json
  {
    "order_id": 1,
    "razorpay_order_id": "order_123456",
    "amount": 9999,
    "currency": "INR",
    "key_id": "rzp_test_123456"
  }
  ```

#### Payment Success Callback
- **URL**: `/orders/payment/success/`
- **Method**: POST
- **Description**: Handles successful payment callback from Razorpay
- **Request Body**:
  ```json
  {
    "razorpay_payment_id": "pay_123456",
    "razorpay_order_id": "order_123456",
    "razorpay_signature": "signature_hash"
  }
  ```
- **Response**: Redirects to order confirmation page

#### Order Confirmation
- **URL**: `/orders/confirmation/<int:order_id>/`
- **Method**: GET
- **Description**: Shows order confirmation page
- **URL Parameters**:
  - `order_id`: Order ID
- **Response**: HTML page with order details

### Store Endpoints

#### Store Products
- **URL**: `/stores/store/<slug:slug>/`
- **Method**: GET
- **Description**: Lists products from a specific store
- **URL Parameters**:
  - `slug`: Store slug
- **Response**: HTML page with store products

#### Store Theme Settings
- **URL**: `/stores/store/<int:store_id>/theme/`
- **Method**: GET, POST
- **Description**: Manage store theme settings
- **URL Parameters**:
  - `store_id`: Store ID
- **Request Body (POST)**:
  ```json
  {
    "theme_name": "dark",
    "primary_color": "#ff5722",
    "font_choice": "sans",
    "custom_css": ".my-custom-class { color: red; }",
    "custom_js": "console.log('Custom JS loaded');"
  }
  ```
- **Response**: HTML page with theme settings form