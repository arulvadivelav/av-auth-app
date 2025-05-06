# av-auth-app

This project is a full-stack Authentication App built with React (frontend) and Django (backend). It includes essential user authentication features such as Login, Send OTP, Verify OTP, Register, and Forgot Password. The backend provides secure REST APIs to support these features, while the frontend offers a responsive UI for seamless user interaction. This application is designed as a reusable and extensible foundation for integrating authentication workflows into any web application.

# 🔧 Backend Setup (Django)

### 📦 Prerequisites
- Python 3.8+
- pip
- Virtualenv (optional but recommended)

### 🚀 Setup Instructions

```bash
# Navigate to backend folder
cd backend/auth_project

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy example settings and configure
cp auth_project/settings.example.py auth_project/settings.py
# Edit auth_project/settings.py and set SECRET_KEY, DB, etc.

# Run migrations and start the server
python manage.py migrate
python manage.py runserver
```
# 🔧 Frontend(UI) Setup (React)

## Make sure you have the following installed:

- [Node.js](https://nodejs.org/) (v11 or higher)
- npm

## Clone the Repository

## 🚀 Setup Instructions

- Change the BASE_URL in the UI/admin-app/services/AuthServices.jsx file with the backend URL

```bash
cd ui/admin-app

npm install

npm start
```

## Photos

![image](https://github.com/user-attachments/assets/e65f813f-6a05-42a5-b6dd-9c0c03b20ece)
![image](https://github.com/user-attachments/assets/2705d530-adfc-4c9a-9845-07c471d45928)
![image](https://github.com/user-attachments/assets/8a2f7f5a-5196-44ee-9627-1afff6b7d555)
![image](https://github.com/user-attachments/assets/21057c11-4e07-4882-932f-41d74a6a6c09)
![image](https://github.com/user-attachments/assets/f9e3467a-e236-42f6-9e69-b631c1806332)

```