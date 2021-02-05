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
     # shellcheck disable=SC2006
     `pyinstaller.exe --onefile  --add-binary "data\\icon.ico;icon.ico" --icon "data\\icon.ico" -n "lock-in"  lockin.py`
     #`pyinstaller.exe --onefile -w  --add-binary "data\\icon.ico;data\icon.ico" --icon "data\\icon.ico" -n "lock-in"  lockin.py`
     ;;

   # Add here more strings to compare
   # See correspondence table at the bottom of this answer

   *)
     echo 'Other OS'
     ;;
esac