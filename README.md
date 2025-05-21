# CareCollective
CareCollective is a web-based platform designed to support and enhance community care initiatives. It connects volunteers, donors, and nonprofit organizations in a centralized ecosystem where they can collaborate to serve communities more efficiently. Built using Django, this project includes user management, event and donation tracking, media (photo) handling, and tools for organizing local support campaigns.

🌟 Project Objectives
Connect volunteers, donors, and NGOs through a shared digital space.

Enable users to post and find help requests, donation needs, or volunteering opportunities.

Allow photo uploads for events, resource deliveries, and verification of community impact.

Provide an admin interface for managing users, reports, and campaigns.

Ensure accessibility and scalability for growing community initiatives.

🚀 Features
User authentication (registration, login, logout)

Role-based access for admins, volunteers, and donors

Campaign and event management dashboard

Donation tracking system

Volunteer opportunity listings

Photo upload and gallery features for showcasing events and contributions

Admin panel for managing submissions and user accounts

Responsive and mobile-friendly interface

🛠️ Technologies Used
The project is built using the following technologies and libraries:

Backend
Python 3.10+

Django 4.x — The main web framework

WAMP SERVER

Frontend
HTML5, CSS3, Bootstrap 5 — for responsive design

JavaScript (Vanilla) — for basic interactivity

Media & Image Handling
Pillow — Python Imaging Library for managing uploaded images

django-cleanup — for automatic deletion of old media files

django-storages (optional) — if planning to integrate AWS S3 or similar

Others
Django Crispy Forms — for elegant form rendering

django-widget-tweaks — for customizing form inputs in templates

📷 Media & Photo Uploads
Users can upload images when submitting:

Donation proof

Event participation photos

Campaign posters or flyers

All uploaded media files are saved in the /media/ directory and can be managed via the admin dashboard. Make sure to set up media root and media URL correctly in your Django settings.py:

python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
