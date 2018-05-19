from setuptools import setup, find_packages
from jong import __version__ as version

install_requires = [
    'arrow',
    'peewee',
    'feedparser',
]

setup(
    name='jong',
    version=version,
    description='JOplin Note Generator',
    long_description='Creating note automatically into Joplin, from your favorites RSS/Atom Feeds',
    author='FoxMaSk',
    maintainer='FoxMaSk',
    author_email='foxmaskhome@gmail.com',
    maintainer_email='foxmaskhome@gmail.com',
    url='https://github.com/foxmask/jong',
    download_url="https://github.com/foxmask/jong/archive/jong-" + version + ".zip",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries'
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=install_requires,
    include_package_data=True,
)
