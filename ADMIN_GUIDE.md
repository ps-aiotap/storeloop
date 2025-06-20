# StoreLoop Admin Guide

This guide explains how to use the various admin features in StoreLoop, including Bundles, Homepage Blocks, Trust Badges, and more.

## Table of Contents
- [Tag Management](#tag-management)
- [Product Bundles](#product-bundles)
- [Homepage Builder](#homepage-builder)
- [Trust Badges](#trust-badges)
- [Static Pages](#static-pages)
- [Contact Forms](#contact-forms)
- [Analytics Dashboard](#analytics-dashboard)

## Tag Management

Tags provide a flexible way to categorize products across different dimensions.

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