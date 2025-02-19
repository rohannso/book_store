# 📚 Book Voyage

## 📝 Overview
Book Voyage is a **full-stack e-commerce platform** for book trading, built using **Django**, with **authentication and payment processing** features. Users can **buy, sell, and trade books securely** with an intuitive interface.

## 🚀 Features
- 🔐 **User Authentication**: Secure login and registration with Django authentication.
- 💳 **Payment Processing**: Integrated a secure payment gateway.
- 📚 **Book Listing & Management**: Users can upload book details, images, and prices.
- 🔎 **Search & Filters**: Advanced search functionality to find books easily.
- 🎨 **Responsive UI**: Optimized for both desktop and mobile users.
- 📦 **Order Management**: Tracks purchases and order history.

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript (Bootstrap for styling)
- **Backend**: Django, Django REST Framework
- **Database**: MYSQL
- **Payment Gateway**: Razorpay

## 📂 Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/rohannso/book_store.git
cd book_store
```

### 2️⃣ Create a Virtual Environment & Install Dependencies
```sh
python -m venv env
source env/bin/activate   # On Windows use: env\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Apply Migrations
```sh
python manage.py migrate
```

### 4️⃣ Create a Superuser (For Admin Access)
```sh
python manage.py createsuperuser
```

### 5️⃣ Run the Development Server
```sh
python manage.py runserver
```
Access the platform at **http://127.0.0.1:8000/**.
)
