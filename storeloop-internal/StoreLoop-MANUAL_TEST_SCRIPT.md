# 🎬 StoreLoop Manual Test Script - Indian Artisan Platform

**Purpose:** Complete testing for StoreLoop's Indian artisan and NGO features including Hindi UI, AI descriptions, WhatsApp notifications, GST compliance, and automated testing

**Latest Updates:**
- ✅ 48 Playwright automated tests with 45-second timeouts
- ✅ 1-click deployment with deploy.bat/deploy.sh
- ✅ Multi-browser testing (Chrome, Firefox, Safari, Mobile)
- ✅ Enhanced Hindi Unicode support and authentication fixes

---

## 🚀 Pre-Recording Setup

### **Environment Preparation**

**Option A: 1-Click Deployment (Recommended)**
```bash
# Windows
deploy.bat

# Linux/Mac
chmod +x deploy.sh && ./deploy.sh
```

**Option B: Manual Setup**
```bash
# 1. Start servers
# Docker (recommended)
docker run -d --name storeloop-postgres -e POSTGRES_DB=storeloop -e POSTGRES_PASSWORD=postgres -p 5434:5432 postgres:latest
docker run -d --name storeloop-redis -p 6379:6379 redis:7-alpine

# Option B: Local PostgreSQL (if you have it installed)
# Make sure PostgreSQL service is running and create database:
# createdb storeloop
# Redis still needs Docker: docker run -d --name storeloop-redis -p 6379:6379 redis:7-alpine

# 2. Install dependencies and setup environment
cd /path/to/storeloop
source storeloop-venv/bin/activate  # Windows: storeloop-venv\Scripts\activate
# Windows: Install numpy and pandas binaries first to avoid build issues
pip install numpy pandas --only-binary=all
pip install python-dotenv django-tailwind
# Create .env file for PostgreSQL
echo "USE_SQLITE=False" > .env
echo "DB_NAME=storeloop" >> .env
echo "DB_USER=postgres" >> .env
echo "DB_PASSWORD=your_postgres_password" >> .env

# 3. Recreate migrations folders (if deleted)
mkdir stores\migrations products\migrations orders\migrations  # Windows
# mkdir -p stores/migrations products/migrations orders/migrations  # Linux/Mac
echo. > stores\migrations\__init__.py  # Windows
echo. > products\migrations\__init__.py
echo. > orders\migrations\__init__.py
# touch stores/migrations/__init__.py products/migrations/__init__.py orders/migrations/__init__.py  # Linux/Mac

# 4. Complete database reset (stop Django first)
# Stop Django server (Ctrl+C)
docker exec -it storeloop-postgres psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'storeloop';"
docker exec -it storeloop-postgres psql -U postgres -c "DROP DATABASE storeloop;"
docker exec -it storeloop-postgres psql -U postgres -c "CREATE DATABASE storeloop;"

# 5. Create fresh migrations and apply
python manage.py makemigrations
python manage.py migrate --fake-initial

# 5. Create admin users using interactive shell
python manage.py shell
# In the shell, run these commands:
# from django.contrib.auth.models import User
# User.objects.all()  # Check existing users
# User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
# exit()

# 5. Start Celery worker (separate terminal)
# Make sure you're in the project root directory and Redis is running
celery -A core worker --loglevel=info

# 6. Start Django server (separate terminal)
python manage.py runserver

# 7. Ensure sample data exists
python manage.py seed_sample_data --users 2 --stores 3 --products 8

# 8. Create NGO partner admin
echo "from django.contrib.auth.models import User; from stores.models import SellerProfile; User.objects.filter(username='ngo_admin').delete(); user = User.objects.create_user('ngo_admin', 'ngo@example.com', 'password'); SellerProfile.objects.create(user=user, is_partner_admin=True, language_preference='hi'); print('NGO admin created successfully')" | python manage.py shell

# 9. Clean browser cache and prepare recording
```

### **Test Data Ready**

- **Admin User:** admin / admin123
- **NGO Partner Admin:** ngo_admin / password
- **Sample Stores:** 3 artisan stores with Hindi names
- **Sample Products:** 8 handcraft products with AI descriptions
- **Payment:** Razorpay test mode enabled
- **WhatsApp:** Stub notifications enabled
- **AI API:** OpenRouter/Groq configured (optional)

---

## 📋 Manual Test Scenarios (For Loom Demo)

### **Scenario 1: 5-Step Seller Onboarding Wizard (Demo: 0:45-1:15)**

#### **Test Steps:**

1. **Login and Start Onboarding Wizard**

   - Navigate to `http://localhost:8000/accounts/login/`
   - Login as seller: `admin` / `admin123`
   - Navigate to `http://localhost:8000/stores/onboarding/`
   - **Expected:** Step 1 - Logo & Basic Info loads

