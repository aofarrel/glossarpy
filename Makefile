. PHONY: all build clean html lint reinstall-local reqs run test

all: # run `make reqs` once before running this
	make clean
	make reinstall-local
	make lint
	make test
	make html

build:
	# prepare for uploading to pypi
	make clean
	python3 -m pip install --upgrade build
	python3 -m build
	# when ready, twine upload dist/*

clean:
	rm -f examples/typical_usage_output.rst
	rm -f examples/typical_usage_toc.txt
	rm -f examples/imported_entries_output.rst
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/

html:
	# assumes dockstore-documentation exists on same level as this repo, see readme
	#
	# 1. copy the rst files to dockstore-documentation repo
	# be careful not to commit these test files to dockstore-documentation!
	cp examples/typical_usage_output.rst ../dockstore-documentation/docs/typical_usage_output.rst
	cp examples/imported_entries_output.rst ../dockstore-documentation/docs/imported_entries_output.rst

	# 2. run dockstore-documention's version of `make html`
	# this will also include the processing of dictionary.rst if it is present in dockstore-documentation
	cd ../dockstore-documentation/docs/; \
	make html; \
	python -mwebbrowser file:///$$(pwd)/_build/html/typical_usage_output.html; \
	python -mwebbrowser file:///$$(pwd)/_build/html/imported_entries_output.html; \
	python -mwebbrowser file:///$$(pwd)/_build/html/dictionary.html

lint:
	flake8 --ignore E501,E231,E128,W503 glossarpy/GlossTxt.py
	flake8 --ignore E501,E231,E128,W503 glossarpy/GlossEntry.py
	flake8 --ignore E501,E231,E128,W503 glossarpy/GreatGloss.py
	mypy glossarpy/GlossTxt.py
	#mypy glossarpy/GlossEntry.py  # mypy struggles with the import due to how this is packaged
	#mypy glossarpy/GreatGloss.py  # mypy struggles with the import due to how this is packaged
	mypy --ignore-missing-imports examples/example_typical_usage.py
	mypy --ignore-missing-imports examples/example_import_entries.py

reinstall-local:
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

test:
	python3 examples/example_typical_usage.py
	python3 examples/example_import_entries.py

