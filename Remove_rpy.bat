@ECHO OFF

:choice
set /P c=Are you sure you want to remove all ".rpy" files from this directory[Y/N]?
if /I "%c%" EQU "Y" goto :somewhere
if /I "%c%" EQU "N" goto :somewhere_else
REM  /S *.rpy.*
REM dir /S *.rpy.* >> /S means include all sub-folders

goto :choice


:somewhere

del "abaqus.rpy"*
REM del *.SMABulk
REM del *.lck
REM del *.023
pause
exit

:somewhere_else

echo "Do not waste my time. Close this window!"
pause
exit