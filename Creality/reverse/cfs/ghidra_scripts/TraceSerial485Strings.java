// Finds target strings, prints xrefs, and decompiles containing functions.

import java.util.*;

import ghidra.app.decompiler.*;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.mem.MemoryAccessException;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import ghidra.program.model.symbol.ReferenceManager;

public class TraceSerial485Strings extends GhidraScript {

    private static final String[] TARGETS = new String[] {
        "cmd_send_data_with_response",
        "raw_send_wait_ack",
        "raw_send",
        "extrude_process",
        "retrude_process",
        "set_motor_speed",
        "set_box_mode",
        "get_buffer_state",
        "get_filament_sensor_state",
        "cmd_485_send_data_with_response timeout",
        "serial_485_wrapper_connect_send_data_break_reconnect: params = ",
        "do not get response, retries = %d, cmd = %s",
        "Waiting for response, retry = ",
        "BOX_MODIFY_TN_DATA ADDR=%d PART=state DATA=disconnect"
    };

    @Override
    protected void run() throws Exception {
        Listing listing = currentProgram.getListing();
        ReferenceManager refman = currentProgram.getReferenceManager();
        Set<String> seenFuncs = new HashSet<>();

        DecompInterface iface = new DecompInterface();
        iface.openProgram(currentProgram);

        println("=== TARGET STRINGS ===");

        DataIterator it = listing.getDefinedData(true);
        while (it.hasNext() && !monitor.isCancelled()) {
            Data data = it.next();
            Object value = data.getValue();
            if (!(value instanceof String)) {
                continue;
            }
            String s = (String) value;
            String matched = null;
            for (String target : TARGETS) {
                if (s.contains(target)) {
                    matched = target;
                    break;
                }
            }
            if (matched == null) {
                continue;
            }

            Address addr = data.getAddress();
            println("");
            println("[" + matched + "] @ " + addr);
            println("string: " + s);

            ReferenceIterator refs = refman.getReferencesTo(addr);
            if (!refs.hasNext()) {
                println("  no xrefs");
                continue;
            }

            while (refs.hasNext()) {
                Reference ref = refs.next();
                Address from = ref.getFromAddress();
                Function func = getFunctionContaining(from);
                if (func == null) {
                    CodeUnit cu = listing.getCodeUnitAt(from);
                    println("  xref from " + from + " (no func): " + (cu != null ? cu.toString() : "no code unit"));
                    continue;
                }

                println("  xref from " + from + " -> func " + func.getName() + " @ " + func.getEntryPoint());

                String key = func.getEntryPoint().toString();
                if (seenFuncs.contains(key)) {
                    continue;
                }
                seenFuncs.add(key);

                DecompileResults res = iface.decompileFunction(func, 60, monitor);
                if (!res.decompileCompleted()) {
                    println("---- DECOMPILE FAILED " + func.getName() + " ----");
                    continue;
                }

                String c = res.getDecompiledFunction().getC();
                if (c.length() > 5000) {
                    c = c.substring(0, 5000);
                }
                println("---- DECOMPILE START " + func.getName() + " ----");
                println(c);
                println("---- DECOMPILE END " + func.getName() + " ----");
            }
        }
        iface.dispose();
    }
}
