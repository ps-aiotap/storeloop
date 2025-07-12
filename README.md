# 🛍️ StoreLoop — Userless E-commerce Platform for Artisans & NGOs

> ✅ Zero local users · 🔐 AT Identity integration · ⚙️ Microservices-ready · 🌏 Built for Indian artisans, globally usable

**StoreLoop** is a modular, userless e-commerce engine designed for artisans, NGOs, and grassroots brands. It removes all user-related logic from Django and relies on a central identity microservice (AT Identity) for authentication, permissions, and session handling.

This decoupling enables clean service boundaries, faster dev cycles, and cross-app integration — ideal for modern, scalable systems.

🔗 [Loom Walkthrough](https://www.loom.com/share/795ebe98fa57463880091cb22868f6e7)  
📸 
<img width="1212" height="538" alt="image" src="https://github.com/user-attachments/assets/2cfc689b-308d-40a2-aca9-3b8ee67805d7" />

---

## 🧱 Architecture Overview

```text
┌─────────────┐    HTTP API    ┌─────────────┐    HTTP API    ┌─────────────┐
│  StoreLoop  │◄──────────────►│ AT Identity │◄──────────────►│ Artisan CRM │
│             │                │   Service   │                │             │
│ NO USERS    │                │ Master User │                │ NO USERS    │
│ user_id INT │                │ Management  │                │ user_id INT │
└─────────────┘                └─────────────┘                └─────────────┘
