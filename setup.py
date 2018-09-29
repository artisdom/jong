from setuptools import setup, find_packages
from jong import __version__ as version

install_requires = [
    'arrow==0.12.1',
    'asks==2.0.0',
    'Django>=2.1,<3.0',
    'django-environ==0.4.5',
    'feedparser==5.2.1',
    'pypandoc==1.4',
    'requests==2.18.4',
    'trio==0.4.0',
]

setup(
    name='jong',
    version=version,
    description='JOplin Notes Generator',
    long_description=open('README.md').read(),
    author='FoxMaSk',
    maintainer='FoxMaSk',
    author_email='foxmask at protonmail',
    maintainer_email='foxmask at protonmail',
    url='https://github.com/foxmask/jong',
    download_url="https://github.com/foxmask/jong/archive/jong-" + version + ".zip",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Topic :: Internet',
        'Topic :: Communications',
        'Topic :: Database',
    ],
    install_requires=install_requires,
    include_package_data=True
)
