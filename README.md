# 🛍️ StoreLoop - Indian Artisan E-commerce Platform

**Zero transaction fees • Hindi UI • AI descriptions • WhatsApp integration • GST compliance**

StoreLoop is a specialized e-commerce platform designed for Indian artisans and NGOs, offering features that mainstream platforms like Wix, Shopify, and WooCommerce don't provide.

## 🎥 Quick Walkthrough

Watch a short Loom demo of StoreLoop in action:  
👉 [StoreLoop Demo on Loom](https://www.loom.com/share/795ebe98fa57463880091cb22868f6e7?sid=cc3a45ce-d68e-4a6b-85e6-8e4c9bee82c4)

This is what the quick walkthrough covers:
- The problem StoreLoop solves
- Key features
- How it’s built for Indian artisans and NGOs

## 🚀 Quick Start (1-Click Deployment)

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

## ✨ Key Features

### 🎯 **For Indian Artisans**
- **5-step onboarding wizard** with Hindi support
- **Zero transaction fees** (vs 2.9% on Wix/Shopify)
- **AI-generated Hindi product descriptions** (editable drafts)
- **GST compliance** with automatic invoice generation
- **WhatsApp notifications** for orders and updates
- **Mobile-first PWA** design for smartphone users
- **Customer management** with multi-address support
- **Smart checkout** with saved address selection

### 🏢 **For NGO Partners**
- **Multi-store management** dashboard
- **Aggregate analytics** across all managed stores
- **Artisan support tools** and training resources
- **Hindi interface** for local NGO staff
- **Store performance comparison** and insights

### 🛒 **For Customers**
- **User registration** with address management
- **Multiple delivery addresses** per customer
- **Smart address selection** during checkout
- **Order history** and tracking
- **Guest checkout** option available
- **Auto-fill** customer details for returning users

### 📱 **Technical Advantages**
- **Mobile-first responsive design**
- **Progressive Web App (PWA)** with offline support
- **Automated testing** with Playwright (48 test scenarios)
- **Excel/CSV bulk product upload** with validation
- **Custom subdomain** for each store
- **Real-time analytics** with Chart.js
- **Advanced database schema** with proper foreign key relationships
- **User authentication** with session management
- **Data migration tools** for address management

## 🛠️ Manual Setup (If needed)

<details>
<summary>Click to expand manual setup instructions</summary>

### Prerequisites
- Python 3.8+
- Docker (for PostgreSQL and Redis)
- Node.js 16+ (for Playwright tests)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd storeloop
python -m venv storeloop-venv
source storeloop-venv/bin/activate  # Windows: storeloop-venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start Services
```bash
# Start PostgreSQL and Redis
docker run -d --name storeloop-postgres -e POSTGRES_DB=storeloop -e POSTGRES_PASSWORD=postgres -p 5434:5432 postgres:latest
docker run -d --name storeloop-redis -p 6379:6379 redis:7-alpine

# Setup database
python manage.py makemigrations
python manage.py migrate
python manage.py reset_admin
python manage.py seed_sample_data --users 2 --stores 3 --products 8
```

### 3. Start Application
```bash
# Terminal 1: Celery worker
celery -A core worker --loglevel=info

# Terminal 2: Django server
python manage.py runserver
```

</details>

## 🧪 Testing

### Automated Testing (Playwright)
```bash
cd tests
npm install
npx playwright install
npx playwright test --project=chromium
npx playwright show-report
```

**Test Coverage:**
- ✅ 48 automated test scenarios
- ✅ Authentication and authorization
- ✅ Customer registration and login
- ✅ Multi-address management
- ✅ Seller onboarding wizard
- ✅ Product management (CRUD)
- ✅ Smart checkout process
- ✅ Dashboard functionality
- ✅ NGO admin features
- ✅ Mobile responsiveness

### Manual Testing
See [MANUAL_TEST_SCRIPT.md](internal/MANUAL_TEST_SCRIPT.md) for comprehensive testing scenarios including:
- Customer registration with address fields
- Multi-address selection during checkout
- 5-step seller onboarding
- Excel/CSV product upload
- Hindi UI testing
- NGO partner dashboard
- Complete purchase flow with quantity selection
- Address auto-fill for returning customers
- WhatsApp notifications
- GST invoice generation

## 🏗️ Architecture

```
StoreLoop/
├── core/                 # Django project settings & user management
├── stores/              # Store management & customer addresses
├── products/            # Product catalog app
├── orders/              # Order processing with address linking
├── templates/           # HTML templates with smart checkout
│   ├── accounts/        # Login/registration templates
│   └── stores/          # Store and checkout templates
├── static/              # CSS, JS, images
├── tests/               # Playwright test suite
├── internal/            # Documentation
├── deploy.bat           # Windows 1-click deployment
├── deploy.sh            # Linux/Mac 1-click deployment
└── requirements.txt     # Python dependencies
```

### Database Schema
- **User** → **UserAddress** (One-to-Many)
- **Order** → **UserAddress** (Many-to-One via foreign key)
- **Store** → **Product** (One-to-Many)
- **Store** → **Order** (One-to-Many)

## 🌟 Competitive Advantages

| Feature | StoreLoop | Wix | Shopify | WooCommerce |
|---------|-----------|-----|---------|-------------|
| Transaction Fees | **0%** | 2.9% | 2.9% | 2.9% |
| Hindi UI | ✅ | ❌ | ❌ | ❌ |
| AI Hindi Descriptions | ✅ | ❌ | ❌ | ❌ |
| GST Compliance | ✅ | ❌ | ❌ | ❌ |
| WhatsApp Integration | ✅ | ❌ | ❌ | ❌ |
| NGO Multi-Store | ✅ | ❌ | ❌ | ❌ |
| Multi-Address Management | ✅ | ❌ | ❌ | ❌ |
| Smart Checkout | ✅ | ❌ | ❌ | ❌ |
| Mobile-First PWA | ✅ | Partial | Partial | Partial |
| Automated Testing | ✅ | ❌ | ❌ | ❌ |

## 📊 Sample Data

The platform comes with pre-seeded sample data:

**Artisan Stores:**
- कलाकार शिल्प (Kalakar Shilp) - Traditional crafts
- हस्तकला भंडार (Hastkala Bhandar) - Handmade goods
- शिल्पी संग्रह (Shilpi Sangraha) - Artisan collection

**Products:**
- बनारसी सिल्क साड़ी (Banarasi Silk Saree)
- कशीदाकारी शाल (Kashmiri Embroidered Shawl)
- मिट्टी का दीया (Clay Diya)
- हस्तनिर्मित गहने (Handmade Jewelry)

## 🔧 Configuration

### Environment Variables (.env)
```bash
DEBUG=True
SECRET_KEY=your-secret-key
USE_SQLITE=False
DB_NAME=storeloop
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5434

# Razorpay (optional)
RAZORPAY_KEY_ID=your-key-id
RAZORPAY_KEY_SECRET=your-key-secret

# AI API (optional)
OPENROUTER_API_KEY=your-api-key
```

### Language Support
- English (default)
- हिंदी (Hindi) - Complete UI translation
- Extensible for other Indian languages

## 📱 Mobile PWA Features

- **Offline support** for browsing products
- **Add to home screen** functionality
- **Push notifications** for order updates
- **Touch-optimized** interface
- **Fast loading** with service workers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `npx playwright test`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation:** [internal/MANUAL_TEST_SCRIPT.md](internal/MANUAL_TEST_SCRIPT.md)
- **Issues:** Create a GitHub issue
- **Email:** support@storeloop.in

---

**🎯 Built specifically for Indian artisans and NGOs - features that global platforms don't offer!**