2. **Step 1: Basic Information**

   - **Name:** "कलाकार शिल्प" (Kalakar Shilp)
   - **Description:** "Handmade crafts by Indian artisans"
   - **Upload Logo:** Sample artisan logo
   - Click "Next"

3. **Step 2: Theme Selection**

   - **Select Theme:** "Warm"
   - **Primary Color:** #8B4513 (brown)
   - **Secondary Color:** #DEB887 (tan)
   - **Font Family:** "Serif"
   - Click "Next"

4. **Step 3: Homepage Layout**

   - **Expected:** Shows homepage block options
   - **Select blocks:** Hero Banner, Featured Products, About Section
   - **Customize:** Edit titles and content
   - Click "Next"

5. **Step 4: Sample Products**

   - **Expected:** Auto-creates 2 sample products
   - Click "Next"

6. **Step 5: Payment & GST Setup**

   - **Razorpay Key ID:** Test key
   - **GST Number:** 27AAPFU0939F1ZV
   - **Business Address:** Sample address
   - Click "Complete Setup"

7. **Verify Subdomain**
   - Navigate to `http://kalakar-shilp.storeloop.in:8000/`
   - **Expected:** Store loads with custom branding and homepage blocks

#### **Success Criteria:**

- ✅ Store created successfully
- ✅ Custom URL accessible
- ✅ Logo displays correctly
- ✅ Store name appears in navigation
- ✅ Homepage blocks display correctly
- ✅ Hero banner shows custom content

---

### **Scenario 2: Excel/CSV Product Upload with AI Descriptions (Demo: 1:15-1:45)**

#### **Test Steps:**

1. **Access Product Upload**

   - Navigate to `http://localhost:8000/stores/products/upload/`
   - **Expected:** Upload interface loads

2. **Prepare CSV File**

   - Create CSV with columns: name, description, price, stock, category, material, region, style
   - **Sample data:**
     ```
     name,description,price,stock,category,material,region,style
     "बनारसी सिल्क साड़ी","Beautiful handwoven saree",15000,5,"Clothing","Silk","Varanasi","Traditional"
     "कशीदाकारी शाल","Embroidered woolen shawl",3500,10,"Accessories","Wool","Kashmir","Kashmiri"
     ```

3. **Upload and Validate**

   - Upload CSV file
   - **Expected:** Shows validation results
   - **Expected:** 2 products imported successfully

4. **Test AI Description Generator**
   - Go to Add Product page
   - **Product Name:** "मिट्टी का दीया"
   - **Material:** "Clay"
   - **Region:** "Khurja"
   - **Style:** "Traditional"
   - Click "Generate Hindi Description"
   - **Expected:** AI generates editable Hindi description
   - **Verify:** Description appears in text area (editable)
   - **Important:** User must review and edit before saving

#### **Success Criteria:**

- ✅ CSV upload processes correctly
- ✅ Row-level validation works
- ✅ AI generates Hindi descriptions
- ✅ Descriptions are editable drafts only
- ✅ No auto-publishing of AI content

---

### **Scenario 3: Mobile-First Seller Dashboard with Hindi UI (Demo: 1:45-2:15)**

#### **Test Steps:**

1. **Access Seller Dashboard**

   - Navigate to `http://localhost:8000/stores/dashboard/`
   - **Expected:** Mobile-first dashboard loads

2. **Test Language Toggle**

   - Click language dropdown
   - Select "हिंदी" (Hindi)
   - **Expected:** UI switches to Hindi
   - **Verify:** Navigation, buttons, labels in Hindi

3. **Test Mobile Responsiveness**

   - Open browser dev tools
   - Switch to mobile view (iPhone/Android)
   - **Expected:** Dashboard adapts to mobile screen
   - **Verify:** Touch-friendly buttons and navigation

4. **Check Analytics Dashboard**

   - **Expected:** Shows total orders, sales, pending orders
   - **Expected:** Chart.js graphs load
   - **Expected:** Low stock alerts visible

5. **Test PWA Installation**
   - **Expected:** "Install App" button appears
   - Click to test PWA installation prompt

#### **Success Criteria:**

- ✅ Hindi UI toggle works correctly
- ✅ Mobile-responsive design
- ✅ Analytics charts display
- ✅ PWA installation available
- ✅ Touch-friendly interface

---

### **Scenario 4: NGO Partner Admin Dashboard (Demo: 2:15-2:45)**

#### **Test Steps:**

1. **Login as NGO Partner Admin**

   - Login: `ngo_admin` / `password`
   - Navigate to `http://localhost:8000/stores/partner-dashboard/`
   - **Expected:** Partner admin dashboard loads

