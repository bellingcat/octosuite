import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="octosuite",
    version="2.2.3",
    author="Richard Mwewa",
    author_email="rly0nheart@duck.com",
    packages=["octosuite"],
    description="Advanced Github OSINT Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rly0nheart/octosuite",
    license="GNU General Public License v3 (GPLv3)",
    install_requires=["requests", "rich"],
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
            "octosuite=octosuite.main:onStart",
        ]
    },
)
