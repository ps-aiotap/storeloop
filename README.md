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
- Product categorization and tagging
- Product variants (size, color, etc.)
- QR code generation for products (for easy sharing/scanning)
- Stock management and inventory tracking

### Theme System
- Advanced theming engine with CSS variables and Tailwind integration
- Three built-in themes: Minimal, Warm, and Dark
- Theme customization options:
  - Primary color selection
  - Font family choice (sans-serif, serif, monospace)
  - Custom logo upload
  - Custom CSS/JS injection
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
- Block-specific configuration options
- Enable/disable blocks without deleting them
- Real-time preview of changes

### Shopping Experience
- Responsive, mobile-friendly design
- Product search and filtering
- Related products recommendations
- Interactive product cards with hover effects and animations
- Streamlined checkout process
- Form validation with real-time feedback

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

### Technical Features
- Built with Django 4.2 LTS
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
3. Create a `.env` file based on `.env.example` with your Razorpay API keys
4. Run migrations and create a superuser:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```
   python manage.py runserver
   ```

## Theme Configuration

1. Create a Store in the admin interface
2. Navigate to `/stores/store/{store_id}/theme/` to configure the theme
3. Choose from Minimal, Warm, or Dark themes
4. Select a primary color and font style
5. Upload a store logo
6. Add custom CSS/JS if needed

## Homepage Builder

1. Navigate to `/stores/{store_slug}/homepage/editor/` to access the homepage builder
2. Add blocks from the library panel on the left
3. Configure each block's settings in the right panel
4. Drag and drop blocks to reorder them
5. Toggle blocks on/off using the visibility control
6. Preview your homepage with the "Preview Homepage" button

## Payment Integration

1. Sign up for a Razorpay account
2. Add your Razorpay API keys to the `.env` file
3. Test the payment flow using Razorpay test cards

## Development

- The application follows a modular architecture with separate apps for products, orders, and stores
- Templates use a component-based approach for reusability
- Theme system uses CSS variables and Tailwind's dark mode
- React is used for interactive components like the homepage builder
- Alpine.js is used for lightweight interactions
- Form validation combines HTML5 validation with JavaScript for enhanced user experience