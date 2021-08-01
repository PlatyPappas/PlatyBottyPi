@ECHO OFF
ECHO Starting up Twitch interface
start node C:\Users\pappa\Documents\Projects\PlatyBottyPi\twitchInterface.js 
ECHO Initiate python virtual environment
C:\Users\pappa\Documents\Projects\PlatyBottyPi\.venv\Scripts\activate.bat && start C:\Users\pappa\Documents\Projects\PlatyBottyPi\.venv\Scripts\python C:\Users\pappa\Documents\Projects\PlatyBottyPi\pluginLoader.py