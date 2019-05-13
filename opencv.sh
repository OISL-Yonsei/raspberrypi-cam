#!/bin/bash

OPENCV_VERSION="4.1.0"

# check exit opencv modules
pkg-config --modversion opencv
if [ "$?" -eq 0 ]; then
    echo "You already install opencv"
    sudo find /usr/local/ -name "*opencv*" -exec rm  {} \;
fi

# update raspberry-pi
sudo apt-get update
sudo apt-get -y upgrade

# install build git cmake and some others
sudo apt-get install -y build-essential checkinstall git cmake wget unzip

# ffmpeg dependencies
sudo apt-get install -y libjack-jackd2-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libsdl1.2-dev libtheora-dev libva-dev libvdpau-dev libvorbis-dev libx11-dev libxfixes-dev libxvidcore-dev texi2html yasm zlib1g-dev libsdl1.2-dev libvpx-dev

# install image codecs
sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

# gstreamer
sudo apt-get install -y libgstreamer0.10-0 libgstreamer0.10-dev gstreamer0.10-tools gstreamer0.10-plugins-base libgstreamer-plugins-base0.10-dev gstreamer0.10-plugins-good gstreamer0.10-plugins-ugly gstreamer0.10-plugins-bad

# install video codecs
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev v4l-utils
sudo apt-get install -y libxvidcore-dev libx264-dev x264

# GTK to support OpenCV GUI
sudo apt-get install -y libgtk2.0-dev libqt4-dev libqt4-opengl-dev

# matrix operations optimization
sudo apt-get install -y libatlas-base-dev gfortran

# install python 2 and 3 and some python libs with pip
sudo apt-get install -y python2.7-dev python3-dev python-pip
sudo apt-get install -y python-tk python-numpy python3-tk python3-numpy python-qt4

mkdir ~/opencv

# opencv compilation
sudo apt-get autoremove -y libopencv-dev python-opencv

# download opencv
cd ~/opencv
wget -O opencv.zip https://github.com/opencv/opencv/archive/"$OPENCV_VERSION".zip
unzip opencv.zip

wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/"$OPENCV_VERSION".zip
unzip opencv_contrib.zip

cd opencv-"$OPENCV_VERSION"
mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D WITH_TBB=OFF \
-D WITH_IPP=OFF \
-D WITH_1394=OFF \
-D BUILD_WITH_DEBUG_INFO=OFF \
-D BUILD_DOCS=OFF \
-D INSTALL_C_EXAMPLES=ON \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D BUILD_EXAMPLES=OFF \
-D BUILD_TESTS=OFF \
-D BUILD_PERF_TESTS=OFF \
-D ENABLE_NEON=ON \
-D ENABLE_VFPV3=ON \
-D WITH_QT=OFF \
-D WITH_GTK=ON \
-D WITH_OPENGL=ON \
-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-"$OPENCV_VERSION"/modules \
-D WITH_V4L=ON \
-D WITH_FFMPEG=ON \
-D WITH_XINE=ON \
-D BUILD_NEW_PYTHON_SUPPORT=ON \
-D OPENCV_GENERATE_PKGCONFIG=ON ../
make
sudo make install
sudo /bin/bash -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/opencv.conf'
sudo ldconfig -v
