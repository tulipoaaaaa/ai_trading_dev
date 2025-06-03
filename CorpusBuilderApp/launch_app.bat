@echo off
REM File: launch_app.bat

REM Activate the virtual environment
call G:\venv\ai_trading_dev_1\Scripts\activate.bat

REM Navigate to the application directory
cd /d %~dp0

REM Run the application
python app\main.py

REM Deactivate the virtual environment when done
call deactivate
