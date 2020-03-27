from setuptools import find_packages, setup
from distutils.util import convert_path

# Imports __version__, reference: https://stackoverflow.com/a/24517154/2220152
ns = {}
ver_path = convert_path('hydrofetch/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), ns)
__version__ = ns['__version__']

setup(
    name='hydrofetch',
    version=__version__,
    url='https://github.com/sblack-usu/hydrofetch',
    license='3-clause BSD',
    author='Scott Black',
    author_email='scott.black@usu.edu',
    description=('Notebook Extension to download hydro data specified in the url.'),
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['notebook>=5.5.0', 'tornado'],
    data_files=[
        ('etc/jupyter/jupyter_notebook_config.d',
         ['jupyterurlparams/etc/jupyterurlparams.json'])
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
