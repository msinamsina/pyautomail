from setuptools import setup, find_packages

setup(
    name='pyautomail',
    version='1.5.0',
    packages=find_packages(),
    url='https://github.com/msinamsina/automail',
    license='MIT',
    author='Mohammad sina Allahkaram',
    author_email="msinamsina@gmail.com",
    description='A Python pkg and command-line interface for Sending email to your contact list',
    install_requires=[
        'sqlalchemy',
        'sqlalchemy_utils',
        'jinja2',
        'pandas'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'automail = automail.manager:main',
        ],
    },
)


