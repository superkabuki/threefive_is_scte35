#  The Makefile of Doom for python packaging
#
#  make install   ->  installs the package  in the current directory
#  make upload -> make a package from the current directory  and uploads to pypi.org
#
# set py3 on the command line  to use pypy3 or a different python version
#
#  like 
#           make install  py3=pypy3
#
#  default is python3
#

py3 = python3

build_cmd = -m build -n
install_cmd = -m pip   install  . --user --no-build-isolation --break-system-packages 

default: install

clean:
	rm -f dist/*
	rm -rf build/*

install:  pkg
	$(py3)  $(install_cmd)


pkg: clean
	$(py3) $(build_cmd)
	
upload: pkg	
	twine upload dist/*



