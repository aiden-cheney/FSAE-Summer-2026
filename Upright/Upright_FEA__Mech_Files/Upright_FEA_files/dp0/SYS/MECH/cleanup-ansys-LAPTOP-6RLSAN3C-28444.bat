@echo off
set LOCALHOST=%COMPUTERNAME%
if /i "%LOCALHOST%"=="LAPTOP-6RLSAN3C" (taskkill /f /pid 35308)
if /i "%LOCALHOST%"=="LAPTOP-6RLSAN3C" (taskkill /f /pid 21352)
if /i "%LOCALHOST%"=="LAPTOP-6RLSAN3C" (taskkill /f /pid 28860)
if /i "%LOCALHOST%"=="LAPTOP-6RLSAN3C" (taskkill /f /pid 35064)
if /i "%LOCALHOST%"=="LAPTOP-6RLSAN3C" (taskkill /f /pid 16816)
if /i "%LOCALHOST%"=="LAPTOP-6RLSAN3C" (taskkill /f /pid 27520)
if /i "%LOCALHOST%"=="LAPTOP-6RLSAN3C" (taskkill /f /pid 36016)
if /i "%LOCALHOST%"=="LAPTOP-6RLSAN3C" (taskkill /f /pid 28444)

del /F cleanup-ansys-LAPTOP-6RLSAN3C-28444.bat
