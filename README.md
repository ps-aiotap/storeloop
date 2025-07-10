# 🛍️ StoreLoop - Indian Artisan E-commerce Platform

**Zero transaction fees • Hindi/English UI • AI descriptions • WhatsApp integration • GST compliance**

StoreLoop is a specialized e-commerce platform designed for Indian artisans and NGOs, offering a comprehensive solution with language toggle, multi-address checkout, AI-generated product descriptions, WhatsApp integration, and GST compliance - features that mainstream platforms like Wix, Shopify, and WooCommerce don't provide for the unique needs of Indian sellers.

## 🎬 Demo Video

[Watch StoreLoop Demo Video](https://youtu.be/demo-link) - See the platform in action!

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
- **5-step onboarding wizard** with full language toggle (Hindi/English)
- **Zero transaction fees** (vs 2.9% on Wix/Shopify)
- **AI-generated product descriptions** in Hindi and English using OpenAI
- **GST compliance** with automatic invoice generation
- **WhatsApp notifications** for orders and updates
- **Mobile-first PWA** design for smartphone users
- **Customer management** with multi-address support
- **Smart checkout** with saved address selection
- **SEO-optimized product pages** for better discoverability

### 🏢 **For NGO Partners**
- **Multi-store management** dashboard
- **Aggregate analytics** across all managed stores
- **Artisan support tools** and training resources
- **Full language toggle** for local NGO staff
- **Store performance comparison** and insights
- **Bulk product management** tools

### 🛒 **For Customers**
- **User registration** with address management
- **Multiple delivery addresses** per customer
- **Smart address selection** during checkout
- **Order history** and tracking
- **Guest checkout** option available
- **Auto-fill** customer details for returning users
- **WhatsApp ordering** option

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

## 🛠️ Setup Instructions

### Local Development

```bash
# Clone repository
git clone <repository-url>
cd storeloop

# Create virtual environment
python -m venv storeloop-venv
source storeloop-venv/bin/activate  # Windows: storeloop-venv\Scripts\activate
pip install -r requirements.txt

# Setup database (SQLite for development)
echo "USE_SQLITE=True" > .env
python manage.py migrate
python manage.py reset_admin
python manage.py seed_sample_data --users 2 --stores 3 --products 8

# Run server
python manage.py runserver
```

### Production Deployment

```bash
# Setup environment
cp .env.example .env
# Edit .env with production settings

# Start services
docker-compose up -d

# Apply migrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

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

## 📱 WhatsApp Integration

StoreLoop includes a WhatsApp bot for product sharing and ordering:

1. **Setup WhatsApp Business API** in `.env`
2. **Start the WhatsApp service:** `python manage.py start_whatsapp_bot`
3. **Test with demo number:** Send "Hello" to +91-DEMO-NUMBER

Customers can:
- Browse products via WhatsApp
- Place orders directly in chat
- Receive order confirmations and updates
- Track shipments

## 🏗️ Architecture

```
StoreLoop/
├── core/                 # Django project settings & user management
├── stores/               # Store management & customer addresses
├── products/             # Product catalog app
├── orders/               # Order processing with address linking
├── whatsapp/             # WhatsApp integration service
├── templates/            # HTML templates with smart checkout
│   ├── accounts/         # Login/registration templates
│   └── stores/           # Store and checkout templates
├── static/               # CSS, JS, images
├── tests/                # Playwright test suite
├── deploy.bat            # Windows 1-click deployment
├── deploy.sh             # Linux/Mac 1-click deployment
└── requirements.txt      # Python dependencies
```

## 🌟 Competitive Advantages

| Feature | StoreLoop | Wix | Shopify | WooCommerce |
|---------|-----------|-----|---------|-------------|
| Transaction Fees | **0%** | 2.9% | 2.9% | 2.9% |
| Hindi/English Toggle | ✅ | ❌ | ❌ | ❌ |
| AI Product Descriptions | ✅ | ❌ | ❌ | ❌ |
| GST Compliance | ✅ | ❌ | ❌ | ❌ |
| WhatsApp Integration | ✅ | ❌ | ❌ | ❌ |
| NGO Multi-Store | ✅ | ❌ | ❌ | ❌ |
| Multi-Address Management | ✅ | ❌ | ❌ | ❌ |
| Smart Checkout | ✅ | ❌ | ❌ | ❌ |
| Mobile-First PWA | ✅ | Partial | Partial | Partial |
| Automated Testing | ✅ | ❌ | ❌ | ❌ |
| SEO Optimization | ✅ | Partial | Partial | Partial |

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

# OpenAI API (for AI descriptions)
OPENAI_API_KEY=your-api-key

# WhatsApp Business API
WHATSAPP_API_TOKEN=your-token
WHATSAPP_PHONE_ID=your-phone-id
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

- **Documentation:** See the docs/ directory
- **Issues:** Create a GitHub issue
- **Email:** support@storeloop.in

---

**🎯 Built specifically for Indian artisans and NGOs - features that global platforms don't offer!**