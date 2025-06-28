# Changelog

## v2.0.0 (2024-01-15) - Enhanced Multi-language Platform

### 🎯 Major Features Added

- **4-Step Seller Onboarding Wizard**
  - Logo upload → Theme selection → Sample products → Razorpay/GST setup
  - Preview before publish functionality
  - Store configuration saved in seller profile

- **Mobile-First Seller Dashboard**
  - PWA-ready for low-end Android devices
  - Product and Order CRUD operations
  - Real-time inventory tracking with low stock alerts
  - Order status updates with WhatsApp integration
  - Chart.js analytics with mobile optimization

- **NGO/Partner Admin Role**
  - `partner_admin` role for NGO managers
  - Multi-store management from single dashboard
  - Switch between seller views
  - Aggregate metrics across managed stores

- **Excel/CSV Product Upload**
  - Bulk import with pandas/openpyxl processing
  - Row-level validation with detailed error summary
  - Support for .xlsx and .csv formats
  - Fields: name, description, price, stock, category, image_url, material, region, style

- **AI Product Description Generator**
  - OpenRouter/Groq API integration
  - Hindi and English description generation
  - **Editable draft suggestions only** - provides suggestions for manual review
  - Input: product name, material, region, style
  - Output: draft descriptions requiring human approval before use
  - **No automatic publishing** - all AI content must be manually reviewed and edited

- **WhatsApp Notifications**
  - Order confirmation to buyers
  - New order alerts to sellers
  - Status update notifications
  - Supports Twilio and Gupshup APIs
  - Celery async delivery

- **Hindi Language UI Support**
  - Complete Django i18n implementation
  - Manual Hindi/English toggle (no auto-detection)
  - Seller dashboard fully translated
  - Product forms and admin interface in Hindi

- **Subdomain & Custom Domain Routing**
  - `artisanname.storeloop.in` for each seller
  - Custom domain mapping support
  - Django middleware-based routing
  - DNS configuration guidance

- **GST Invoice PDF Generation**
  - Automatic GST calculation (18% rate)
  - WeasyPrint PDF generation
  - Seller GST profile integration
  - Downloadable invoices per order
  - Compliance with Indian tax requirements

- **Enhanced Analytics**
  - Monthly sales trends with Chart.js
  - Top-selling products analysis
  - Customer demographics
  - DRF API endpoints for real-time data
  - Mobile-optimized charts

### 🏗️ Technical Improvements

- **Django REST Framework** integration for APIs
- **Celery + Redis** for background task processing
- **Pandas/openpyxl** for Excel file processing
- **WeasyPrint** for PDF invoice generation
- **Django i18n** for Hindi/English localization
- **Subdomain middleware** for multi-tenant routing
- **Enhanced security** with proper validation

### 🆚 Technical Highlights

- Multi-language UI implementation with Django i18n
- Integrated payment processing with Indian compliance
- Real-time notification system via WhatsApp APIs
- AI integration for content assistance (draft suggestions)
- Multi-tenant architecture with subdomain routing
- Progressive Web App capabilities
- Comprehensive automated testing framework

## v0.1.0 (2023-06-15) - Initial Release

### Features

- **Multi-seller Architecture**
  - Store model with name, slug, and logo
  - Products linked to stores via ForeignKey
  - Store-specific product listings
  - Admin restrictions for sellers to access only their data

- **Theme System**
  - Three built-in themes: Minimal, Warm, and Dark
  - Customizable primary color and font family
  - Store logo upload
  - Versioned theme templates to prevent upgrade conflicts
  - Custom CSS/JS injection for store owners

- **Product Management**
  - Product listings with images and descriptions
  - Product detail pages
  - Automatic QR code generation for products
  - Related products display

- **Payment Integration**
  - Razorpay payment gateway integration
  - Order creation and management
  - Payment success handling
  - Order confirmation

- **Plugin System**
  - Extensible plugin architecture
  - Support for custom payment providers
  - Support for custom shipping providers
  - Basic shipping provider implementation

- **Security**
  - CSRF protection
  - XSS prevention
  - Content Security Policy
  - HTTPS enforcement
  - Secure headers

### Known Limitations

- Limited payment gateway options (Razorpay only)
- No product categories or tags
- No user account management for customers
- No shopping cart functionality (single product checkout only)
- Limited reporting and analytics
- No inventory management
- No multi-currency support
- No tax calculation
- No shipping integration beyond the basic plugin

### Technical Debt

- Needs more comprehensive test coverage
- Needs better error handling for payment failures
- Plugin system needs more documentation
- Theme customization could be more user-friendly

### Next Steps

- Add product categories and filtering
- Implement shopping cart functionality
- Add user account management for customers
- Integrate more payment gateways
- Add inventory management
- Implement reporting and analytics
- Add multi-currency support
- Improve mobile responsiveness