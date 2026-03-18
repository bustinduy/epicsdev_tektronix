# epicsdev_tektronix
Python-based EPICS PVAccess server for Tektronix MSO oscilloscopes (4, 5, and 6 Series).

It is based on [p4p](https://epics-base.github.io/p4p/) and [epicsdev](https://github.com/ASukhanov/epicsdev) packages 
and it can run standalone on Linux, OSX, and Windows platforms.

This implementation is adapted from [epicsdev_rigol_scope](https://github.com/ASukhanov/epicsdev_rigol_scope) 
and supports Tektronix MSO series oscilloscopes using SCPI commands as documented in the 
[Tektronix 4-5-6 Series MSO Programmer Manual](https://download.tek.com/manual/4-5-6-Series-MSO-Programmer_077130524.pdf).

## Installation
This project requires Python 3.11 or newer.

The defaults in this repository are currently tailored for a local Tektronix
MSO44B setup with:
- 4 channels
- VISA resource `TCPIP::192.168.2.194::4000::SOCKET`

Recommended local setup from a clone of the repository:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

`requirements.txt` installs the full local environment:
- core runtime dependencies for the server
- GUI and plotting packages used by the repository config files
- the missing GUI pieces required by `pypeto` and `pvplot`: `PyQt5` and `pyqtgraph`

If you only want the server package without the GUI tools:

```bash
python -m pip install .
```

If you want the optional GUI stack when installing from package metadata:

```bash
python -m pip install ".[gui]"
```

For editable installs, use plain `python -m pip install -e .`. Do not add
`--no-build-isolation` unless you also manage the build backend dependencies
yourself.

## Smoke Test
Run the hardware-free smoke test after installation:

```bash
python demo/smoke_demo.py
```

To also verify the GUI stack:

```bash
python demo/smoke_demo.py --check-gui
```

The smoke test checks that:
- the core Python dependencies import correctly
- the package can build its PV definition table without a real instrument
- the GUI modules import correctly when `--check-gui` is enabled

## Features
- Support for Tektronix MSO oscilloscopes (configurable)
- Real-time waveform acquisition via EPICS PVAccess
- SCPI command interface for scope control
- Support for multiple trigger modes (AUTO, NORMAL, SINGLE)
- Configurable horizontal and vertical scales
- Channel-specific controls (coupling, offset, termination)
- Performance timing diagnostics

## Command-line Options
- `-a, --autosave`: Autosave control
- `-c, --recall`: if given: disable recalling of autosaved PVs 
- `-C, --channels`: Number of channels per device (default: 4)
- `-d, --device`: Device name for PV prefix (default: 'tektronix')
- `-i, --index`: Device index for PV prefix (default: '0')
- `-r, --resource`: VISA resource string (default: 'TCPIP::192.168.2.194::4000::SOCKET')
- `-v, --verbose`: Increase verbosity (-vv for debug output)

## Example Usage
```bash
python -m epicsdev_tektronix.mso -r 'TCPIP::192.168.2.194::4000::SOCKET'
```




Control GUI:

```bash
python -m pypeto -c config -f epicsdev_tektronix
```

## Supported Tektronix Models
- MSO44, MSO46, MSO48 (4 Series)
- MSO54, MSO56, MSO58 (5 Series)
- MSO64 (6 Series)
- Other MSO series models using compatible SCPI commands

## Performance
Acquisition time of 6 channels, each with 1M of floating point values is 2.0 s. Throughput maxes out at 12 MB/s.
