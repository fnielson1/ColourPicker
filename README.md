<h1 align="center">
  <img src="pick-colour-picker.png" width="256" alt="Pick">
  <br />
  Pick
</h1>

<p align="center"><b>A colour picker app for Ubuntu and Linux which allows picking any colour on the screen and remembers the last few you picked.</b></p>

![Pick Screenshot](pick-screenshot-16x9.png?raw=true)

<p align="center">Made with 💝 for <img src="https://raw.githubusercontent.com/anythingcodes/slack-emoji-for-techies/gh-pages/emoji/tux.png" align="top" width="24" /></p>

[![Pick](https://snapcraft.io/pick-colour-picker/badge.svg)](https://snapcraft.io/pick-colour-picker) [![Snap Status](https://build.snapcraft.io/badge/stuartlangridge/ColourPicker.svg)](https://build.snapcraft.io/user/stuartlangridge/ColourPicker)

## Building, Testing, and Installation

### Linux

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/pick-colour-picker)

```bash
snap install pick-colour-picker
```

### Source

You'll need the dependencies listed in `pyproject.toml`  
Doing the steps in the **Setup** section below will install them for you.

**For development with a virtual environment:**
```bash
# Remove old venv if it exists
rm -rf .venv

# Create venv and activate it
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
```

#### Setup
```bash
./setup.sh
```

#### Running Pick
```bash
python3 -m pick
```

## Packaging

Both Flatpak and Snap packages use the shared `assets` directory located at the project root (`/assets`). Ensure any asset updates are made in this directory.

## Distribution
Create a build of the project using the following:

```bash
sudo python3 setup.py install
```
A `setup.py` is present, so `python3 setup.py install` is possible, but beware that [uninstalling setup.py-installed apps is not as easy as it should be](https://github.com/stuartlangridge/ColourPicker/issues/62) and prepare accordingly if you plan to use this install method.

#### (Experimental) Building a Wheel or Source Distribution
```bash
pip install build
python -m build
```
