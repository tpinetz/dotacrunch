Dotacrunch
==========

About
-----
Dotacrunch is a tool that aims to make data from replays easily accesible, as well as providing some utility Classes to ease visualizing of this data. It is built on smoke, a parsing utility for Dota2-Replays.

Prerequisites
-------------
Before you can install the necessary libraries via pip it might be possible that you have to install some packages for your linux distribution first. To install all the libraries from requirements.txt execute the following command from the main directory of this repository:

`$ pip install -r requirements.txt`

You also need to install smoke which is currently not on pip, just follow the instructions on their github page: [smoke](https://github.com/skadistats/smoke)

Installation
------------

To install, simply type
`python setup.py install`

Usage
-----
You can find example usage for the API in the examples folder. You have to install the library beforehand. Execute all of them or a specific one with the following commands:

`$ python -m examples`

`$ python -m examples.draw_movement`


If you want to know how the library works, you can check out the tests. To run them, change into the src/dotacrunch folder and execute:

`$ python -m unittest discover tests`

Credits
-------

[smoke](https://github.com/skadistats/smoke) for providing an awesome library to fetch replay data
