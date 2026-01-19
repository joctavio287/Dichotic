@echo off
setlocal

python behavioural_analysis.py
if errorlevel 1 exit /b %errorlevel%

python eeg_preprocessing.py
if errorlevel 1 exit /b %errorlevel%

python evoked_potentials.py
if errorlevel 1 exit /b %errorlevel%

endlocal
