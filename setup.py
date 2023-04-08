from setuptools import setup, find_packages

setup(
    name='pm2',
    version='1.0.0',
    description='pm2 for python',
    author='cryatt',
    url='https://github.com/Gaming552/pm2',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # idk
    ],
    entry_points={
        'console_scripts': [
            'my-command=my_library.cli:main',
        ],
    },
)
