. PHONY: all clean html reinstall reqs run test

all: # run `make reqs` once before running this
	make clean
	make reinstall
	make test
	make run
	make html

clean:
	rm -f examples/typical_usage_output.rst
	rm -f examples/typical_usage_toc.txt
	rm -f examples/imported_entries_output.rst
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/

html:
	cp examples/typical_usage_output.rst ../dockstore-documentation/docs/typical_usage_output.rst
	cp examples/imported_entries_output.rst ../dockstore-documentation/docs/imported_entries_output.rst
	cd ../dockstore-documentation/docs/; \
	make html; \
	python -mwebbrowser file:///$$(pwd)/_build/html/typical_usage_output.html; \
	python -mwebbrowser file:///$$(pwd)/_build/html/imported_entries_output.html

reinstall:
	pip3 install -r requirements-dev.txt
	python3 -m pip install types-setuptools # this one is just to stop mypy from complaining
	pip3 uninstall --yes glossarpy
	python3 setup.py bdist_wheel
	pip3 install dist/*-py3-none-any.whl

reqs:
	# install requirements for dockstore-documentation - it's best to do this inside a venv
	# until dockstore-documentation merges 12.1 to develop, we have to manually add attrs==21.4.0
	curl https://raw.githubusercontent.com/dockstore/dockstore-documentation/develop/requirements.txt >> requirements-dev.txt
	echo "attrs==21.4.0\n" >> requirements-dev.txt
	pip3 install -r requirements-dev.txt

run:
	python3 examples/example_typical_usage.py
	python3 examples/example_import_entries.py

test:
	flake8 --ignore E501,E231,E128 glossarpy/glossarpy.py

