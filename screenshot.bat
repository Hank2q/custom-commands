@echo off
if [%1]==[] ("%~dp0\screenshot.py") else ("%~dp0\screenshot.py" %1)