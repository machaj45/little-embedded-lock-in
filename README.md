# Little Embedded Lock-in
This is little lock-in amplifier that is based on NUCLEO-F303RE - STM32 Nucleo-64 development board. This device comunicate with desktop aplication that computes outcome of selected mesurments and also gives user ability to controlo nucleo board.
## Main manual
Main manual is in this repository in pdf format that gives clear information how to handle this device.
## Unknown Issues
Please report any issues that bothers you in issue section of this repository or on email jmachalek@seznam.cz
Thank you in advance.
## Known Issues 
  - Pyserial needs **permmision** on ubuntu for accesing usb ports
    - solution:
      - use user group to give your self priviliages
      ```
      sudo usermod -a -G dialout {your_user_name} 
      ```
      - restart your computer
## Known Issues for building on linux
  - PyQt5 is missing library on ubuntu 20.10 called **libxcb-xinerama0** 
    - solution: 
      - install that library to your system
      ```
      sudo apt install libxcb-xinerama0 
      ```
