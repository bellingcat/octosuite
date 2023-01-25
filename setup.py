import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="octosuite",
    version="3.1.0",
    author="Richard Mwewa",
    author_email="rly0nheart@duck.com",
    packages=["octosuite"],
    description="Advanced Github OSINT Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bellingcat/octosuite",
    license="GNU General Public License v3 (GPLv3)",
    install_requires=["requests", "rich", "psutil", "pyreadline3"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
        ],
    entry_points={
        "console_scripts": [
            "octosuite=octosuite.main:octosuite",
        ]
    },
)
