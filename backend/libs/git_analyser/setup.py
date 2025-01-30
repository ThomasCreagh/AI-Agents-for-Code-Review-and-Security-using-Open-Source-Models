from setuptools import find_packages, setup

setup(
    name='git_analyser',
    packages=find_packages(include=["git_analyser"]),
    version='0.1.0',
    description='A libarary to help analyse git repos easier',
    author='Sweng25 group 23',
    install_requires=['pydrill==0.3.4'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