2. **View Managed Stores**

   - **Expected:** Shows all managed artisan stores
   - **Expected:** Aggregate metrics displayed
   - Total stores, artisans, revenue

3. **Switch Store View**

   - Select different store from dropdown
   - **Expected:** Dashboard switches to show store-specific metrics
   - **Expected:** Can view individual store performance

4. **Manage Artisan Stores**

   - **Expected:** Can access individual store settings
   - **Expected:** Can view orders for each store
   - **Expected:** Can help artisans with store management

5. **Test Hindi Interface**
   - Switch language to Hindi
   - **Expected:** Partner dashboard in Hindi
   - **Expected:** All NGO management features in Hindi

#### **Success Criteria:**

- ✅ NGO admin can manage multiple stores
- ✅ Store switching works correctly
- ✅ Aggregate metrics display
- ✅ Individual store access
- ✅ Hindi interface for NGO admins

---

### **Scenario 5: Automated Testing with Playwright (Demo: 2:45-3:00)**

#### **Test Steps:**

1. **Run Playwright Tests**
   ```bash
   cd tests
   npx playwright test --project=chromium
   ```
   - **Expected:** All 48 tests pass
   - **Expected:** Tests complete in under 2 minutes
   - **Expected:** No failures or timeouts

2. **View Test Report**
   ```bash
   npx playwright show-report
   ```
   - **Expected:** HTML report opens
   - **Expected:** All test categories show green
   - **Expected:** Screenshots and videos available for any failures

3. **Test Coverage Areas**
   - Authentication flows
   - Seller onboarding wizard
   - Product management
   - Dashboard functionality
   - NGO admin features
   - Buyer purchase flows

#### **Success Criteria:**

- ✅ All automated tests pass
- ✅ Test execution under 2 minutes
- ✅ Comprehensive coverage of key features
- ✅ Visual test report available
- ✅ No critical bugs detected

---

### **Scenario 6: Customer Registration & Multi-Address Management (Demo: 3:00-3:30)**

#### **Test Steps:**

1. **Customer Registration**
   - Navigate to `http://localhost:8000/accounts/register/`
   - Fill registration form:
     - Username: `test_customer`
     - Email: `customer@example.com`
     - Phone: `9876543210`
     - Street: `123 Test Street`
     - City: `Mumbai`
     - State: `Maharashtra`
     - PIN: `400001`
   - Click "Register"
   - **Expected:** Auto-login and redirect to stores

2. **Multi-Address Checkout**
   - Browse to any store and select a product
   - Click "Buy Now"
   - **Expected:** Checkout modal shows saved address
   - Select "Add new address"
   - Add different address:
     - Street: `456 Office Complex`
     - City: `Delhi`
     - State: `Delhi`
     - PIN: `110001`
   - Complete order

3. **Address Selection**
   - Place another order
   - **Expected:** Both addresses available for selection
   - Click different addresses to test selection
   - **Expected:** Visual feedback on selected address

#### **Success Criteria:**
- ✅ Customer registration with address fields
- ✅ Multiple addresses saved per customer
- ✅ Address selection during checkout
- ✅ Visual feedback for selected addresses
- ✅ Orders linked to specific addresses

### **Scenario 7: Complete Purchase Flow with WhatsApp & GST (Demo: 3:30-4:00)**

#### **Test Steps:**

1. **Browse Products on Subdomain**

   - Navigate to `http://kalakar-shilp.storeloop.in:8000/`
   - Click on "बनारसी सिल्क साड़ी" product
   - **Expected:** Product detail page loads

2. **Place Order**

   - Click "Buy Now"
   - **Fill customer details:**
     - Name: "Priya Sharma"
     - Email: "priya@example.com"
     - Phone: "+91 9876543210"
     - Address: "123 MG Road, Delhi, 110001"
   - Click "Proceed to Payment"

3. **Razorpay Payment with GST**

   - **Expected:** Razorpay modal opens
   - **Use test card:** 4111 1111 1111 1111
   - Complete payment
   - **Expected:** GST amount calculated and displayed

4. **WhatsApp Notifications**

   - **Expected:** WhatsApp notification sent to buyer (stub)
   - **Expected:** WhatsApp notification sent to seller (stub)
   - **Check console:** WhatsApp stub messages logged

5. **GST Invoice Generation**

   - Go to order detail page
   - Click "Download GST Invoice"
   - **Expected:** PDF invoice downloads
   - **Verify:** GST number, calculation, compliance format

6. **Order Status Update**
   - Change order status to "Shipped"
   - **Expected:** WhatsApp status update sent

#### **Success Criteria:**

- ✅ Subdomain store works correctly
- ✅ Payment with GST calculation
- ✅ WhatsApp notifications triggered
- ✅ GST invoice PDF generated
- ✅ Status update notifications
- ✅ Hindi product names display correctly

