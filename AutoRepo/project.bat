@echo off
:: if a period is provided as a second argument the project repo will be created in the directory from which the file is run, else points to a default directory for projects
if not [%2]==[.] (cd "Path\to\projects\collection")
"%~dp0\gitrepo.py" %1
