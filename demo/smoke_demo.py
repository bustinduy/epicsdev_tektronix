#!/usr/bin/env python3
"""Hardware-free smoke test for the epicsdev_tektronix package."""

from __future__ import annotations

import argparse
from types import SimpleNamespace


def import_core_dependencies() -> dict[str, str]:
    """Import the core runtime dependencies and return their versions."""
    versions: dict[str, str] = {}
    for module_name in ("numpy", "pyvisa", "p4p", "psutil", "epicsdev"):
        module = __import__(module_name)
        versions[module_name] = getattr(module, "__version__", "unknown")
    return versions


def build_pv_definitions(channels: int) -> tuple[int, list[str]]:
    """Create PV definitions without talking to a real instrument."""
    from epicsdev_tektronix import mso

    mso.pargs = SimpleNamespace(
        resource="TCPIP::192.168.1.100::5025::SOCKET",
        channels=channels,
        channelList=[f"CH{i + 1}" for i in range(channels)],
    )

    pv_defs = mso.myPVDefs()
    pv_names = [pv_def[0] for pv_def in pv_defs]
    required_names = {
        "visaResource",
        "timePerDiv",
        "trigSource",
        "c01Waveform",
        f"c{channels:02}Waveform",
    }
    missing = sorted(required_names.difference(pv_names))
    if missing:
        raise RuntimeError(f"Missing expected PV definitions: {missing}")
    return len(pv_defs), pv_names


def import_gui_dependencies() -> dict[str, str]:
    """Import the optional GUI modules and return their versions."""
    versions: dict[str, str] = {}
    for module_name in ("PyQt5", "pyqtgraph", "pypeto", "pvplot"):
        module = __import__(module_name)
        versions[module_name] = getattr(module, "__version__", "unknown")
    return versions


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--channels",
        type=int,
        default=6,
        help="Number of scope channels to synthesize in the PV definition check.",
    )
    parser.add_argument(
        "--check-gui",
        action="store_true",
        help="Also require pypeto, pvplot, pyqtgraph, and a Qt binding to import.",
    )
    args = parser.parse_args()

    try:
        core_versions = import_core_dependencies()
        pv_count, _ = build_pv_definitions(args.channels)
    except ModuleNotFoundError as exc:
        raise SystemExit(
            f"Missing dependency '{exc.name}'. Install the current requirements with "
            "'python -m pip install -r requirements.txt' and re-run the smoke test."
        ) from exc

    print("Core imports OK:")
    for module_name, version in core_versions.items():
        print(f"  - {module_name} {version}")
    print(f"PV definition generation OK: {pv_count} PVs for {args.channels} channels")

    if args.check_gui:
        try:
            gui_versions = import_gui_dependencies()
        except ModuleNotFoundError as exc:
            raise SystemExit(
                f"Missing GUI dependency '{exc.name}'. Install the GUI stack with "
                "'python -m pip install -r requirements.txt' and re-run with --check-gui."
            ) from exc
        print("GUI imports OK:")
        for module_name, version in gui_versions.items():
            print(f"  - {module_name} {version}")
    else:
        print("GUI import check skipped. Re-run with --check-gui after installing GUI packages.")


if __name__ == "__main__":
    main()
