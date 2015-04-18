from setuptools import setup

def readme():
    return open("README.md").read()

setup(
    name = 'mondb',
    packages = ['mdb'],
    version = '0.0.2',
    long_description= "MODELS for MONGODB",
    description = 'MongoDB Models',
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
    install_requires=['pymongo>=2.8', 'six >= 1.9.0'],
    test_suite="test"
)
