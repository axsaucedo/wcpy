from setuptools import setup, Command, find_packages
import os
import pywc

currentFileDirectory = os.path.dirname(__file__)
with open(os.path.join(currentFileDirectory, "README.md"), "r") as f:
    readme = f.read()


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./**/__pycache__ ./.eggs ./.cache')


print(find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]))

setup(
    name="pywc",
    version=pywc.VERSION,
    description="Count the number of words in a folder",
    long_description=readme,
    author="Alejandro Saucedo",
    author_email="a@e-x.io",
    url="https://github.com/axsauze/pywc",
    classifiers=[
        "Development Status :: 3 - Alpha Development Status"
        "Intended Audience :: Developers",
        "Programming Language :: Python 3",
        "Programming Language :: Python 3.2",
        "Programming Language :: Python 3.3",
    ],
    keywords="Word count (wc) on steroids",
    license="MIT",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    scripts=('pywc.py',),
    data_files=[ (".", ["LICENSE"]) ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    cmdclass={
        'clean': CleanCommand
    }
)
