import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name='etupem',
    version='0.2.0',
    license='MIT',
    description='Easy To Understand Python Error Message',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['etupem'],
    install_requires=['colorama'],
    entry_points={'console_scripts': ['pythonja=etupem.ja:runner']},
    url='https://github.com/nodai2hITC/etupem/',
    author='nodai2hITC',
    author_email='nodai2h.itc@gmail.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
