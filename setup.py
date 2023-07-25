from setuptools import setup, find_packages

setup(
    name='automail',
    version='1.1.1',
    packages=find_packages(),
    url='https://github.com/msinamsina/sending-gmail',
    license='MIT',
    author='Mohammad sina Allahkaram',
    author_email="msinamsina@gmail.com",
    description='A python package for sending E-mails',
    install_requires=[
        'sqlalchemy',
        'sqlalchemy_utils',
        'jinja2',
        'pandas'
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'automail = automail.manager:main',
        ],
    },
)


