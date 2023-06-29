:: Set the project root directory.
set PYTHONPATH=%WORKSPACE%

:: Set the basic python binary and virtual environment location.
set PYTHON_BASIC_BINARY=C:\Users\Amanda\AppData\Local\Programs\Python\Python311\python.exe
set PYTHON_VENVS=D:\venv

:: Check and create virtual environment.
if not exist %PYTHON_VENVS% (
    mkdir %PYTHON_VENVS%
)
set VENV=%PYTHON_VENVS%\venv_%JOB_BASE_NAME%
if not exist %VENV%\pyvenv.cfg (
    call %PYTHON_BASIC_BINARY% -m venv %VENV%
    call %VENV%\Scripts\python.exe -m pip install --upgrade pip >nul 2>&1
    call %VENV%\Scripts\python.exe -V
    call %VENV%\Scripts\pip.exe -V
)

:: Activate to join the virtual environment.
call %VENV%\Scripts\activate.bat

:: Update dependencies.
pip install -r requirement.txt -q

:: Execute.
call "%VENV%\Scripts\pytest"

call allure serve allure_results