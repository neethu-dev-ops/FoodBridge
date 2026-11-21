# FoodBridge – Food Waste Reduction and Donation Platform

## Project Overview
FoodBridge is a Django-based web application designed to reduce food waste by connecting food donors with NGOs. Restaurants, hotels, bakeries and other donors can share surplus food with organizations that distribute it to people in need.

## Main Features
- User registration and login
- Role-based access for Donors, NGOs and Admin
- Donor dashboard
- Add and manage food donations
- AI-generated food descriptions using Google Gemini
- AI-based food category suggestions
- NGO dashboard to view available food
- NGOs can request food donations
- Donors can approve or reject requests
- Pickup scheduling and tracking
- NGOs can mark donations as collected
- Admin management through Django Admin

## Technologies Used
- Python
- Django
- HTML
- CSS
- Bootstrap
- JavaScript
- SQLite
- Google Gemini API

## Project Structure
- `core` – Main pages and templates
- `users` – User registration and profile management
- `donations` – Food donations, requests and pickup management
- `FoodBridge` – Django project settings and configuration

## Installation and Setup

1. Clone the repository:

   `git clone YOUR_GITHUB_REPOSITORY_URL`

2. Open the project folder:

   `cd FoodBridge`

3. Create a virtual environment:

   `python -m venv env`

4. Activate the virtual environment on Windows:

   `env\Scripts\activate`

5. Install the required packages:

   `pip install -r requirements.txt`

6. Create a `.env` file in the project root and add your Gemini API key:

   `GEMINI_API_KEY=your_api_key_here`

7. Apply database migrations:

   `python manage.py migrate`

8. Run the development server:

   `python manage.py runserver`

9. Open `http://127.0.0.1:8000/` in your browser.

## Database
SQLite is used as the project's database.

## Project Purpose
FoodBridge aims to reduce food wastage and support communities in need by making surplus food donation and collection easier.
