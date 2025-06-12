# StoreLoop URL Mapping

This document maps all URLs in the StoreLoop application to their corresponding views and describes their purpose.

| URL Pattern | View | HTTP Methods | Purpose |
|-------------|------|-------------|---------|
| `/` | ProductListView | GET | Homepage showing all products |
| `/products/` | ProductListView | GET | List all products across stores |
| `/products/<int:pk>/` | ProductDetailView | GET | Show details of a specific product |
| `/orders/create/<int:product_id>/` | create_order | POST | Create a new order for a product |
| `/orders/payment/success/` | payment_success | POST | Handle successful payment callback from Razorpay |
| `/orders/confirmation/<int:order_id>/` | order_confirmation | GET | Show order confirmation page |
| `/stores/` | StoreListView | GET | List all stores |
| `/stores/store/<int:store_id>/theme/` | store_theme_settings | GET, POST | Manage store theme settings |
| `/stores/store/<slug:slug>/` | StoreProductListView | GET | Show products from a specific store |
| `/admin/` | Django Admin | GET, POST | Admin interface for site management |

## View Descriptions

### Product Views

- **ProductListView**: Class-based view that displays a paginated list of all products. Supports filtering by store and theme-specific templates.
- **ProductDetailView**: Class-based view that shows detailed information about a specific product, including related products from the same store.

### Order Views

- **create_order**: Function-based view that creates a new order for a product and initiates the Razorpay payment process.
- **payment_success**: Function-based view that handles the callback from Razorpay after a successful payment, updating the order status.
- **order_confirmation**: Function-based view that displays the order confirmation page after a successful payment.

### Store Views

- **StoreListView**: Class-based view that displays a list of all stores.
- **store_theme_settings**: Function-based view that allows store owners to manage their store's theme settings.
- **StoreProductListView**: Class-based view that displays products from a specific store, using the store's theme.