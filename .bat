@echo off
cd %~dp0 
call virtual\scripts\activate
call pip install -r requirements.txt
cd %~dp0
call python updateScript.py

