@echo off
cd %~dp0 
call activate tracker
cd %~dp0
call python updateScript.py

