from ghidra.app.decompiler import DecompInterface
from ghidra.program.model.listing import CodeUnit


TARGETS = [
    "cmd_send_data_with_response",
    "raw_send_wait_ack",
    "raw_send",
    "extrude_process",
    "retrude_process",
    "set_motor_speed",
    "set_box_mode",
    "get_buffer_state",
    "get_filament_sensor_state",
]


def iter_string_data():
    listing = currentProgram.getListing()
    data_iter = listing.getDefinedData(True)
    while data_iter.hasNext() and not monitor.isCancelled():
        data = data_iter.next()
        value = data.getValue()
        if isinstance(value, unicode):
            yield data, value


def find_target_strings():
    found = []
    for data, value in iter_string_data():
        for target in TARGETS:
            if target in value:
                found.append((target, data, value))
                break
    return found


def decompile_function(func):
    iface = DecompInterface()
    iface.openProgram(currentProgram)
    res = iface.decompileFunction(func, 60, monitor)
    if not res.decompileCompleted():
        return None
    return res.getDecompiledFunction().getC()


def main():
    refs = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()
    found = find_target_strings()
    seen_funcs = set()

    print("=== TARGET STRINGS ===")
    for target, data, value in found:
        addr = data.getAddress()
        print("\n[%s] @ %s" % (target, addr))
        print("string: %s" % value)
        xrefs = list(refs.getReferencesTo(addr))
        if not xrefs:
            print("  no xrefs")
            continue

        for ref in xrefs:
            from_addr = ref.getFromAddress()
            func = getFunctionContaining(from_addr)
            if func is None:
                code_unit = listing.getCodeUnitAt(from_addr)
                text = code_unit.toString() if code_unit else "no code unit"
                print("  xref from %s (no func): %s" % (from_addr, text))
                continue

            key = func.getEntryPoint().toString()
            print("  xref from %s -> func %s @ %s" % (
                from_addr, func.getName(), func.getEntryPoint()))
            if key in seen_funcs:
                continue
            seen_funcs.add(key)
            c_text = decompile_function(func)
            if c_text is None:
                print("    decompile failed")
                continue
            print("---- DECOMPILE START %s ----" % func.getName())
            print(c_text[:5000])
            print("---- DECOMPILE END %s ----" % func.getName())


if __name__ == "__main__":
    main()
