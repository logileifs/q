clean:
	rm -rf build/

build: clean
	mkdir build
	cd .. && python -m zipapp controlant/ -p='/usr/bin/env python' -o=controlant/build/q.zip

install:
	pip install -r requirements --target ./lib/
