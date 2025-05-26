@echo off
setlocal

set TENANT_DOMAIN=chrisbbehrensproton.onmicrosoft.com
set DISPLAY_NAME=New User

if "%~1"=="" (
    echo ERROR: Username not provided. Usage: %0 username password
    goto :eof
)
if "%~2"=="" (
    echo ERROR: Password not provided. Usage: %0 username password
    goto :eof
)
set USER_NAME=%~1
set USER_PASSWORD=%~2
set USER_UPN=%USER_NAME%@%TENANT_DOMAIN%

call az ad user create ^
    --display-name "%DISPLAY_NAME%" ^
	--force-change-password-next-sign-in true ^
    --password "%USER_PASSWORD%" ^
    --user-principal-name %USER_UPN%

if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to create user.
    goto :eof
)

echo User %USER_UPN% created successfully!
echo Portal login: Use %USER_UPN% with provided password at https://portal.azure.com
echo Note: User must change password on first login.

endlocal
goto :eof