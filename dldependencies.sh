#!/bin/bash

sudo pip install --upgrade pip 1> /dev/null
sudo apt-get -qq update 1> /dev/null

if [ "$PYQT" == "PyQt4" ]; then
	sudo apt-get -qq install libqt4-dev python-qt4 pyqt4-dev-tools qt4-designer
	sudo apt-get -qq install python3-nose python-nose
	sudo apt-get -qq install pep8
	pip install --use-mirrors coveralls

	wget http://jaist.dl.sourceforge.net/project/pyqt/sip/sip-4.16.7/sip-4.16.7.tar.gz
	tar zxvf sip-4.16.7.tar.gz
	cd sip-4.16.7
	python configure.py
	make --silent
	sudo make install --silent

	python3 configure.py
	make --silent
	sudo make install --silent
	cd ..

	wget http://jaist.dl.sourceforge.net/project/pyqt/PyQt4/PyQt-4.10.4/PyQt-x11-gpl-4.10.4.tar.gz
	tar zxvf PyQt-x11-gpl-4.10.4.tar.gz
	cd PyQt-x11-gpl-4.10.4/
	echo 'yes' | python configure.py
	make --silent
	sudo make install --silent

	sudo apt-get install python3-pyqt4
	cd ..
	rm -R PyQt-x11-gpl-4.10.4/
	rm -R sip-4.16.7
	python -c 'import sip'
	python -c 'import PyQt4'
	python -c 'import PyQt4.QtCore'
fi

if [ "$PYQT" == "PyQt3" ]; then
	sudo add-apt-repository --yes ppa:ubuntu-sdk-team/ppa 1> /dev/null
	sudo apt-get update -qq 1> /dev/null
	sudo apt-get -qq install qtbase5-dev qtdeclarative5-dev libqt5webkit5-dev libsqlite3-dev 1> /dev/null
	sudo apt-get -qq install qt5-default qttools5-dev-tools 1> /dev/null
	sudo apt-get -qq install python3-nose python-nose 1> /dev/null
	sudo apt-get -qq install pep8 1> /dev/null
	pip install --use-mirrors coveralls 1> /dev/null

	wget http://download.qt.io/official_releases/qt/5.4/5.4.1/single/qt-everywhere-opensource-src-5.4.1.tar.gz
	tar zxvf qt-everywhere-opensource-src-5.4.1.tar.gz 1> /dev/null
	cd qt-everywhere-opensource-src-5.4.1
	sudo ./configure -opensource -confirm-license -qt-xcb -no-gif -no-compile-examples
	sudo make
	sudo make install --silent
	cd ..

	wget http://jaist.dl.sourceforge.net/project/pyqt/sip/sip-4.16.7/sip-4.16.7.tar.gz
	tar zxvf sip-4.16.7.tar.gz 1> /dev/null
	cd sip-4.16.7
	python configure.py 1> /dev/null
	make --silent
	sudo make install --silent

	python3 configure.py
	make --silent
	sudo make install --silent
	cd ..

	wget http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.4.1/PyQt-gpl-5.4.1.tar.gz
	tar zxvf PyQt-gpl-5.4.1.tar.gz 1> /dev/null
	cd PyQt-gpl-5.4.1/
	python configure.py
	make --silent
	sudo make install --silent
	sudo apt-get install python-pyqt5
	cd ..

	rm -R PyQt-gpl-5.4.1/
	rm -R sip-4.16.7
	python -c 'import sip'
	python -c 'import PyQt5'
	python -c 'import PyQt5.QtCore'
fi

if [ "$PYQT" == "PyQt5" ]; then
	sudo add-apt-repository "deb http://archive.ubuntu.com/ubuntu trusty universe" 1> /dev/null
	sudo add-apt-repository "deb http://archive.ubuntu.com/ubuntu trusty main" 1> /dev/null
	sudo apt-get update 1> /dev/null
	sudo apt-get install qdbus qmlscene qt5-default qt5-qmake qtbase5-dev-tools qtchooser qtdeclarative5-dev xbitmaps xterm libqt5svg5-dev qttools5-dev qtscript5-dev qtdeclarative5-folderlistmodel-plugin qtdeclarative5-controls-plugin -y 1> /dev/null

	wget http://jaist.dl.sourceforge.net/project/pyqt/sip/sip-4.16.7/sip-4.16.7.tar.gz
	tar zxvf sip-4.16.7.tar.gz 1> /dev/null
	cd sip-4.16.7
	python configure.py 1> /dev/null
	make --silent
	sudo make install --silent

	python3 configure.py 1> /dev/null
	make --silent
	sudo make install --silent
	cd ..

	wget http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.4.1/PyQt-gpl-5.4.1.tar.gz
	tar zxvf PyQt-gpl-5.4.1.tar.gz 1> /dev/null
	cd PyQt-gpl-5.4.1/
	python configure.py --confirm-license 1> /dev/null
	make --silent
	sudo make install
	cd ..

	rm -R PyQt-gpl-5.4.1/
	rm -R sip-4.16.7
	python -c 'import sip'
	python -c 'import PyQt5'
	python -c 'import PyQt5.QtCore'
fi