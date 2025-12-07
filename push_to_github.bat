@echo off
echo.
echo ============================================
echo   GitHub Push Script
echo ============================================
echo.
echo INSTRUCTIONS:
echo 1. Create a Personal Access Token at:
echo    https://github.com/settings/tokens/new
echo.
echo 2. Token name: pdfproject
echo 3. Check: repo (all permissions)
echo 4. Generate token and COPY it
echo.
echo 5. Run this command with your token:
echo.
echo    git push https://YOUR_TOKEN@github.com/sumathiselvan79/cidc-7.git main
echo.
echo Replace YOUR_TOKEN with your actual token
echo.
echo ============================================
echo.
set /p token="Paste your GitHub token here and press Enter: "
echo.
echo Pushing to GitHub...
git push https://%token%@github.com/sumathiselvan79/cidc-7.git main
echo.
if %errorlevel% equ 0 (
    echo ============================================
    echo   SUCCESS! Code pushed to GitHub!
    echo   https://github.com/sumathiselvan79/cidc-7
    echo ============================================
) else (
    echo ============================================
    echo   FAILED! Check your token and try again.
    echo ============================================
)
pause
