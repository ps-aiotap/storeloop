# 🛍️ StoreLoop — Indian Artisan E-commerce Platform

![StoreLoop Screenshot](https://github.com/user-attachments/assets/c5f5ae01-d2a4-437b-81f2-0b6cf9702618)

**Zero transaction fees • Hindi/English UI • AI descriptions • WhatsApp integration • GST compliance**

StoreLoop is a userless, microservices-friendly e-commerce platform designed specifically for Indian artisans, NGOs, and community sellers. It delivers a complete, opinionated solution to common local challenges: multilingual interfaces, GST invoicing, multi-address delivery, AI-assisted product management, and native WhatsApp integration. Unlike Shopify, WooCommerce, or Wix, StoreLoop deeply localizes e-commerce for Indian realities.

---

## 🎬 Demo Video

[Watch StoreLoop Demo Video](https://youtu.be/demo-link) - See the platform in action!

## 🎥 Quick Walkthrough

Loom video: [StoreLoop Demo on Loom](https://www.loom.com/share/795ebe98fa57463880091cb22868f6e7?sid=cc3a45ce-d68e-4a6b-85e6-8e4c9bee82c4)

Covered in the demo:

* The unique needs of Indian artisans and NGOs
* What makes StoreLoop different from global platforms
* Key tech insights into its userless identity architecture

---

## 🌟 Feature Highlights

* **Hindi + English Interface**
* **AI-generated product descriptions**
* **Multi-address checkout system**
* **WhatsApp integration** (for orders & tracking)
* **GST-compliant invoice generation**
* **No transaction fees or platform cuts**
* **Dashboard for NGOs with sub-store support**
* **Stateless, userless backend via AT Identity integration**

---

## 🚀 Architecture Overview

```
┌─────────────┐    HTTP API    ┌─────────────┐    HTTP API    ┌─────────────┐
│  StoreLoop  │◄──────────────►│ AT Identity │◄──────────────►│ Artisan CRM │
│             │                │   Service   │                │             │
│ NO USERS    │                │ Master User │                │ NO USERS    │
│ user_id INT │                │ Management  │                │ user_id INT │
└─────────────┘                └─────────────┘                └─────────────┘
```

### 🚫 What’s Removed

* Django auth, admin, and all user FKs
* Local user session/state logic

### ✅ What’s Added

* Stateless `ATIdentityUser` proxy from remote auth service
* API-only authentication & permission decorators
* Lightweight, microservice-compatible user handling

---

## 🚀 Quick Start (1-Click Dev Deployment)

### Windows

```bash
# Double-click or run:
start_dev.bat
```

### Mac/Linux

```bash
./start_dev.sh
```

### Manual Start

1. **Start AT Identity (Port 8001)**

```bash
cd at_identity_project
python manage.py runserver 8001
```

2. **Start StoreLoop (Port 8000)**

```bash
cd storeloop
python manage.py runserver 8000
```

3. **Login Test**
   Visit: [http://localhost:8000/login/](http://localhost:8000/login/)

---

## 📊 Userless DB Schema (Before vs After)

| Before (User FK)           | After (Userless)                             |
| -------------------------- | -------------------------------------------- |
| `owner = ForeignKey(User)` | `owner_id = IntegerField()`                  |
|                            | `owner_username = CharField(max_length=150)` |

---

## 🔧 Project Structure

```
StoreLoop/
├── at_identity/              # Identity service integration
│   └── auth/                 # Backends, middleware, proxy user
├── stores/                  # Store logic, models, views
├── templates/               # Jinja2-based HTML templates
└── core/                    # Minimal Django settings
```

---

## 📝 Auth & Permissions Flow

**Login Flow:**

1. Frontend calls AT Identity login API
2. Identity service returns auth payload
3. StoreLoop uses proxy object + stores minimal session info

**Permissions:**

1. `@at_permission_required` decorators check access
2. AT Identity validates and responds via API

---

## 📅 Roadmap (Upcoming Features)

* NGO donation module (via UPI)
* Inventory alerts
* Storefront theming system

---

## 👪 Who It’s For

* 🇮🇳 Indian artisans selling offline or via WhatsApp
* 🧵 NGO initiatives running community crafts
* 🛍️ Solo or collective makers needing plug-n-play web presence

---

## 🚫 Not Another Shopify Clone

StoreLoop is not built for general-purpose global e-commerce. It’s purpose-built for Indian small sellers who:

* Need Hindi-first UI
* Want GST invoices without plugins
* Can’t pay monthly SaaS fees
* Use WhatsApp for all order comms

---

## 🔎 Explore More

* Full code walkthrough on [Loom](https://www.loom.com/share/795ebe98fa57463880091cb22868f6e7)
* Deployment guide coming soon
* Homepage screenshot: *To be updated here*

---

## 🚑 Support / Contributions

* Raise GitHub Issues for bugs or feature ideas
* Contributions welcome for regional language support, NGO reporting

---

### ✨ StoreLoop — Zero friction. Zero fees. 100% made for India.
