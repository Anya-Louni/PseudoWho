@echo off
REM Build and Run Script for PseudoQui (Windows)
REM Provides convenient commands for development

SETLOCAL ENABLEDELAYEDEXPANSION

:menu
cls
echo ================================
echo   PseudoQui - Build Script
echo ================================
echo.
echo [1] Install All Dependencies
echo [2] Install Backend Only
echo [3] Install Frontend Only
echo [4] Run Backend Server
echo [5] Run Frontend Server
echo [6] Run Tests
echo [7] Clean Data Files
echo [8] Clean All Generated Files
echo [9] Check Status
echo [0] Exit
echo.
set /p choice="Enter your choice: "

if "%choice%"=="1" goto install_all
if "%choice%"=="2" goto install_backend
if "%choice%"=="3" goto install_frontend
if "%choice%"=="4" goto run_backend
if "%choice%"=="5" goto run_frontend
if "%choice%"=="6" goto run_tests
if "%choice%"=="7" goto clean_data
if "%choice%"=="8" goto clean_all
if "%choice%"=="9" goto check_status
if "%choice%"=="0" goto end
goto menu

:install_all
echo.
echo Installing all dependencies...
python setup.py
pause
goto menu

:install_backend
echo.
echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
cd ..
echo Backend dependencies installed!
pause
goto menu

:install_frontend
echo.
echo Installing frontend dependencies...
cd frontend
call npm install
cd ..
echo Frontend dependencies installed!
pause
goto menu

:run_backend
echo.
echo Starting backend server on http://localhost:5000
echo Press Ctrl+C to stop
cd backend
python run.py
cd ..
pause
goto menu

:run_frontend
echo.
echo Starting frontend server on http://localhost:3000
echo Press Ctrl+C to stop
cd frontend
call npm start
cd ..
pause
goto menu

:run_tests
echo.
echo Running tests...
cd backend
python -m pytest tests/ -v
cd ..
pause
goto menu

:clean_data
echo.
echo Cleaning data files...
if exist backend\data\tree_data.json del /q backend\data\tree_data.json
if exist backend\data\game_history.json del /q backend\data\game_history.json
echo Data files cleaned!
pause
goto menu

:clean_all
echo.
echo Cleaning all generated files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (*.egg-info) do @if exist "%%d" rd /s /q "%%d"
if exist backend\data\tree_data.json del /q backend\data\tree_data.json
if exist backend\data\game_history.json del /q backend\data\game_history.json
if exist frontend\build rd /s /q frontend\build
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
echo Cleanup complete!
pause
goto menu

:check_status
echo.
echo ================================
echo   System Status
echo ================================
echo.
echo Python version:
python --version
echo.
echo Node version:
node --version
echo.
echo npm version:
call npm --version
echo.
echo ================================
pause
goto menu

:end
echo.
echo Goodbye!
exit /b
