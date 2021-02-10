#!/bin/bash
# -*- coding: utf-8 -*-


#!/bin/sh


case "$(uname -s)" in

   Darwin)
     echo 'Mac OS X'
     ;;

   Linux)
     echo 'Linux'
     # shellcheck disable=SC2006  
     `pyinstaller --onefile  --add-binary "data/icon.ico,icon.ico" --add-binary "data/hi_res_icon.png,hi_res_icon.png" --icon "data/icon.ico" -n "lock-in"  lockin.py`
     ;;

   CYGWIN*|MINGW32*|MSYS*|MINGW*)
     echo 'MS Windows'
     # shellcheck disable=SC2006
     `pyinstaller.exe --onefile  --add-binary "data\\icon.ico;icon.ico" --add-binary "data\\hi_res_icon.png;hi_res_icon.png" --icon "data\\icon.ico" -n "lock-in"  lockin.py`
     #`pyinstaller.exe --onefile -w --add-binary "data\\icon.ico;icon.ico" --add-binary "data\\hi_res_icon.png;hi_res_icon.png" --icon "data\\icon.ico" -n "lock-in"  lockin.py`
     rm -rf ./build
     rm -rf ./__pycache__
     rm  ./lock-in.spec
     echo 'building for MS Windows DONE'
     ;;

   # Add here more strings to compare
   # See correspondence table at the bottom of this answer

   *)
     echo 'Other OS'
     ;;
esac
