from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path


# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)


here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pushetta',

    version='1.0.15',

    description='Client for Pushetta API',
    long_description=long_description,

    url='https://github.com/guglielmino/pushetta-py',
    download_url = 'https://github.com/guglielmino/pushetta-py/archive/master.zip',

    author='Fabrizio Guglielmino',
    author_email='guglielmino@gumino.com',

    license='MIT',

    classifiers=[

        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Monitoring',


        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    keywords='pushetta push notifications',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        "future",
        "paho-mqtt",
    ],
)
