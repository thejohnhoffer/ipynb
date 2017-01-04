from setuptools import setup

setup(name='nbook',
            version='0.1',
            description='Import nbook files to python',
            url='http://github.com/thejohnhoffer/ipynb',
            author='John Hoffer (thejohnhoffer)',
            author_email='john@hoff.in',
            license='MIT',
            packages=['nbook'],
            install_requires=['nbformat'],
            zip_safe=False)
