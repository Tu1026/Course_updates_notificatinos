@echo off
cd %~dp0 
call virtual\scripts\activate
cd %~dp0
call python updateScript.py

