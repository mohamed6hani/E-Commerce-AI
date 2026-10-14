@echo off
REM open_server.bat
REM This script opens your eCommerce AI development server in your default browser.
REM Modify the PORT variable below if your server runs on a different port (e.g., 8000 for FastAPI, 5000 for Node/Express).

set PORT=8800

REM Build the React frontend so it can be served statically by the backend
pushd ..\frontend-react
npm run build
popd

REM Start the backend in a new window (now serving API + UI on port 8800)
start "MERN Backend" npm start

REM Wait 10 seconds to give the server time to start
TIMEOUT /T 10 /NOBREAK > NUL

REM Open the login page in the default browser
start "" http://localhost:%PORT%/login
pause

