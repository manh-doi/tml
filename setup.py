import os
from setuptools import setup

version = "0.0.3"

packages = (x[0].replace("./", "").replace("/", ".") for x in
            filter(lambda x: x[2].__contains__("__init__.py"), os.walk("./")))

packages = list(filter(lambda x: "tests" not in x or "slang" not in x, packages))

setup(
    name='m-tml',
    version=version,
    packages=packages,
    url='',
    license='',
    author='manhdoi',
    author_email='manhtran40kc@gmail.com',
    description=''
)
