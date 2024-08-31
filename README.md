# Indian Sign Language (ISL) Learning Tool

This repository contains the backend code for an Indian Sign Language (ISL) learning tool built using FastAPI and SQLAlchemy. The tool is designed to help users learn and practice ISL through structured lessons, quizzes, and milestones, providing an interactive and user-friendly experience.

## Features

- **User Registration and Authentication**: Secure user registration and login system with JWT-based authentication to protect routes and user data.
  
- **Learning Resources**: A collection of ISL lessons with videos and descriptions. Users can browse through various lessons to learn new signs and practice them.
  
- **Milestones and Badges**: Users can achieve milestones as they progress through the lessons. Badges are awarded for completing specific milestones, encouraging continuous learning.

- **Quizzes**: Users can test their knowledge through quizzes associated with each lesson. Immediate feedback is provided, allowing users to assess their learning progress.

- **User Progress Tracking**: Track user progress through lessons and quizzes to personalize the learning experience.

- **Admin Management**: Admin routes to manage content, such as creating, updating, and deleting lessons, milestones, and quizzes.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python to interact with the PostgreSQL database.
- **PostgreSQL**: A powerful, open-source object-relational database system.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **JWT Authentication**: JSON Web Token for secure authentication.

## Getting Started

### Prerequisites

- Python 3.6+
- PostgreSQL

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/isl-learning-tool.git
   cd isl-learning-tool

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
3. **Set up the database**:
   - Create a PostgreSQL database.
   - Update the database connection details in the `config.py` file.
4. **Run the application**:
   ```bash
   uvicorn main:app --reload
5. **Access the application**:
   - Open your web browser and navigate to `http://localhost:8000` to access the application.
6. **Admin Routes**:
   - To access admin routes, use the following credentials:
   - Username: admin
   - Password: admin
7. **User Routes**:
   - To access user routes, use the following credentials:
   - Username: user
   - Password: user