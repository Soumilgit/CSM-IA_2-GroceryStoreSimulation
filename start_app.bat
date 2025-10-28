@echo off
echo.
echo ========================================
echo  Grocery Store Simulation Launcher
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please create one first: python -m venv .venv
    pause
    exit /b 1
)

echo [1/3] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [2/3] Checking dependencies...
python -c "import simpy, gradio, matplotlib, pandas" 2>nul
if errorlevel 1 (
    echo [!] Missing dependencies, installing...
    pip install simpy gradio matplotlib pandas --quiet
    pip install "huggingface_hub<1.0" --quiet
)

echo [3/3] Starting Gradio app...
echo.
echo ========================================
echo  Server will start at:
echo  http://127.0.0.1:7860
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python gradio_app_simple.py

echo.
echo Server stopped.
pause
