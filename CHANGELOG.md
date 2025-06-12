# Changelog

## v0.1.0 (2023-06-15)

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