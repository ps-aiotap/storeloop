# StoreLoop

StoreLoop is a Django-based e-commerce platform with multi-seller support, customizable themes, and integrated payment processing.

## Features

### Store Management
- Multi-seller platform with individual store profiles
- Store-specific product catalogs and branding
- Custom domain support for each store
- Store analytics and performance metrics
- JSON-driven homepage builder for each store

### Product Management
- Comprehensive product catalog with images, descriptions, and pricing
- Dynamic tagging system with configurable tag types (Occasion, Lifestyle, Festival, etc.)
- Product bundles/combos with shared inventory management
- Product variants (size, color, etc.)
- QR code generation for products (for easy sharing/scanning)
- Stock management and inventory tracking

### Theme System
- Advanced theming engine with CSS variables and Tailwind integration
- Base themes with inheritance support for child themes
- Three built-in themes: Minimal, Warm, and Dark
- Theme customization options:
  - Primary and secondary color selection
  - Font family choice (sans-serif, serif, monospace)
  - Custom logo upload
  - Custom CSS/JS injection
  - Overridable layout blocks
- Responsive design across all themes
- Dark mode support with automatic detection

### Homepage Builder
- Drag-and-drop interface for arranging content blocks
- Multiple block types:
  - Hero banners with customizable images and CTAs
  - Product grids with filtering options
  - Testimonial sections with different display styles
  - Text blocks with rich formatting
  - Image galleries and video embeds
  - Trust badge displays
  - Contact/inquiry forms
  - Tag collection displays
- Block-specific configuration options
- Enable/disable blocks without deleting them
- Real-time preview of changes

### Content Management
- Static pages with WYSIWYG or markdown editing
- Trust badge management for displaying certifications and guarantees
- SEO-friendly dynamic landing pages for tags and collections
- Contact and inquiry form management

### Shopping Experience
- Responsive, mobile-friendly design
- Product search and filtering
- Related products recommendations
- Interactive product cards with hover effects and animations
- Streamlined checkout process
- Form validation with real-time feedback

### Analytics
- Vendor-specific dashboard with performance metrics
- Product view tracking and statistics
- Tag performance analysis
- Order conversion statistics

### Payment Processing
- Integrated Razorpay payment gateway
- Secure payment processing
- Order confirmation and tracking
- Email notifications for order status

### User Experience
- Form validation with real-time feedback
- Responsive design for all device sizes
- Accessibility-focused UI components
- Intuitive navigation and user flow
- Store switcher for multi-store browsing

### Technical Features
- Built with Django 4.2 LTS
- PostgreSQL database for robust data storage
- Tailwind CSS for modern styling
- React components for interactive UI elements
- Alpine.js for lightweight interactions
- CSS variables for theme customization
- Modular architecture for easy extension
- Optimized for performance and SEO

## Setup

1. Clone the repository
2. Create a virtual environment and install dependencies:
   ```
   python -m venv storeloop-venv
   source storeloop-venv/bin/activate  # On Windows: storeloop-venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set up PostgreSQL:
   ```
   # Create a database
   createdb storeloop
   
   # Or using psql
   psql -U postgres
   CREATE DATABASE storeloop;
   ```
4. Create a `.env` file based on `.env.example` with your database and Razorpay API keys:
   ```
   # Database settings
   DB_NAME=storeloop
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   
   # Razorpay settings
   RAZORPAY_KEY_ID=your_key_id
   RAZORPAY_KEY_SECRET=your_key_secret
   ```
5. Run migrations and create a superuser:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```

## Theme Configuration

1. Create a Store in the admin interface
2. Navigate to `/stores/store/{store_id}/theme/` to configure the theme
3. Choose from Minimal, Warm, or Dark themes or create a custom theme
4. Select primary and secondary colors
5. Choose a font style (sans-serif, serif, monospace)
6. Upload a store logo
7. Add custom CSS/JS if needed
8. Optionally override specific layout blocks

## Homepage Builder

1. Navigate to `/stores/{store_slug}/homepage/editor/` to access the homepage builder
2. Add blocks from the library panel on the left
3. Configure each block's settings in the right panel
4. Drag and drop blocks to reorder them
5. Toggle blocks on/off using the visibility control
6. Preview your homepage with the "Preview Homepage" button

## Content Management

1. Create static pages like About, FAQ, or Workshops in the admin interface
2. Upload and configure trust badges to display on product pages
3. Set up contact forms with customizable fields and integrations
4. Create tag collections for SEO-friendly landing pages

## Payment Integration

1. Sign up for a Razorpay account
2. Add your Razorpay API keys to the `.env` file
3. Test the payment flow using Razorpay test cards

## Development

### Architecture
- Modular Django apps: products, orders, stores
- Component-based templates for reusability
- CSS variables + Tailwind for theming
- React for interactive UI (homepage builder)
- Alpine.js for lightweight interactions

### Testing & Quality
```bash
# Run comprehensive tests
pytest stores/tests/test_comprehensive.py -v

# Run all tests with coverage
pytest --cov=./ --cov-report=html

# Code formatting
black . && isort . && flake8 .
```

### Automated Form Testing
```bash
# Complete form testing pipeline (Discovery → Generation → Execution)
cd tests/playwright
npm install && playwright install

# Basic pipeline
npm run one-step

# Advanced pipeline (includes security, performance, accessibility)
npm run advanced-pipeline

# Specialized testing
npm run test-security      # Security tests (XSS, SQL injection, CSRF)
npm run test-performance   # Performance and load testing
npm run test-accessibility # Keyboard navigation and a11y

# Individual steps
npm run nav-discover    # Discover forms via navigation
npm run generate        # Generate tests from discovered forms  
npm test               # Run generated tests
```

**Features:**
- 🔍 **Zero-assumption discovery** - Crawls actual navigation links
- 🧪 **Comprehensive testing** - Happy path, validation, security, edge cases
- 🛡️ **Security testing** - XSS, SQL injection, CSRF protection
- ⚡ **Performance monitoring** - Form submission timing and rate limiting
- ♿ **Accessibility testing** - Keyboard navigation and ARIA compliance
- 📊 **Enhanced reporting** - Custom dashboard with metrics and coverage
- 🚀 **CI/CD integration** - GitHub Actions workflow included
- 🔄 **Parallel execution** - Multi-worker test execution

**Generated files are automatically excluded from Git tracking.**

**For other projects:** See [FORM_TESTING_PROMPTS.md](FORM_TESTING_PROMPTS.md) for implementation prompts.

### Sample Data
```bash
# Seed development data
python manage.py seed_sample_data --users 3 --stores 2 --products 10
```

### New Features
- **Product Variants**: Size, color, material variants with individual QR codes
- **Enhanced Homepage Builder**: Improved drag-and-drop with state isolation
- **Security**: Razorpay signature verification, rate limiting, webhook validation
- **SEO**: Multi-store sitemaps, structured data, comprehensive robots.txt
- **Extensible Blocks**: Plugin system for third-party homepage blocks

### CI/CD
GitHub Actions workflow includes:
- Parallel testing (unit, integration, security)
- Code quality checks (Black, isort, Flake8, MyPy)
- Security scanning (Bandit, Safety)
- Performance testing

## Admin Guide

For detailed instructions on using the admin features (Bundles, Homepage Blocks, Trust Badges, etc.), please refer to the [Admin Guide](ADMIN_GUIDE.md).