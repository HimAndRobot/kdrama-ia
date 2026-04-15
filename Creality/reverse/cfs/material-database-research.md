# CFS Material Database Research

This note documents the path used to reach the real CFS material database and confirm how Creality resolves generic materials such as `PLA`, `PETG`, `ASA`, and related variants.

## Goal

The goal was to answer three concrete questions:

1. Where does the printer get the purge / target nozzle temperatures used by the CFS flow.
2. Whether those temperatures are hardcoded in the socket flow or resolved from a local database.
3. How to map generic material selections from the UI flow to the data stored on the printer.

## Initial Hypothesis

The first suspect was the high-level CFS command flow exposed by Creality, especially commands such as:

- `BOX_START_PRINT_EXTRUDE_MATERIAL`
- `BOX_EXTRUDE_MATERIAL`
- `BOX_CUT_MATERIAL`

These commands are not plain Klipper macros. They are implemented in proprietary Creality extensions.

## What Was Analyzed

Files used during the investigation:

- `box_wrapper.cpython-38-mipsel-linux-gnu.so`
- `box_wrapper.disasm.txt`
- `serial_485_wrapper.cpython-38-mipsel-linux-gnu.so`
- `serial_485_wrapper.disasm.txt`
- `box.py`
- `serial_485.py`
- `klippy-tail-2000.log`

Live data pulled from the printer:

- `live/material_database.json`

## Important Finding: Not Encrypted

The `box_wrapper` module was not encrypted. It is a stripped native shared object:

- ELF 32-bit
- MIPS
- generated from Cython

Important embedded symbols and strings were still visible through static inspection:

- `extras.box_wrapper.BoxAction.get_material_target_temp`
- `extras.box_wrapper.BoxAction.get_flush_temp`
- `material database get nozzle temp: %s`
- `material database get material name: %s`
- `get next material temp: %d`
- `flush_temp: %d`

This mattered because it proved the correct path was not “decrypting firmware”, but rather:

1. static string/symbol analysis
2. disassembly
3. live file extraction from the printer

## Why `box_wrapper` Was The Right Target

The CFS transport layer exists lower down in `serial_485_wrapper`, but the temperature selection logic was clearly higher level.

The strongest indicators were the `BoxAction` symbols related to material lookup:

- `get_material_target_temp`
- `get_flush_temp`

These names directly matched the behavior being investigated.

## The Critical Breakthrough

Inside `box_wrapper`, the following path string was found:

- `creality/userdata/box/material_database.json`

That established that the real material data was file-backed and likely readable directly from the printer filesystem.

## Live Extraction

The file was then pulled from the printer over SSH and stored locally as:

- `reverse/cfs/live/material_database.json`

That file is the real source of truth for the generic material profiles used by the proprietary CFS stack.

## What The Database Contains

Each entry contains:

- `base.id`
- `base.meterialType`
- `base.brand`
- `base.name`
- `base.minTemp`
- `base.maxTemp`
- `kvParam.nozzle_temperature`
- `kvParam.nozzle_temperature_initial_layer`
- `kvParam.nozzle_temperature_range_low`
- `kvParam.nozzle_temperature_range_high`

This immediately explained why temperatures such as:

- `PLA -> 220/240`
- `PETG -> 250/270`

were appearing in the flow.

They already existed in the material database.

## Confirmed Generic IDs

The generic entries confirmed in the database are:

- `00001` -> `Generic PLA`
- `00002` -> `Generic PLA-Silk`
- `00003` -> `Generic PETG`
- `00004` -> `Generic ABS`
- `00005` -> `Generic TPU`
- `00006` -> `Generic PLA-CF`
- `00007` -> `Generic ASA`
- `00008` -> `Generic PA`
- `00009` -> `Generic PA-CF`
- `00010` -> `Generic BVOH`
- `00011` -> `Generic PVA`
- `00012` -> `Generic HIPS`
- `00013` -> `Generic PET-CF`
- `00014` -> `Generic PETG-CF`
- `00015` -> `Generic PA6-CF`
- `00016` -> `Generic PAHT-CF`
- `00017` -> `Generic PPS`
- `00018` -> `Generic PPS-CF`
- `00019` -> `Generic PP`
- `00020` -> `Generic PET`
- `00021` -> `Generic PC`

## How It Was Proven At Runtime

After locating the file, live edits were made directly in `material_database.json` on the printer.

Changing the temperatures in the matching generic entry changed the temperatures actually used by the CFS flow.

This confirmed that:

- the proprietary flow does resolve through `material_database.json`
- the database is not only descriptive metadata
- editing the file changes runtime behavior

## Relationship To Socket Payloads

The `modifyMaterial` socket payload used by the Creality UI and by the injected Mainsail panel includes fields such as:

- `type`
- `vendor`
- `name`
- `minTemp`
- `maxTemp`
- `pressure`
- `rfid`

During capture and replay work, it became clear that:

- `rfid` is not the database ID
- `db_id` used by the generic material database is a separate concept

The generic database ID is what must be used when editing `material_database.json`.

## Practical Conclusion

To persist purge or generic material temperatures, the reliable path is:

1. resolve the generic material database ID
2. edit the matching entry in `material_database.json`
3. write the file back on the printer

That is why the custom Klipper-side helper was built later: to update the database directly instead of trying to force the entire behavior through the WebSocket layer.

## Final Conclusion

The path to the material database was:

1. inspect `box_wrapper`
2. search for temperature-related symbols and strings
3. find the embedded `material_database.json` path
4. pull the file live from the printer via SSH
5. edit the file and verify that the CFS behavior changes

So the real answer was not “decrypt the binary”.

The real answer was:

- static reverse engineering of `box_wrapper`
- plus live extraction and validation of `material_database.json`

That gave a complete and practical route from proprietary wrapper to editable runtime material data.
