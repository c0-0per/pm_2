@echo off
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python to continue.
    exit /b
)

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

echo Installing required packages...
pip install -r requirements.txt

set FLASK_APP=app.py
set FLASK_ENV=development

echo Starting Flask application...
flask run

deactivate
