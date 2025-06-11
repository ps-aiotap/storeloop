# StoreLoop

StoreLoop is a Django-based eCommerce platform designed for single-seller storefronts with future multi-seller capabilities.

## Features

- Product catalog with images and QR codes
- Razorpay payment integration
- Order management
- Admin panel for product and order management
- Responsive design with Tailwind CSS
- Email notifications for orders

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/storeloop.git
   cd storeloop
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file from the example:
   ```
   cp .env.example .env
   ```
   Then edit the `.env` file with your own settings.

6. Run migrations:
   ```
   python manage.py migrate
   ```

7. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```
   python manage.py runserver
   ```

9. Access the site at http://127.0.0.1:8000/

### Razorpay Setup

1. Create a Razorpay account at https://razorpay.com/
2. Get your API keys from the Razorpay Dashboard
3. Add your Razorpay API keys to the `.env` file

## Development

### Adding Sample Data

To add sample products:

```
python manage.py loaddata sample_data.json
```

### Running Tests

```
pytest
```

## Project Structure

- `core/` - Main project settings
- `products/` - Product catalog app
- `orders/` - Order management app
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)
- `media/` - User-uploaded files

## Future Enhancements

- Multi-seller support
- Product categories and filtering
- User accounts and profiles
- Wishlist functionality
- Product reviews and ratings

## GitHub Issue Tracker Setup

Suggested labels for GitHub issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

## License

This project is licensed under the MIT License - see the LICENSE file for details.