from setuptools import find_packages, setup

setup(
    name="zcl",
    version="0.0.1",
    description="Library implementing a ZigBee stack",
    url="http://github.com/jimmo/python-zcl",
    author="Jim Mussared",
    author_email="jim.mussared@gmail.com",
    license="MIT",
    packages=find_packages(exclude=['*.tests']),
    install_requires=[
    ],
    tests_require=[
    ],
)
