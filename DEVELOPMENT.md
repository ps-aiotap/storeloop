# StoreLoop Development Guide

StoreLoop is a Django-based e-commerce platform with multi-seller and theme support. This guide will help you set up a local development environment and understand the project structure.

## Prerequisites

- Python 3.8+
- Node.js and npm (for Tailwind CSS)
- Git

## Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/storeloop.git
   cd storeloop
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv storeloop-venv
   # On Windows
   storeloop-venv\Scripts\activate
   # On macOS/Linux
   source storeloop-venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Node.js dependencies:
   ```bash
   npm install
   ```

5. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

6. Run migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Build Tailwind CSS:
   ```bash
   npm run build
   ```

9. Run the development server:
   ```bash
   python manage.py runserver
   ```

10. Access the site at http://127.0.0.1:8000/

## Project Structure

```
storeloop/
├── core/                  # Project settings and main URLs
├── products/              # Product models, views, and templates
├── orders/                # Order processing and payment integration
├── stores/                # Multi-seller store models and theme settings
├── plugins/               # Plugin system for extending functionality
├── templates/             # Base templates and shared components
│   ├── base.html          # Main template with theme support
│   ├── products/          # Product-specific templates
│   ├── orders/            # Order-specific templates
│   └── stores/            # Store-specific templates
│       └── themes/        # Theme templates (minimal, warm, dark)
├── static/                # Static files (CSS, JS, images)
├── media/                 # User-uploaded files
├── themestaticsrc/        # Tailwind source files
│   └── input.css          # Tailwind input CSS
├── staticcss/             # Generated CSS output
├── docs/                  # Project documentation
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Key Modules

### Core Module
- Contains project settings, main URL configuration, and shared utilities
- Manages environment variables and configuration
- Implements the plugin system for extending functionality

### Products Module
- Manages product catalog, listings, and detail views
- Handles product images and QR code generation
- Provides product search and filtering

### Orders Module
- Processes customer orders
- Integrates with Razorpay for payments
- Handles order confirmation and status updates

### Stores Module
- Implements multi-seller architecture
- Manages store profiles and theme settings
- Provides store-specific product listings
- Handles custom CSS/JS injection for store customization

## Theme System

StoreLoop supports three built-in themes:
1. **Minimal**: Clean, simple design with white background
2. **Warm**: Amber-tinted design with warmer colors
3. **Dark**: Dark mode with light text on dark background

Each theme can be customized with:
- Primary color
- Font choice (sans-serif, serif, monospace)
- Store logo
- Custom CSS/JS

### Theme Structure

Themes are organized in a versioned structure to prevent customizations from being overwritten during updates:

```
templates/
└── stores/
    └── themes/
        ├── minimal/
        │   ├── v1/
        │   │   ├── product_list.html
        │   │   └── product_detail.html
        │   └── v2/
        │       ├── product_list.html
        │       └── product_detail.html
        ├── warm/
        │   └── v1/
        │       ├── product_list.html
        │       └── product_detail.html
        └── dark/
            └── v1/
                ├── product_list.html
                └── product_detail.html
```

## Plugin System

StoreLoop includes a plugin system for extending functionality without modifying core code. Plugins can add:
- New payment providers
- Shipping methods
- Additional features

### Creating a Plugin

1. Create a new Python package in the `plugins` directory
2. Implement the appropriate plugin interface (e.g., `PaymentProvider`, `ShippingProvider`)
3. Register the plugin in `settings.py` under `STORELOOP_PLUGINS`

Example plugin structure:
```
plugins/
└── my_shipping/
    ├── __init__.py
    ├── provider.py
    └── templates/
        └── my_shipping/
            └── form.html
```

## Testing

Run tests with:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=.
```

## Building CSS

When modifying Tailwind CSS:
1. Edit files in `themestaticsrc/`
2. Run `npm run build` to generate production CSS
3. For development with auto-reload: `npm run dev`

## Extending StoreLoop

### Adding a New App
1. Create the Django app:
   ```bash
   python manage.py startapp app_name
   ```
2. Add to INSTALLED_APPS in settings.py
3. Create models, views, and templates
4. Add URL patterns to core/urls.py

### Adding a New Theme
1. Create a new theme directory in `templates/stores/themes/`
2. Add the theme option to `THEME_CHOICES` in `stores/models.py`
3. Create theme-specific templates

### Creating a Custom Plugin
1. Create a new package in the `plugins` directory
2. Implement the appropriate plugin interface
3. Register the plugin in `settings.py`