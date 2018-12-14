FROM ubuntu:16.04

RUN sudo apt install git
RUN sudo apt-get update
RUN sudo apt-get upgrade
RUN sudo apt-get install build-essential cmake pkg-config
RUN sudo apt-get install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev
RUN sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
RUN sudo apt-get install libxvidcore-dev libx264-dev
RUN sudo apt-get install libgtk-3-dev
RUN sudo apt-get install libatlas-base-dev gfortran
RUN sudo apt-get install python2.7-dev python3.5-dev
RUN sudo apt-get install cmake
RUN sudo apt-get install libgoogle-glog-dev
RUN sudo apt-get install libatlas-base-dev
RUN sudo apt-get install libeigen3-dev
RUN sudo apt-get install libsuitesparse-dev
RUN sudo apt-get install libboost-all-dev
RUN sudo apt-get install freeglut3-dev
RUN sudo apt-get install doxygen

# Installing OpenCV 
RUN cd \
    && wget https://github.com/opencv/opencv/archive/3.1.0.zip \
    && unzip 3.1.0.zip \
    && cd opencv-3.1.0 \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install \
    && cd \
    && rm 3.1.0.zip

RUN cd \
    && wget https://github.com/opencv/opencv_contrib/archive/3.1.0.zip \
    && unzip 3.1.0.zip \
    && cd opencv-3.1.0/build \
    && cmake -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.1.0/modules/ .. \
    && make \
    && make install \
    && cd ../.. \
&& rm 3.1.0.zip

# Installing PCL
#RUN apt-get install -y software-properties-common 
RUN apt-get update && apt-get install -y \
		git build-essential linux-libc-dev \
		cmake cmake-gui \
		libusb-1.0-0-dev libusb-dev libudev-dev \
		mpi-default-dev openmpi-bin openmpi-common \
		libflann1.8 libflann-dev \
		libeigen3-dev \
		libboost-all-dev \
		libvtk5.10-qt4 libvtk5.10 libvtk5-dev \
		libqhull* libgtest-dev \
		freeglut3-dev pkg-config \
		libxmu-dev libxi-dev \
		qt-sdk openjdk-8-jdk openjdk-8-jre \
		openssh-client

# PCL - build from source and install 
RUN cd /opt \
   && git clone https://github.com/PointCloudLibrary/pcl.git pcl-trunk \
   && ln -s /opt/pcl-trunk /opt/pcl \
   && cd /opt/pcl && git checkout pcl-1.8.0 \
   && mkdir -p /opt/pcl-trunk/release \
   && cd /opt/pcl/release && cmake -DCMAKE_BUILD_TYPE=None -DBUILD_GPU=ON -DBUILD_apps=ON -DBUILD_examples=ON .. \
   && cd /opt/pcl/release && make -j3 \
   && cd /opt/pcl/release && make install \
   && cd /opt/pcl/release && make clean

# Installing python-cpl
RUN cd \
	&& git clone https://github.com/strawlab/python-pcl.git
	&& pip install --upgrade pip
	&& pip install cython==0.25.2
	&& pip install numpy
	&& python setup.py build_ext -i
	&& python setup.py install

CMD ["echo", "hello world!"]