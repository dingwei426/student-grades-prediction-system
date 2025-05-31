# 🧠 Student Grades Prediction System

A full-stack AI-powered academic advising tool that predicts student performance and recommends optimized subject study plans based on CGPA improvement potential.

## 📚 Table of Contents

- [🚀 Features](#-features)
- [🛠️ Developer Setup Guide](#️-developer-setup-guide)
  - [⚙️ Environment Configuration & Database Setup](#️-environment-configuration--database-setup)
  - [🧪 Option 1: Manual Setup](#-option-1-manual-setup)
  - [🐳 Option 2: Run with Docker Compose](#-option-2-run-with-docker-compose)
- [🖼️ UI Screenshots](#️-ui-screenshots)

## 🚀 Features

- 🎓 Predicts student grades using ML models (LightGBM, RandomForest, etc.)
- 📊 Recommends core and elective subjects to improve CGPA
- 🧠 AI-generated personalized study plans (OpenRouter API)
- ⚙️ Flask backend with JWT authentication and SQLAlchemy
- 🌐 ReactJS frontend with clean UI
- 🐬 MySQL and 🟥 Redis support
- 🐳 Dockerized for easy deployment

## 🛠️ Developer Setup Guide

> [!NOTE]
> ai_ml directory includes the script to train and download the ML models.
> Random Forest Models should be store in /backend/app/services/predictive-models/rf_9.
> LightGBM Models should be store in /backend/app/services/predictive-models/lgbm_9.

### ⚙️ Environment Configuration & Database Setup

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Open `.env` and fill in the necessary values:

```env
SECRET_KEY='your_secret_key'
JWT_SECRET_KEY='your_jwt_secret_key'
DATABASE_URI='mysql+pymysql://root:root@localhost/student_grades'
MAIL_USERNAME='your_email@example.com'
MAIL_DEFAULT_SENDER='your_email@example.com'
MAIL_PASSWORD='your_email_password'
MAIL_SERVER='smtp.gmail.com'
MAIL_USE_TLS='True'
OPENROUTER_API_KEY='your_openrouter_api_key'
REDIS='localhost'
```

---

### 🧪 Option 1: Manual Setup

#### ✅ Step 1: Start MySQL and Redis using Docker

> [!NOTE]
> You may run in these in localhost instead of using docker.

```bash
# MySQL
docker run --name mysql-fyp-container -e MYSQL_ROOT_PASSWORD=root -d -p 3306:3306 mysql:latest

# Redis
docker run --name redis-fyp-container -d -p 6379:6379 redis
```

Create the database in MySQL:

```sql
mysql -u root -p
# Enter password: root
CREATE DATABASE student_grades CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

#### ✅ Step 2: Set Up Python Environment & Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run DB migrations
flask db upgrade

# Start Flask server
flask run
```

> Backend runs at: `http://localhost:5000`

#### ✅ Step 3: Start React Frontend

```bash
cd frontend
npm install
npm start
```

> Frontend runs at: `http://localhost:3000`

---

### 🐳 Option 2: Run with Docker Compose

> [!NOTE]  
> In your `.env` file:
>
> - Change `DATABASE_URI=mysql+pymysql://root:root@localhost/student_grades`
>   to `DATABASE_URI=mysql+pymysql://root:root@mysql/student_grades`
> - Change `REDIS='localhost'` to `REDIS='redis'`

#### ✅ Step 1: Start with Docker Compose

```bash
docker-compose up --build
```

This will:

- Build and run the Flask backend
- Start the React frontend
- Launch MySQL and Redis containers

#### ✅ Step 2: Apply Database Migrations

Create the database:

```bash
docker exec -it mysql mysql -u root -p
# Enter password: root
CREATE DATABASE student_grades CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

Once the backend container is running, apply migrations:

```bash
# Stamp the DB to match your current models (if already existing)
docker-compose exec backend flask db stamp head

# Generate the migration script
docker-compose exec backend flask db migrate -m "Initial migration"

# Apply migration to create/update tables
docker-compose exec backend flask db upgrade
```

---

✅ **Your system is now running!**
Access it at:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:5000](http://localhost:5000)

---

## 🖼️ UI Screenshots

### 🔐 Login Page

![Login Page](img/login.png)

### 📝 Signup Page

![Signup Page](img/signup.png)

### 🏠 Home Page

![Home Page](img/homepage.png)

### 📈 Prediction Result

![Prediction Result Page](img/prediction_result.png)

### 🧾 Prediction History

![Prediction History Page](img/prediction_history.png)

### 🤖 AI Recommendation

![AI Recommendation Section](img/ai_recommendation.png)

### ⚙️ Settings

![Settings Page](img/settings.png)