---

### **Scenario 8: Database Architecture & Migration Demo (Demo: 4:00-4:30)**

#### **Test Steps:**

1. **Show Database Schema**
   - Access Django admin at `http://localhost:8000/admin/`
   - Navigate to Users, UserAddress, and Orders
   - **Expected:** Proper foreign key relationships visible
   - Show User → UserAddress (one-to-many)
   - Show Order → UserAddress (many-to-one)

2. **Data Migration Verification**
   - Check existing orders have delivery_address foreign key
   - Verify UserAddress records created from old order data
   - **Expected:** No data loss during migration
   - **Expected:** Proper relational structure

3. **API Endpoints**
   - Test `/stores/api/customer-addresses/` endpoint
   - **Expected:** Returns user's addresses in JSON
   - **Expected:** Proper error handling for non-existent users

#### **Success Criteria:**
- ✅ Database relationships properly established
- ✅ Migration completed without data loss
- ✅ API endpoints return correct data
- ✅ Foreign key constraints working
- ✅ Data integrity maintained

### **Scenario 9: Analytics & Competitive Advantage Demo (Demo: 4:30-5:00)**

#### **Test Steps:**

1. **Seller Analytics Dashboard**

   - Navigate to analytics section
   - **Expected:** Chart.js graphs showing:
     - Monthly sales trends
     - Top-selling products
     - Customer demographics
   - **Expected:** Mobile-optimized charts

2. **Compare with Competitors**

   - **Demonstrate StoreLoop advantages:**
     - Zero transaction fees (vs Wix 2.9%)
     - Hindi UI support (vs English-only competitors)
     - Built-in GST compliance
     - WhatsApp integration
     - AI descriptions in local language
     - NGO multi-store management

3. **Test AI Form Testing (Optional)**
   ```bash
   cd tests/playwright
   npm run advanced-pipeline
   ```
   - **Expected:** Automated testing of all forms
   - **Expected:** Security validation passes
   - **Expected:** Hindi form testing works

#### **Success Criteria:**

- ✅ Analytics display correctly
- ✅ Mobile-optimized charts
- ✅ Competitive advantages clear
- ✅ AI testing validates Hindi forms
- ✅ Zero transaction fees demonstrated

---

## 🎯 Recording Checklist

### **Before Recording:**

- [ ] Redis server running
- [ ] Celery worker running
- [ ] Django server running on localhost:8000
- [ ] Sample artisan data seeded
- [ ] NGO partner admin created
- [ ] Hindi language files compiled
- [ ] WhatsApp stub notifications working
- [ ] AI API keys configured (optional)
- [ ] Browser cache cleared
- [ ] Test payment credentials ready
- [ ] Screen recording software configured
- [ ] Audio levels tested

### **During Recording:**

- [ ] Speak clearly and at moderate pace
- [ ] Highlight cursor movements
- [ ] Zoom in on important details
- [ ] Show mobile responsiveness
- [ ] Demonstrate real-time updates
- [ ] Keep energy high and engaging

### **Key Moments to Capture:**

- [ ] Customer registration with address fields
- [ ] Multi-address selection during checkout
- [ ] Address auto-fill for returning customers
- [ ] Database schema with foreign key relationships
- [ ] 4-step onboarding wizard flow
- [ ] Hindi UI toggle in action
- [ ] Excel/CSV bulk upload with validation
- [ ] AI description generation (editable drafts)
- [ ] NGO partner admin switching stores
- [ ] WhatsApp notification triggers
- [ ] GST invoice PDF download
- [ ] Mobile PWA installation prompt
- [ ] Subdomain store access
- [ ] Analytics charts in Hindi
- [ ] Place Order button visibility fix

### **Common Issues to Avoid:**

- [ ] Slow internet causing timeouts
- [ ] Payment gateway errors in demo mode
- [ ] Browser console errors visible
- [ ] Typos in form fields
- [ ] Audio/video sync issues

---

## 📱 Mobile Testing Verification

### **Responsive Design Check:**

1. **Open browser dev tools**
2. **Switch to mobile view (iPhone/Android)**
3. **Test all scenarios on mobile:**
   - Store homepage loads correctly
   - Product pages are touch-friendly
   - Checkout form works on mobile
   - Payment process mobile-optimized
   - Navigation menu responsive

### **Mobile Success Criteria:**

- ✅ All text readable without zooming
- ✅ Buttons large enough for touch
- ✅ Forms easy to fill on mobile
- ✅ Images scale appropriately
- ✅ Navigation menu collapses properly

---

**🎬 Ready to record a compelling demo showcasing StoreLoop's unique advantages for Indian artisans and NGOs - features that Wix, Shopify, and WooCommerce don't offer!**
