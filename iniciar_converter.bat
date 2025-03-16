@echo off
cd /d "C:\\Users\\loren\\Python - Lorenzo\\Projetos - Lorenzo\\PDF Converter Deploy"
call .venv\Scripts\activate
streamlit run converter.py
pause
