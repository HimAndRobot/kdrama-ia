# Creality Reverse Engineering Notes

This directory documents an initial reverse-engineering workflow for proprietary Creality Klipper extensions running on a K1C-class printer.

## Goal

The first goal was not to change printer behavior in a risky way. It was to prove that we could:

1. Identify the real runtime implementation of a proprietary command.
2. Extract the active files from the printer.
3. Rebuild them locally in a format accepted by the printer.
4. Deploy a harmless test modification.
5. Confirm that the modified code path was actually executed on the device.

## Target Command

The first command investigated was:

`CX_ROUGH_G28`

This command is available from the printer CLI and from the Creality interface, but it is not defined as a plain text macro in the usual user config files.

## What We Found

- `CX_ROUGH_G28` is registered inside Klipper runtime, not only in Creality UI code.
- The active implementation is in:
  - `/usr/share/klipper/klippy/extras/custom_macro.py`
  - `/usr/share/klipper/klippy/extras/custom_macro.pyc`
- The handler is `cmd_CX_ROUGH_G28`.
- The command calls:
  - temperature preparation
  - `change_hot_min_temp(...)` on a `prtouch` object when available
  - `run_script_from_command('G28')`

## Local Directory Layout

- `backup/`
  - untouched copies pulled from the printer
- `work/`
  - editable working copies
- `compare/`
  - locally rebuilt `.pyc` files used to compare output against the originals

## Step-By-Step Workflow

### 1. Identify the active implementation

We searched the runtime command registry and the installed Klipper extensions until we found that `CX_ROUGH_G28` belongs to `custom_macro.pyc`.

### 2. Pull original files from the printer

We copied both the source and bytecode versions to the local machine:

- original source: `backup/custom_macro.py`
- original bytecode: `backup/custom_macro.pyc`

We also created working copies:

- editable source: `work/custom_macro.py`
- initial bytecode copy: `work/custom_macro.pyc`

### 3. Validate source vs active bytecode

We compared the local source copy against the bytecode pulled from the printer.

Important checks:

- same function name: `cmd_CX_ROUGH_G28`
- same first source line
- same referenced names
- same relevant string constants
- same command sequence, including `G28`

This confirmed that the local source copy matches the active runtime logic.

### 4. Install a local Python 3.8 toolchain

The printer runs Python 3.8, so generating a deployable `.pyc` with Python 3.9 would not be safe.

We installed:

- `pyenv`
- local `Python 3.8.20`

This allowed us to generate Python 3.8-compatible `.pyc` files locally.

### 5. Recompile the original file locally

We rebuilt the original `custom_macro.py` using Python 3.8 and compared it to the bytecode pulled from the printer.

Result:

- the function-level bytecode for `cmd_CX_ROUGH_G28` matched
- remaining binary differences were only header metadata differences, such as timestamp/header bytes

This proved the local rebuild path is correct.

### 6. Add a harmless test change

We inserted a single CLI-visible debug message into `cmd_CX_ROUGH_G28` before the final `G28` call:

```python
gcmd.respond_info(
    "[CX_ROUGH_G28] ext_temp=%s bed_temp=%s leveling=%s" % (
        self.g28_ext_temp, self.bed_temp, self.leveling_calibration
    )
)
```

This was intentionally chosen because it:

- does not alter motion behavior
- is easy to confirm from the CLI
- proves the modified code path is active

### 7. Rebuild the modified bytecode locally

We recompiled the modified source with local Python 3.8 and generated a deployable `.pyc`.

Artifacts:

- rebuilt original bytecode: `compare/orig/custom_macro.dfile.pyc`
- rebuilt modified bytecode: `compare/mod/custom_macro.dfile.pyc`

### 8. Back up the printer-side files

Before deployment, we created remote backups on the printer:

- `custom_macro.py.bak_<timestamp>`
- `custom_macro.pyc.bak_<timestamp>`

### 9. Deploy the test change

We copied both the modified `.py` and `.pyc` to the printer.

Copying both matters because Python may ignore a standalone `.pyc` if the source file timestamp/path state does not match expectations.

### 10. Validate on the printer

After restart/testing, the CLI showed:

```text
[CX_ROUGH_G28] ext_temp=150.0 bed_temp=50.0 leveling=1
use prtouch_v2
CX_ROUGH_G28
```

This confirmed:

- the printer accepted the locally rebuilt Python 3.8 bytecode
- the modified code path was loaded and executed
- the reverse-engineering and rebuild pipeline is viable

## Current Status

The initial end-to-end validation is complete.

We now have a confirmed workflow for:

- extracting active Creality Klipper extension files
- comparing source and bytecode locally
- rebuilding compatible Python 3.8 bytecode
- deploying controlled test patches
- validating execution through the printer CLI

## Next Logical Targets

- trace the full `G28` path after `cmd_CX_ROUGH_G28`
- inspect `prtouch`, `prtouch_v2`, and related wrappers
- identify where Creality-specific homing behavior diverges from upstream Klipper
- make behavior changes only after confirming the exact downstream execution path
