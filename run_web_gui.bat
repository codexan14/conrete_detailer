@echo off
start "FastAPI Server" cmd /k "fastapi dev .\api\main.py"
start "Streamlit App" cmd /k "streamlit run .\streamlit_app\main.py"