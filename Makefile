python ?= python3.6
package = v6wos

all: $(package).egg-info
$(package).egg-info: setup.py bin/pip
	bin/python -m pip install --editable . && touch $@
bin/pip: bin/python
	curl https://bootstrap.pypa.io/get-pip.py | bin/python
bin/python:
	$(python) -m venv . --without-pip

test: all bin/coverage bin/pylama bin/check-manifest bin/rst2xml.py
	bin/coverage run setup.py test
	bin/coverage html
	bin/coverage report --fail-under=100
	bin/pylama setup.py $(package)
	bin/check-manifest || ! test -d .git
	bin/python setup.py check -mrs
	bin/pip list --format=legacy --outdated
bin/coverage: bin/pip
	bin/pip install --upgrade coverage
bin/pylama: bin/pip
	bin/pip install --upgrade pylama pyflakes
bin/check-manifest: bin/pip
	bin/pip install --upgrade check-manifest
bin/rst2xml.py: bin/pip
	bin/pip install --upgrade docutils

integration-test: all debug.yaml
	bin/python -m v6wos.tests.integration debug.yaml
debug: all debug.yaml
	bin/$(package) --debug --config=debug.yaml
debug.yaml:
	cp v6wos/config/debug.yaml .

clean:
	rm -rf *.egg-info $(shell find $(package) -name "__pycache__")
	rm -rf bin lib lib64 include pip-selfcheck.json pyvenv.cfg
	rm -rf build dist wheelhouse .coverage htmlcov .tox
