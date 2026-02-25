PY3 = python3
PYPY3 = pypy3

build_cmd = -m build -n
install_cmd = -m pip   install  . --user --no-build-isolation --break-system-packages 


default: install

clean:
	rm -f dist/*
	rm -rf build/*

install: python3

pkg: clean
	$(PY3) $(build_cmd)
	
pypy3: clean
	$(PYPY3) $(build_cmd)
	$(PYPY3) $(install_cmd)	

python3: clean
	$(PY3) $(build_cmd)
	$(PY3)  $(install_cmd)

upload: clean pkg	
	twine upload dist/*



