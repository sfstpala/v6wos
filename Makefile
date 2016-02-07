python ?= python3.5
package = c24

all: $(package).egg-info
$(package).egg-info: setup.py bin/pip
	bin/pip install --upgrade --editable . && touch $@
bin/pip: bin/python
	bin/pip install --upgrade setuptools pip
bin/python:
	$(python) -m venv .

test: all bin/coverage bin/pylama bin/check-manifest bin/rst2xml.py
	bin/coverage run setup.py test
	bin/coverage html
	bin/coverage report --fail-under=100
	bin/pylama setup.py $(package)
	bin/check-manifest || ! test -d .git
	bin/python setup.py check -mrs
	bin/pip list --outdated
bin/coverage: bin/pip
	bin/pip install --upgrade coverage
bin/pylama: bin/pip
	bin/pip install --upgrade pylama pyflakes
bin/check-manifest: bin/pip
	bin/pip install --upgrade check-manifest
bin/rst2xml.py: bin/pip
	bin/pip install --upgrade docutils

debug: all debug.yaml
	bin/$(package) --debug --config=debug.yaml
debug.yaml:
	cp c24/config/debug.yaml .

clean:
	rm -rf *.egg-info $(shell find $(package) -name "__pycache__")
	rm -rf bin lib lib64 include pip-selfcheck.json pyvenv.cfg
	rm -rf build dist wheelhouse .coverage htmlcov
