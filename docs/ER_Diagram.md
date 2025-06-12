# StoreLoop ER Diagram and Model Description

## Entity Relationship Diagram

```
+---------------+       +---------------+       +---------------+
|    Store      |       |    Product    |       |    Order      |
+---------------+       +---------------+       +---------------+
| id            |<----->| id            |       | id            |
| name          |       | title         |       | product       |<----+
| slug          |       | description   |       | user          |<-+  |
| owner         |<-+    | price         |       | amount        |  |  |
| description   |  |    | image         |       | payment_id    |  |  |
| theme_name    |  |    | qr_code       |       | status        |  |  |
| primary_color |  |    | store         |------>| created_at    |  |  |
| font_choice   |  |    | created_at    |       +---------------+  |  |
| logo          |  |    | updated_at    |                          |  |
| created_at    |  |    +---------------+                          |  |
| updated_at    |  |                                               |  |
+---------------+  |    +---------------+                          |  |
                   |    |     User      |                          |  |
                   |    +---------------+                          |  |
                   +--->| id            |<-------------------------+  |
                        | username      |                             |
                        | email         |                             |
                        | password      |                             |
                        | ...           |                             |
                        +---------------+                             |
```

## Model Descriptions

### Store Model
- **Purpose**: Represents a seller's store in the multi-seller architecture
- **Key Fields**:
  - `name`: Store name
  - `slug`: URL-friendly store identifier
  - `owner`: ForeignKey to User (the store owner)
  - `theme_name`: Selected theme (minimal, warm, dark)
  - `primary_color`: Theme primary color
  - `font_choice`: Selected font family
  - `logo`: Store logo image
  - `custom_css`: Custom CSS injected into store pages
  - `custom_js`: Custom JavaScript injected into store pages

### Product Model
- **Purpose**: Represents products sold in the stores
- **Key Fields**:
  - `title`: Product name
  - `description`: Product description
  - `price`: Product price (DecimalField)
  - `image`: Product image
  - `qr_code`: Generated QR code for product sharing
  - `store`: ForeignKey to Store (which store sells this product)

### Order Model
- **Purpose**: Represents customer orders
- **Key Fields**:
  - `product`: ForeignKey to Product
  - `user`: ForeignKey to User (customer)
  - `amount`: Order amount
  - `payment_id`: Razorpay payment ID
  - `razorpay_order_id`: Razorpay order ID
  - `status`: Order status (pending, completed, etc.)
  - `created_at`: Order creation timestamp

### User Model
- **Purpose**: Django's built-in User model for authentication
- **Key Fields**: Standard Django User fields (username, email, password)

## Relationships

- A Store is owned by a User (one-to-many)
- A Store has many Products (one-to-many)
- A Product belongs to one Store (many-to-one)
- An Order is placed by a User (many-to-one)
- An Order contains a Product (many-to-one)

The multi-seller architecture is implemented through the Store model, which links products to specific sellers (store owners).