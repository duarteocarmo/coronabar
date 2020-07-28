from setuptools import setup, find_packages
import sys

APP = []
DATA_FILES = []
OPTIONS = {}
SETUP = []
INSTALL = []
SCRIPT = []
PACKAGES = []

if sys.platform.startswith("darwin"):
    APP = ["app.py"]
    DATA_FILES = []
    OPTIONS = {
        "py2app": {
            "argv_emulation": True,
            "iconfile": "icon.icns",
            "plist": {
                "CFBundleShortVersionString": "0.2.0",
                "LSUIElement": True,
            },
            "packages": ["rumps", "requests"],
        }
    }
    SETUP = ["py2app"]
    INSTALL = ["rumps", "requests"]
    SCRIPT = []
elif sys.platform.startswith("linux"):
    APP = ["app.py"]
    DATA_FILES = []
    SETUP = []
    SCRIPT = ["bin/coronabar"]
    PACKAGES = find_packages()


setup(
    app=APP,
    name="CoronaBar",
    packages=PACKAGES,
    data_files=DATA_FILES,
    options=OPTIONS,
    setup_requires=SETUP,
    install_requires=INSTALL,
    include_package_data=True,
    scripts=SCRIPT,
)
