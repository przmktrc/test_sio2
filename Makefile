install: uninstall configure runner
	ln -s $(shell pwd)/test_sio2 ~/bin/test_sio2

uninstall:
	if [ -L ~/bin/test_sio2 ]; then rm -f ~/bin/test_sio2; fi


configure: path_to_here


path_to_here:
	echo "path_to_here: str = \"$(shell pwd)\"" > path_to_here.py


runner:
	echo "python $(shell pwd)/src/test_sio2.py \"\$$@\"" > test_sio2
	chmod +x test_sio2


clean:
	rm -rf __pycache__ src/__pycache__ .mypy_cache src/.mypy_cache test_sio2
