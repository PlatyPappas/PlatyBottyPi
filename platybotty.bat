@ECHO OFF
ECHO Starting up Twitch interface
start node C:\Users\pappa\Documents\Projects\PlatyBottyPi\twitchInterface.js 
ECHO Initiate python virtual environment
C:\Users\pappa\Documents\Projects\PlatyBottyPi\.venv\Scripts\activate.bat && start python C:\Users\pappa\Documents\Projects\PlatyBottyPi\pluginLoader.py
C:\Users\pappa\Documents\Projects\PlatyBottyPi\.venv\Scripts\deactivate.bat