@echo off
echo Empaquetando GestProd v6...

:: Crear carpeta de salida si no existe
if not exist "dist" mkdir dist

:: Limpiar carpetas anteriores
if exist "build" rmdir /s /q build
if exist "dist\GestProd" rmdir /s /q dist\GestProd

:: Empaquetar con PyInstaller
echo Ejecutando PyInstaller...
pyinstaller --noconfirm --onefile --windowed --icon=assets/favicon.ico --name="GestProd" ^
    --add-data="assets;assets" ^
    main.py

:: Copiar base de datos y otros archivos necesarios
echo Copiando archivos adicionales...
if not exist "dist\GestProd" mkdir dist\GestProd
copy dist\GestProd.exe dist\GestProd\
copy produccion.db dist\GestProd\
if exist "window_preference.txt" copy window_preference.txt dist\GestProd\
if exist "theme_preference.txt" copy theme_preference.txt dist\GestProd\

echo.
echo Empaquetado completado. La aplicación se encuentra en la carpeta dist\GestProd
echo.
pause
