import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;

public class DecompileArgs extends GhidraScript {
    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length == 0) {
            throw new RuntimeException("Usage: DecompileArgs.java <function-entry> [...]");
        }

        DecompInterface iface = new DecompInterface();
        iface.openProgram(currentProgram);

        for (String entryStr : args) {
            Address entry = toAddr(entryStr);
            Function func = getFunctionAt(entry);
            println("");
            println("=== FUNCTION " + entry + " ===");
            if (func == null) {
                func = getFunctionContaining(entry);
            }
            if (func == null) {
                println("not a function");
                continue;
            }
            println("entry: " + func.getEntryPoint());
            println("name: " + func.getName());
            DecompileResults res = iface.decompileFunction(func, 120, monitor);
            if (!res.decompileCompleted()) {
                println("decompile failed: " + res.getErrorMessage());
                continue;
            }
            println(res.getDecompiledFunction().getC());
        }

        iface.dispose();
    }
}
