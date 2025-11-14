from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="supermock",
    version="0.2.0",
    author="SuperMock Team",
    description="Local Telegram Bot API Mock Server for testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/infernasel/SuperMock-1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "flask>=2.0.0",
        "requests>=2.25.0",
        "pyyaml>=5.4.0",
        "flask-socketio>=5.3.0",
        "flask-cors>=4.0.0",
        "python-socketio>=5.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-asyncio>=0.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "supermock=supermock.cli:main",
        ],
    },
)
