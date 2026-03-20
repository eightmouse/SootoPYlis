![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Target](https://img.shields.io/badge/Target-GBA-orange)
[![Support me on Ko-fi](https://img.shields.io/badge/Support%20Me-Ko--fi-F16061?logo=ko-fi&logoColor=white)](https://ko-fi.com/eightmouse)

# SootoPYlis

SootoPYlis is my attempt to recreate the feel of [PokeSwift](https://github.com/Dimillian/PokeSwift) for Pokemon Emerald in Python.

I'm building it as a native-feeling desktop app with a PySide6/QML shell, a Python gameplay core, and a local import pipeline that works from a user-supplied copy of Pokemon Emerald.

## Inspiration

Credit goes to [Dimillian](https://github.com/Dimillian) for creating [PokeSwift](https://github.com/Dimillian/PokeSwift). That project is the clearest reference for the kind of polished desktop Pokemon experience I want to build here.

## What This Repo Is

Right now this repo contains:

- a PySide6 desktop app shell that mirrors the PokeSwift-style layout for Emerald
- a Python overworld/runtime layer
- a local ROM probe and import/cache flow
- an early Emerald overworld slice with movement, warps, rendering, and background music plumbing

## What This Repo Does Not Ship

I do not include:

- Pokemon Emerald ROMs
- save files or emulator states
- generated runtime caches
- local reference checkouts used during development
- bundled Nintendo assets extracted from a ROM

To run the project, you need to provide your own local copy of Pokemon Emerald.

## Current Development Notes

The project is still in active prototype mode. The desktop shell is already in place, and the current focus is moving from placeholder behavior to accurate Emerald overworld rendering, movement, audio, and eventually battle flow.

At the moment, some development paths still expect a local `pret/pokeemerald` reference checkout under `tmp/pokeemerald-ref` while I continue replacing those pieces with direct ROM-backed extraction.

## Stack

- Python 3.13+
- PySide6
- Qt Quick / QML
- Pillow

## Project Layout

```text
SootoPYlis/
  App/
    SootoPYlisDesktop/
      Sources/
        sootopylis_desktop/
  Sources/
    SootCore/
      sootcore/
    SootUI/
      sootui/
    EmeraldData/
      emeralddata/
    EmeraldExtractor/
      emeraldextractor/
  Tests/
```

## Running It Locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
python run_desktop.py
```

On Windows, launch it with:

```text
open_desktop.bat
```

That launcher prints a few environment checks and then opens the desktop app.
