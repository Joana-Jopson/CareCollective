# 💙 CareCollective

**CareCollective** is a web-based platform designed to connect volunteers, donors, and nonprofit organizations in a unified digital space. It aims to simplify coordination, amplify impact, and promote social responsibility through event tracking, donations, volunteer listings, and photo documentation.

---

## 🌟 Key Objectives

- Build a centralized hub for community care efforts
- Enable real-time coordination between donors, volunteers, and NGOs
- Provide tools to showcase events and their impact through photo uploads
- Offer administrative controls to manage users and content

---

## 🚀 Features

- 🔐 User Authentication (Sign Up / Login / Logout)
- 🧑‍🤝‍🧑 Role-based Access: Admins, Volunteers, Donors
- 📝 Create & Manage Campaigns and Events
- 💰 Track Donations and Contributions
- 🤝 Volunteer Registration & Task Listings
- 📸 Photo Uploads for Events and Donations
- ⚙️ Admin Dashboard for Monitoring and Approvals
- 📱 Mobile-Responsive Frontend

---

## 🛠️ Tech Stack

### Backend

- **Python 3.10+**
- **Django 4.x**
- **SQLite3** (or PostgreSQL for production)

### Frontend

- **HTML5 + CSS3**
- **Bootstrap 5**
- **JavaScript (Vanilla)**

### Media Handling

- 📷 **Pillow** — For image processing
- 🧹 **django-cleanup** — To auto-delete unused media files
- 🧩 **django-crispy-forms** — For styled form layouts
- 🎛 **django-widget-tweaks** — For custom form UI

---

## 📂 Media & Photo Uploads

Users can upload photos for:
- Event documentation
- Proof of donation delivery
- Campaign posters

Ensure the following settings are added to `settings.py`:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
