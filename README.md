This is the repo for Picarputer, a python Car Display/UI for the Raspberry Pi

![Picarputer Interface](https://raw.githubusercontent.com/MimTiller/Picarputer/master/picarputer.PNG)


## Requirements:
x86 PC 
Raspberry Pi or other ARM based processor

## Installation:
install [Kivy](https://kivy.org/doc/stable/gettingstarted/installation.html), the graphical interface used for this project

clone the github repo 
`git clone https://github.com/mimtiller/picarputer`

install all pip requirements
`python3 -m pip install -r requirements.txt`

run it!
`python3 main.py`

## Usage:
to use the application, simply run
'python3 main.py' in the picarputer folder

## Compatibility:
Because this app is built using python/kivy, Windows, Linux, and MacOS are all supported.
1. Windows does not have an easy way to pull AVRCP bluetooth data, so that is not supported
2. Android and iOS are a future possibility as it ports easily
