import ghidra.app.decompiler.*;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;

public class DecompileSpecificFunctions extends GhidraScript {

    private static final String[] ENTRIES = {
        "00028a78",
        "00028c48",
        "00028e14",
        "000194a0",
        "00019888",
        "0001b800",
        "0001838c",
        "00052d74",
        "00052bc0",
        "00052b40",
        "00052b44"
    };

    @Override
    protected void run() throws Exception {
        DecompInterface iface = new DecompInterface();
        iface.openProgram(currentProgram);

        for (String entryStr : ENTRIES) {
            Address entry = toAddr(entryStr);
            Function func = getFunctionAt(entry);
            println("");
            println("=== FUNCTION " + entry + " ===");
            if (func == null) {
                println("not a function");
                continue;
            }
            println("name: " + func.getName());
            DecompileResults res = iface.decompileFunction(func, 60, monitor);
            if (!res.decompileCompleted()) {
                println("decompile failed");
                continue;
            }
            String c = res.getDecompiledFunction().getC();
            println(c);
        }

        iface.dispose();
    }
}
