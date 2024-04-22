#!/bin/bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git
sudo apt-get install cmake
sudo apt-get install g++
sudo apt-get install python3
sudo apt-get install pip
pip install numpy
sudo apt-get install libxss-dev libxxf86vm-dev libxkbfile-dev libxv-dev
sudo apt-get install libxpm-dev
sudo apt-get install libxft-dev
sudo apt-get install wget
sudo apt-get install libxerces-c-dev
sudo apt-get install libqt5core5a
sudo apt-get install qtbase5-dev
sudo apt-get install libxmu-headers
sudo apt-get install libxmu-dev
sudo apt-get install libmotif-dev

get_root(){
	git clone --branch latest-stable --depth=1 https://github.com/root-project/root.git root_src
	mkdir root_build root_install && cd root_build
	cmake -DCMAKE_INSTALL_PREFIX=../root_install ../root_src
	cmake --build . -- install -j4
	source ../root_install/bin/thisroot.sh
}


get_geant4(){
	wget https://github.com/Geant4/geant4/archive/refs/tags/v11.2.1.tar.gz
	tar -xf v11.2.1.tar.gz
	cd geant4-11.2.1
	mkdir geant4_build
	cd geant4_build
	cmake -DGEANT4_INSTALL_DATA=ON -DGEANT4_USE_GDML=ON -DGEANT4_USE_OPENGL_X11=ON -DGEANT4_USE_XM=ON -DGEANT4_USE_QT=ON -DGEANT4_BUILD_MULTITHREADED=ON -DGEANT4_USE_RAYTRACER_X11=ON -DCMAKE_INSTALL_PREFIX=./ ../
	make -j8
	make install
	source bin/geant4.sh
}

get_genie(){
	echo "add here"
}

get_geant4
