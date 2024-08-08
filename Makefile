.PHONY: all

all: clean package uninstall install clean

package:
	python -m build


uninstall:
	pip uninstall m-tml


install:
	pip install dist/m_tml-0.0.2-py3-none-any.whl


doc:
	cd docs && make html

clean:
	rm -rf build && rm -rf dist && rm -rf m_tml.egg-info
