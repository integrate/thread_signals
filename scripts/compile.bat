set base_dir=%~dp0..

if exist %base_dir%\build (echo y | rmdir /s %base_dir%\build)
if exist %base_dir%\dist (echo y | rmdir /s %base_dir%\dist)
if exist %base_dir%\thread_signals.egg-info (echo y | rmdir /s %base_dir%\thread_signals.egg-info)

%base_dir%\setup.py bdist_wheel
