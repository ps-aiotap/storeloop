# StoreLoop Admin Guide - Multi-language E-commerce Platform

This guide explains how to use StoreLoop's features including seller onboarding, AI description assistance, notification systems, multi-language UI, multi-store management, and automated testing.

**Latest Updates:**
- ✅ 48 automated Playwright tests with 45-second timeouts
- ✅ 1-click deployment scripts (deploy.bat/deploy.sh)
- ✅ Enhanced Hindi language support with proper Unicode handling
- ✅ Fixed authentication fixtures and test robustness
- ✅ All browser testing enabled (Chrome, Firefox, Safari, Mobile)

## Table of Contents
- [Quick Start (1-Click Deployment)](#quick-start-1-click-deployment)
- [Automated Testing](#automated-testing)
- [Seller Onboarding Wizard](#seller-onboarding-wizard)
- [Mobile-First Seller Dashboard](#mobile-first-seller-dashboard)
- [NGO Partner Admin](#ngo-partner-admin)
- [Excel/CSV Product Upload](#excelcsv-product-upload)
- [AI Product Descriptions](#ai-product-descriptions)
- [WhatsApp Notifications](#whatsapp-notifications)
- [Hindi Language Support](#hindi-language-support)
- [Subdomain Management](#subdomain-management)
- [GST Invoice Generation](#gst-invoice-generation)
- [Analytics Dashboard](#analytics-dashboard)
- [Legacy Features](#legacy-features)

## Quick Start (1-Click Deployment)

### Windows
```bash
# Double-click or run:
deploy.bat
```

### Linux/Mac
```bash
chmod +x deploy.sh
./deploy.sh
```

**That's it!** Your StoreLoop instance will be running at `http://localhost:8000`

- **Admin Login:** admin / admin123
- **NGO Admin:** ngo_admin / password

## Automated Testing

### Running Playwright Tests
```bash
cd tests
npm install
npx playwright install
npx playwright test --project=chromium
npx playwright show-report
```

### Test Coverage (48 Tests)
- ✅ Authentication and authorization flows
- ✅ 4-step seller onboarding wizard
- ✅ Product management (CRUD operations)
- ✅ Dashboard functionality with Hindi UI
- ✅ NGO admin multi-store management
- ✅ Mobile responsiveness testing
- ✅ All browsers (Chrome, Firefox, Safari, Mobile)

### Test Configuration
- **Timeout:** 45 seconds per test
- **Browsers:** Chrome, Firefox, Safari, Mobile Chrome, Mobile Safari
- **Parallel Execution:** 6 workers
- **Reports:** HTML, JSON, JUnit formats

## Seller Onboarding Wizard

The 4-step onboarding wizard helps artisans set up their stores quickly without technical expertise.

### Starting the Onboarding Process

1. Create a user account and SellerProfile in Django admin
2. Navigate to `/stores/onboarding/`
3. Follow the 4-step wizard:

### Step 1: Logo & Basic Information
- **Store Name**: Enter in Hindi or English (e.g., "कलाकार शिल्प")
- **Description**: Brief description of products/services
- **Logo Upload**: Store logo (automatically resized)
- Click "Next" to proceed

### Step 2: Theme Selection
- **Theme**: Choose from Minimal, Warm, or Dark
- **Primary Color**: Brand color for buttons and accents
- **Secondary Color**: Supporting color for highlights
- **Font Family**: Sans-serif, Serif, or Monospace
- Preview changes in real-time
- Click "Next" to proceed

### Step 3: Sample Products
- System automatically creates 2 sample products
- Helps artisans understand product structure
- Can be edited or deleted later
- Click "Next" to proceed

### Step 4: Payment & GST Setup
- **Razorpay Key ID**: For payment processing
- **Razorpay Key Secret**: Secure payment key
- **GST Number**: For invoice generation (format: 27AAPFU0939F1ZV)
- **Business Address**: For GST invoices
- Click "Complete Setup" to finish

### Post-Onboarding
- Store is automatically published
- Subdomain created: `storename.storeloop.in`
- Seller can access dashboard at `/stores/dashboard/`

## Mobile-First Seller Dashboard

The dashboard is optimized for mobile devices, especially low-end Android phones commonly used by artisans.

### Dashboard Features

1. **Quick Stats Cards**
   - Total Orders
   - Total Sales (in ₹)
   - Pending Orders
   - Active Products

2. **Language Toggle**
   - Switch between Hindi and English
   - Preference saved in user profile
   - All UI elements translated

3. **Quick Actions**
   - Add Product (single product form)
   - Bulk Upload (Excel/CSV import)

4. **Recent Orders**
   - Last 5 orders with status
   - Click to view order details
   - Update order status

5. **Low Stock Alerts**
   - Products with stock ≤ 5
   - Helps prevent stockouts

6. **Sales Analytics**
   - Chart.js graphs
   - Monthly sales trends
   - Mobile-optimized charts

### PWA Installation
- Dashboard supports Progressive Web App installation
- "Install App" button appears on mobile browsers
- Works offline for basic functionality
- Perfect for artisans with limited internet

## NGO Partner Admin

NGOs can manage multiple artisan stores from a single dashboard.

### Setting Up Partner Admin

1. Create user account for NGO manager
2. In Django admin, create SellerProfile:
   - Set `is_partner_admin = True`
   - Add managed stores to `managed_stores` field

### Partner Dashboard Features

1. **Access**: `/stores/partner-dashboard/`
2. **Store Switching**: Dropdown to switch between managed stores
3. **Aggregate Metrics**:
   - Total stores managed
   - Total artisans
   - Combined revenue
4. **Individual Store Management**:
   - View store-specific metrics
   - Help artisans with orders
   - Monitor performance

### NGO Use Cases
- **Craft Cooperatives**: Manage multiple artisan members
- **Women's Self-Help Groups**: Support group members' stores
- **Rural Development NGOs**: Enable village artisans
- **Fair Trade Organizations**: Oversee certified producers

## Excel/CSV Product Upload

Bulk product import saves time for artisans with large catalogs.

### Preparing Upload File

**Required Columns**:
- `name`: Product name (Hindi/English)
- `description`: Detailed description
- `price`: Price in INR (numbers only)
- `stock`: Available quantity
- `category`: Product category
- `image_url`: URL to product image (optional)
- `material`: Material used (for AI descriptions)
- `region`: Origin region (for AI descriptions)
- `style`: Style/type (for AI descriptions)

**Sample CSV**:
```csv
name,description,price,stock,category,material,region,style
"बनारसी सिल्क साड़ी","Beautiful handwoven saree",15000,5,"Clothing","Silk","Varanasi","Traditional"
"कशीदाकारी शाल","Embroidered woolen shawl",3500,10,"Accessories","Wool","Kashmir","Kashmiri"
```

### Upload Process

1. Navigate to `/stores/products/upload/`
2. Select CSV or Excel file
3. Click "Upload"
4. System validates each row:
   - Checks required fields
   - Validates data types
   - Reports errors with row numbers
5. Successful products are imported
6. Error summary provided for failed rows

### Validation Features
- **Row-level validation**: Each row processed independently
- **Error reporting**: Specific error messages with row numbers
- **Partial success**: Valid rows imported even if some fail
- **Upload history**: Track previous uploads and results

## AI Product Descriptions

**Important**: AI provides editable draft suggestions only - never auto-publishes content. All AI-generated content requires manual review and approval.

### How It Works

1. **Input Fields**:
   - Product name
   - Material (e.g., "Silk", "Clay", "Wood")
   - Region (e.g., "Varanasi", "Kashmir", "Rajasthan")
   - Style (e.g., "Traditional", "Contemporary", "Handwoven")

2. **AI Processing**:
   - Uses OpenRouter or Groq API
   - Generates both Hindi and English descriptions
   - Creates short (50 words) and long (150 words) versions

3. **Human Review**:
   - Descriptions appear as editable draft suggestions in text areas
   - User must review, edit, and approve before saving
   - AI provides assistance only - human creativity and approval required

### Using AI Descriptions

1. In product form, fill basic details
2. Click "Generate English Description" or "Generate Hindi Description"
3. Wait for AI processing (shows loading indicator)
4. Review generated text in form fields
5. Edit descriptions as needed
6. Save product with human-approved content

### API Configuration

**OpenRouter Setup**:
```env
OPENROUTER_API_KEY=your_api_key
```

**Groq Setup**:
```env
GROQ_API_KEY=your_api_key
```

**Fallback**: If no API configured, system uses template-based descriptions.

## WhatsApp Notifications

Automatic WhatsApp messages keep buyers and sellers informed.

### Notification Types

1. **Order Confirmation** (to buyer):
   ```
   🛍️ Order Confirmation - Store Name
   
   Order ID: ORD-12345678
   Product: Product Name
   Quantity: 1
   Total: ₹1,500
   
   Thank you for your purchase!
   ```

2. **New Order Alert** (to seller):
   ```
   🔔 New Order Received!
   
   Order ID: ORD-12345678
   Customer: Customer Name
   Product: Product Name
   Amount: ₹1,500
   
   Please process this order.
   ```

3. **Status Updates** (to buyer):
   ```
   📦 Order Update - Store Name
   
   Order ID: ORD-12345678
   Status: Shipped
   
   Track your order for updates.
   ```

### WhatsApp API Options

**Option 1: Twilio WhatsApp**
```env
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_WHATSAPP_ENABLED=true
```

**Option 2: Gupshup WhatsApp**
```env
GUPSHUP_API_KEY=your_api_key
GUPSHUP_SOURCE_NUMBER=your_number
```

**Development**: Uses stub implementation that logs messages to console.

### Setting Up WhatsApp Numbers

1. **For Sellers**: Add WhatsApp number in SellerProfile
2. **For Buyers**: Collected during checkout process
3. **Format**: Include country code (+91 for India)

## Hindi Language Support

Complete Hindi UI support for artisans who prefer local language.

### Language Features

1. **Manual Toggle**: Users choose Hindi/English (no auto-detection)
2. **Complete Translation**: All UI elements, forms, messages
3. **Persistent Preference**: Choice saved in user profile
4. **Mixed Content**: Supports Hindi product names with English interface

### Setting Up Hindi

1. **Django i18n Configuration**:
   ```python
   LANGUAGES = [
       ('en', 'English'),
       ('hi', 'हिंदी'),
   ]
   ```

2. **Compile Translation Files**:
   ```bash
   python manage.py compilemessages
   ```

3. **Language Toggle**: Available in dashboard header

### Translation Coverage

- ✅ Seller dashboard
- ✅ Product forms
- ✅ Order management
- ✅ Analytics labels
- ✅ Error messages
- ✅ Email notifications
- ✅ WhatsApp messages

## Subdomain Management

Each store gets its own subdomain for professional appearance.

### Subdomain Features

1. **Automatic Creation**: `storename.storeloop.in`
2. **Custom Domains**: Map `customdomain.com` (optional)
3. **SSL Support**: Automatic HTTPS for subdomains
4. **SEO Friendly**: Each store has unique URL

### DNS Configuration

**For Subdomains**:
- Wildcard DNS: `*.storeloop.in` → Server IP
- Automatic SSL via Let's Encrypt

**For Custom Domains**:
1. Customer adds CNAME: `www.customdomain.com` → `storeloop.in`
2. Add domain in store settings
3. SSL certificate auto-generated

### Middleware Routing

```python
# stores/middleware.py
class SubdomainMiddleware:
    def process_request(self, request):
        store = get_store_from_domain(request)
        if store:
            request.store = store
            return render_store_frontend(request, store)
```

## GST Invoice Generation

Automatic GST-compliant invoices for Indian tax requirements.

### GST Features

1. **Automatic Calculation**: 18% GST rate (configurable)
2. **PDF Generation**: WeasyPrint for professional invoices
3. **Compliance**: Follows Indian GST invoice format
4. **Download**: Per-order PDF download

### Invoice Components

- **Seller Details**: Name, GST number, address
- **Buyer Details**: Name, address, phone
- **Product Details**: Name, quantity, rate, amount
- **Tax Calculation**: Base amount, GST amount, total
- **Invoice Number**: Auto-generated unique number

### Setting Up GST

1. **Seller GST Profile**:
   - GST Number (format: 27AAPFU0939F1ZV)
   - Business Address
   - Legal Business Name

2. **Invoice Generation**:
   - Automatic on order completion
   - Manual download from order detail page
   - Email attachment (optional)

### Sample Invoice Format

```
TAX INVOICE

From: Store Name
GST No: 27AAPFU0939F1ZV
Address: Business Address

To: Customer Name
Address: Customer Address

Invoice No: INV-ORD-12345678
Date: 15/01/2024

Product: Banarasi Silk Saree
Quantity: 1
Rate: ₹12,711.86
Amount: ₹12,711.86

Taxable Amount: ₹12,711.86
GST @ 18%: ₹2,288.14
Total Amount: ₹15,000.00
```

## Analytics Dashboard

Mobile-optimized analytics for artisan business insights.

### Analytics Features

1. **Sales Trends**: Monthly revenue charts
2. **Top Products**: Best-selling items
3. **Customer Analytics**: Demographics and behavior
4. **Mobile Charts**: Chart.js optimized for small screens
5. **Hindi Labels**: Analytics in local language

### API Endpoints

```javascript
// /stores/api/analytics/
{
  "monthly_sales": {
    "2024-01": 45000,
    "2024-02": 52000
  },
  "top_products": {
    "Banarasi Saree": 15,
    "Kashmir Shawl": 12
  },
  "total_orders": 127,
  "total_revenue": 234000
}
```

### Using Analytics

1. **Identify Trends**: Which months are best for sales
2. **Popular Products**: Focus marketing on top sellers
3. **Inventory Planning**: Stock popular items
4. **Pricing Strategy**: Analyze price vs. sales volume

## Legacy Features

### Creating Tag Types

1. Navigate to **Admin > Products > Tag Types**
2. Click **Add Tag Type**
3. Enter a name (e.g., "Occasion", "Lifestyle", "Festival")
4. Save the tag type

### Creating Tags

1. Navigate to **Admin > Products > Tags**
2. Click **Add Tag**
3. Select the tag type (e.g., "Occasion")
4. Enter a name (e.g., "Wedding", "Birthday")
5. Add a description (optional)
6. Add SEO metadata (optional)
7. Save the tag

### Assigning Tags to Products

1. Navigate to **Admin > Products > Products**
2. Select a product to edit
3. In the Tags section, select the relevant tags
4. Save the product

## Product Bundles

Bundles allow you to group multiple products together and sell them as a single unit.

### Creating a Bundle

1. Navigate to **Admin > Products > Bundles**
2. Click **Add Bundle**
3. Enter bundle details:
   - Name
   - Description
   - Price (this can be different from the sum of individual product prices)
   - Store
   - Image (optional)
4. Save the bundle

### Adding Products to a Bundle

1. In the bundle edit page, scroll to the **Bundle Items** section
2. Click **Add another Bundle Item**
3. Select a product
4. Set the quantity
5. Repeat for each product in the bundle
6. Save the bundle

### How Bundles Work

- When a bundle is purchased, inventory is deducted from each individual product
- The available stock of a bundle is limited by the product with the lowest stock (relative to its quantity in the bundle)
- Bundles can be tagged just like regular products

## Homepage Builder

The Homepage Builder allows you to create dynamic, customizable homepages for each store.

### Accessing the Homepage Builder

1. Navigate to `/stores/{store_slug}/homepage/editor/`
2. Or go to **Admin > Stores > Stores**, select your store, and click the "Edit Homepage" button

### Adding Blocks

1. In the Homepage Builder, click the "Add Block" button
2. Select a block type:
   - Hero Banner
   - Product Grid
   - Featured Products
   - Testimonials
   - Text Block
   - Image Gallery
   - Video Embed
   - Trust Badges
   - Contact Form
   - Tag Collection
3. Configure the block settings in the right panel
4. Click "Save Block"

### Reordering Blocks

1. Drag and drop blocks to change their order
2. Click "Save Layout" to save the new order

### Enabling/Disabling Blocks

1. Toggle the visibility switch on any block
2. Disabled blocks remain in the layout but aren't displayed on the homepage

## Trust Badges

Trust badges help build customer confidence by displaying certifications, guarantees, or other trust indicators.

### Creating Trust Badges

1. Navigate to **Admin > Products > Trust Badges**
2. Click **Add Trust Badge**
3. Enter a name (e.g., "Secure Payments", "30-Day Returns")
4. Add a description (optional)
5. Upload an icon image
6. Select the store
7. Save the trust badge

### Displaying Trust Badges

Trust badges can be displayed in two ways:
1. **Homepage Block**: Add a Trust Badges block in the Homepage Builder
2. **Product Pages**: Trust badges are automatically displayed on product detail pages

## Static Pages

Static pages allow you to create content like About Us, FAQ, or Terms of Service.

### Creating a Static Page

1. Navigate to **Admin > Products > Static Pages**
2. Click **Add Static Page**
3. Enter page details:
   - Title
   - Content (supports HTML formatting)
   - Store
   - SEO metadata (optional)
4. Toggle "Is Published" to control visibility
5. Save the page

### Accessing Static Pages

Static pages are available at `/stores/{store_slug}/pages/{page_slug}/`

## Contact Forms

Contact forms allow customers to send inquiries directly from your store.

### Creating a Contact Form

1. Navigate to **Admin > Products > Contact Forms**
2. Click **Add Contact Form**
3. Configure form settings:
   - Title
   - Email to receive submissions
   - Success message
   - Field options (show phone, show subject)
   - WhatsApp number (optional)
   - Newsletter integration toggle
4. Save the form

### Adding a Contact Form to Homepage

1. In the Homepage Builder, add a "Contact Form" block
2. Select your contact form from the dropdown
3. Configure display options
4. Save the block

## Analytics Dashboard

The Analytics Dashboard provides insights into store performance.

### Accessing the Dashboard

Navigate to `/dashboard/analytics/` when logged in as a store owner

### Dashboard Features

1. **Product Views**: Chart showing views over time
2. **Top Products**: List of most-viewed products
3. **Tag Performance**: Analytics on which tags drive the most views
4. **Time Range**: Filter data by different time periods (7, 30, 90 days)

### Using Analytics for Decision Making

- Identify popular products for featuring on your homepage
- Discover which tags perform best to optimize your categorization
- Track the impact of marketing campaigns on product views