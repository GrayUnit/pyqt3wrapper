============
Pyqt3Wrapper
============
[![Build Status](https://travis-ci.org/NicolasHExia/pyqt3wrapper.svg?branch=master)](https://travis-ci.org/NicolasHExia/pyqt3wrapper)


Dependencies
------------

Python 2.7 or later, including all Python 3.x versions.

PyQt. You may download PyQt4 or PyQt5.
PyQt need Qt and sip to be used.

Download Qt : http://www.qt.io/download/

Download Sip : http://www.riverbankcomputing.com/software/sip/download

Download Pyqt: http://www.riverbankcomputing.com/software/pyqt/download5


Quick start
-----------

Download tar.gz file in dist repository
```sh
wget https://github.com/NicolasHExia/pyqt3wrapper/blob/master/dist/pyqt3wrapper-0.0.0.tar.gz
tar xzf pyqt3wrapper-0.0.0.tar.gz
cd pyqt3wrapper-0.0.0
python setup.py install
```

Now you can use:
```sh
wrappyqt3 uifile.ui
```

Have fun

Description
-----------

Since the update of pyqt4 -> pyqt5, the option -w (--pyqt3-wrapper)
has disappeared. So, if you were using pyqt before version 4 some of your ui 
files compiled with pyqt5 will not be compatible.

This program generates excatly the same thing as --pyqt3-wrapper option.

But it does not generate only this block, it uses the pyuic module and generates
a build ui file complete, compatible with earlier versions of pyqt.

You can see an example of code generate in the file tests/output/test_pyuicwrapper

Command Line Arguments
----------------------
```
Example: wrappyqt3 -o file_generate.py uifile.ui

positional arguments:
  inputfile             This is the name of uifile that will be parse

optional arguments:
  -o 					This is the name of file that will be build
  -f, --force           If the output file (-o option) exist, this option allows
  						overwriting.
  						If the output file exist and 
  						you do not specify this option, this error will appear:
  						"Your file exists. Use -f option for overwrite it"


This program use pyuic module. You can use these three arguments as in pyuic:
  
  -x, --execute

  -d, --debug

  -n N, --indent N
```

Exit codes
----------
	* **0** success
	* **1** input file read error
	* **2** output file already exists without --force specified


Environment
===========
PYUIC_PATH= ...
