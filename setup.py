from nopilot import __version__
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="nopilot",
    version=__version__,
    author="jmsdnns",
    author_email="jdennis@gmail.com",
    description="we aint need no stinkin copilot. how about no pilot?",
    long_description=long_description,
    url="http://github.com/jmsdnns/nopilot",
    install_requires=["openai", "python-dotenv"],
    extras_require={
        "dev": [
            "black",
        ]
    },
    entry_points={
        "console_scripts": [
            "nopilot = nopilot.cli:run",
        ]
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
