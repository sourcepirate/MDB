from setuptools import setup

setup(
    name = 'MDB',
    packages = ['mdb'],
    version = '0.0.1',
    description = 'MongoDB Models',
    author='plasmashadow',
    author_email='plasmashadowx@gmail.com',
    url='https://github.com/RevelutionWind/MDB.git',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GLS'
    ],
     install_requires=['pymongo>=2.8', 'six >= 1.9.0']
)
