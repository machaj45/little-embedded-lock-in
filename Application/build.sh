#!/bin/bash



#!/bin/sh

case "$(uname -s)" in

   Darwin)
     echo 'Mac OS X'
     ;;

   Linux)
     echo 'Linux'
     ;;

   CYGWIN*|MINGW32*|MSYS*|MINGW*)
     echo 'MS Windows'
     `pyinstaller.exe --onefile  --add-binary "data\\icon.ico;icon.ico" --icon "data\\icon.ico" -n "lock-in"  lockin.py`
     ;;

   # Add here more strings to compare
   # See correspondence table at the bottom of this answer

   *)
     echo 'Other OS'
     ;;
esac