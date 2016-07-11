from setuptools import setup

def readme():
    return open("README.md", "r").read()

setup(
    name = 'mondb',
    packages = ['mondb', 'mondb/urltools', 'mondb/Query'],
    version = '0.0.5.2',
    long_description= readme(),
    description = "MODELS for MONGODB",
    author='plasmashadow',
    author_email='plasmashadowx@gmail.com',
    url='https://github.com/RevelutionWind/MDB.git',
    license="BSD 2-Claus",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
    ],
    install_requires=['six', 'motor', 'mock', 'tornado'],
    test_suite="test"
)
