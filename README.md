# StoreLoop

StoreLoop is a Django-based e-commerce platform with multi-seller and theme support.

## Features

- Product catalog with images, descriptions, and pricing
- Order processing with Razorpay integration
- QR code generation for products (for easy sharing/scanning)
- Multi-seller support with per-store theming
- Customizable themes per seller (Minimal, Warm, Dark)
- Enhanced product cards with hover effects and animations
- Responsive, mobile-friendly design
- Tailwind CSS for modern styling

## Theme System

StoreLoop supports customizable themes for each seller's store:

- **Theme Options**: Minimal, Warm, and Dark
- **Customization**: Primary color, font style, and store logo
- **Dynamic Templates**: Templates adapt based on the selected theme
- **Interactive UI**: Hover effects and animations enhance user experience

## Product Features

- Product images with hover-to-zoom effects
- Product details with descriptions and pricing
- QR codes for easy product sharing
- Categorization and organization options
- Interactive product cards with visual feedback

## Setup

1. Create a virtual environment and install dependencies from requirements.txt
2. Create a .env file based on .env.example
3. Run migrations and create a superuser
4. Run the development server

## Theme Configuration

1. Create a Store in the admin interface
2. Navigate to `/stores/store/{store_id}/theme/` to configure the theme
3. Choose from Minimal, Warm, or Dark themes
4. Select a primary color and font style
5. Upload a store logo

## Development

- Built with Django 4.2 LTS
- Uses Tailwind CSS for styling
- Includes QR code generation for products
- Mobile-first responsive design
- Modular architecture for easy extension