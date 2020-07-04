@echo off
if [%1]==[dir] (start C:\Users\HASSANIN\Desktop\PythonProj) && exit
if not [%2]==[.] (cd "C:\Users\HASSANIN\Desktop\PythonProj")
"%~dp0\gitrepo.py" %1