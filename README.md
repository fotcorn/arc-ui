# ARC UI Development Setup

This guide will help you set up the development environment for the ARC UI project.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- virtualenv

## Setup Steps

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env.dev` file in the project root with the following content:
   ```
   DEBUG=1
   SECRET_KEY=your-secret-key-here
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
   ```
   Replace `your-secret-key-here` with a secure secret key.

5. Run database migrations:
   ```
   python manage.py migrate
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

The application should now be running at `http://localhost:8000`.
