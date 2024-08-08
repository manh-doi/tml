.PHONY: all

all: package uninstall install

package:
	rm -rf build && rm -rf dist && rm -rf m_tml.egg-info && python -m build --wheel


uninstall:
	pip uninstall m-tml


install:
	pip install dist/m_tml-0.0.2-py3-none-any.whl


doc:
	cd docs && make html

