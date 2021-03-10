set base_dir=%~dp0..
set ver=0.1.3

set twine=%base_dir%\venv\scripts\twine.exe
set ver_name=%base_dir%\dist\thread_signals-%ver%-py3-none-any.whl

%twine% upload %ver_name%
