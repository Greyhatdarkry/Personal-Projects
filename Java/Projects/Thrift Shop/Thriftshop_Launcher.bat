@echo off
set "JDK_PATH=C:\Program Files (x86)\Java\jdk1.7.0_17"
set "JAVA_EXE=%JDK_PATH%\bin\java.exe"
if not exist "%JAVA_EXE%" set "JAVA_EXE=java"

echo Compiling Thrift Shop GUI...
"%JDK_PATH%\bin\javac.exe" -cp . *.java

if %ERRORLEVEL% EQU 0 (
    echo Compilation successful! Starting app...
    "%JAVA_EXE%" Thriftshop
) else (
    echo Compilation failed. Please check if the JDK_PATH is correct in this script.
    pause
)
