from setuptools import setup, find_packages
setup(
    name='pyautomail',
    version='1.7.0.3',
    packages=find_packages(),
    url='https://github.com/msinamsina/pyautomail',
    license='MIT',
    author='Mohammad sina Allahkaram',
    author_email="msinamsina@gmail.com",
    description='Automated Email Sending for Large Scale Email and Gmail Automation',
    install_requires=[
        'sqlalchemy',
        'sqlalchemy_utils',
        'jinja2',
        'pandas',
        'coloredlogs',
        'pytest',
        'typer'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'pyautomail = pyautomail.__main__:main',
            'pyautomail-manager = pyautomail.manager:main'
        ],
    },
)
