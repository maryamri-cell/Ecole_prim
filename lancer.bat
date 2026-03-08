@echo off
echo ========================================
echo   EcoleCom - Lancement du serveur Flask
echo ========================================
echo.

:: Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installé !
    echo Téléchargez Python sur https://python.org
    pause
    exit
)

:: Installer les dépendances si nécessaire
if not exist "venv" (
    echo Installation de l'environnement virtuel...
    python -m venv venv
    echo Installation des dépendances...
    venv\Scripts\pip install -r requirements.txt
    echo.
)

:: Lancer l'application
echo Démarrage du serveur...
echo Ouvrez votre navigateur sur : http://localhost:5000
echo Appuyez sur CTRL+C pour arrêter le serveur.
echo.
venv\Scripts\python app.py
pause
