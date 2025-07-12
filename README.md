# 🛍️ StoreLoop - Completely Userless E-commerce Platform

**Zero local users • AT Identity integration • API-first authentication • Microservices ready**

StoreLoop is now a **completely userless** e-commerce platform that delegates all user management to AT Identity service, enabling true microservices architecture with independent deployment.

## 🎯 Architecture Overview

```
┌─────────────┐    HTTP API    ┌─────────────┐    HTTP API    ┌─────────────┐
│  StoreLoop  │◄──────────────►│ AT Identity │◄──────────────►│ Artisan CRM │
│             │                │   Service   │                │             │
│ NO USERS    │                │ Master User │                │ NO USERS    │
│ user_id INT │                │ Management  │                │ user_id INT │
└─────────────┘                └─────────────┘                └─────────────┘
```

## ✨ Userless Features

### 🚫 **What's Removed**
- ❌ `django.contrib.auth` - Completely removed
- ❌ `django.contrib.admin` - No admin interface
- ❌ User model imports - Zero user dependencies
- ❌ User foreign keys - Replaced with `user_id` integers
- ❌ Local user database tables - No user storage

### ✅ **What's Added**
- ✅ `ATIdentityUser` proxy objects - Virtual users from API
- ✅ `UserlessATIdentityBackend` - API-based authentication
- ✅ `ATIdentityMiddleware` - Session management
- ✅ `@at_permission_required` - Permission decorators
- ✅ User ID synchronization - Integer-based relationships

## 🚀 Quick Start

### 1. Start AT Identity Service (Port 8001)
```bash
cd at_identity_project
python manage.py runserver 8001
```

### 2. Start StoreLoop (Port 8000)
```bash
cd storeloop
python manage.py runserver 8000
```

### 3. Test Userless Authentication
Visit: `http://localhost:8000/login/`

## 📊 Database Schema (Userless)

### Before (With Users)
```sql
CREATE TABLE stores_store (
    owner_id FOREIGN KEY REFERENCES auth_user(id)  -- Problem!
);
```

### After (Userless)
```sql
CREATE TABLE stores_store (
    owner_id INTEGER,           -- AT Identity user ID
    owner_username VARCHAR(150) -- Cached for display
);
```

## 🔧 Configuration

### StoreLoop Settings
```python
# Completely userless
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.sessions", 
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "stores",
]

# AT Identity integration
AUTHENTICATION_BACKENDS = [
    'at_identity.auth.backends_userless.UserlessATIdentityBackend',
]

AT_IDENTITY_URL = 'http://localhost:8001/api/'
APP_NAME = 'storeloop'
```

## 🧪 Testing

### Manual Testing
1. **Login Test**: `http://localhost:8000/login/`
2. **Dashboard Test**: `http://localhost:8000/dashboard/`
3. **Permission Test**: Try creating store without permission

### API Testing
```bash
# Test AT Identity authentication
curl -X POST http://localhost:8001/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test", "app_name": "storeloop"}'
```

## 📁 Project Structure

```
StoreLoop/
├── at_identity/              # AT Identity service components
│   ├── auth/                 # Userless authentication
│   │   ├── backends_userless.py
│   │   ├── middleware.py
│   │   ├── user_proxy.py
│   │   └── decorators.py
│   ├── api/                  # REST API endpoints
│   └── models.py             # AT Identity models
├── stores/                   # Userless store management
│   ├── models.py             # No User foreign keys
│   ├── views_userless.py     # API-based views
│   └── urls_userless.py      # Userless URL patterns
├── templates/                # Userless templates
└── core/                     # Minimal Django settings
```

## 🔄 Migration from User-based to Userless

### Phase 1: Remove Django Auth
```python
# Remove from INSTALLED_APPS
# 'django.contrib.auth',
# 'django.contrib.admin',
```

### Phase 2: Update Models
```python
# Before
owner = models.ForeignKey(User, on_delete=models.CASCADE)

# After  
owner_id = models.IntegerField()  # AT Identity user ID
owner_username = models.CharField(max_length=150)
```

### Phase 3: Update Views
```python
# Before
@login_required
def create_store(request):
    store = Store.objects.create(owner=request.user)

# After
@at_permission_required('store.create')
def create_store(request):
    store = Store.objects.create(
        owner_id=request.user.id,
        owner_username=request.user.username
    )
```

## 🌟 Benefits

### **True Independence**
- No shared database dependencies
- Independent deployment cycles
- Technology stack flexibility
- Microservices architecture ready

### **Simplified Architecture**
- No user synchronization needed
- No foreign key constraints
- Cleaner database schema
- API-first integration

### **Better Performance**
- No local user queries
- Cached user data where needed
- API calls only when necessary
- Stateless user management

## 🔗 Integration Points

### Authentication Flow
```
1. User login → AT Identity API
2. AT Identity validates → Returns user data
3. StoreLoop creates ATIdentityUser proxy
4. Session stores user_id only
5. Subsequent requests use cached data
```

### Permission Flow
```
1. View access → Check @at_permission_required
2. Decorator calls AT Identity API
3. AT Identity returns permissions
4. Allow/deny access based on response
```

## 📚 Documentation

- [Complete Architecture Guide](INDEPENDENT_APPS_GUIDE.md)
- [Plugin Integration Guide](PLUGIN_GUIDE.md)
- [Userless System Guide](USERLESS_GUIDE.md)
- [Step-by-Step Testing](TESTING_GUIDE.md)

## 🆘 Support

- **Issues**: Create GitHub issue
- **Architecture**: See integration guides
- **Testing**: Follow testing guide

---

**🎯 Completely userless - zero local user management, 100% AT Identity integration!**