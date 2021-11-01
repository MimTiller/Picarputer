This is the repo for Picarputer, a python Car UI for the Raspberry Pi

![Picarputer Interface](https://raw.githubusercontent.com/MimTiller/Picarputer/master/picarputer.PNG)

## Overview of ToDos

A overview of ToDos can be found in [this file](todo-list.md).

## Requirements:

x86 PC or Raspberry Pi with python 3.7 (if building with the install script, otherwise you can install python3-kivy)

Feature-Requirements can be found [here](requirements.md).

## Installation:

clone the github repo
install all pip requirements with 'python3 -m pip install -r requirements.txt'
in a command terminal, run 'python3 main.py'

## Usage:

to use the application, simply run
'python main.py' in the picarputer folder

## Compatibility:

Because this app is built using python/kivy, Windows, Linux, and MacOS are all supported.

1. Windows does not have an easy way to pull AVRCP bluetooth data, so that is not supported
2. Android and iOS may eventually be supported, depending on my free time and willpower
