import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import java.io.FileWriter;

public class WriteDecompileToFile extends GhidraScript {
    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 2) {
            throw new RuntimeException("Usage: WriteDecompileToFile.java <addr> <outPath>");
        }
        String addrStr = args[0];
        String outPath = args[1];

        Address entry = toAddr(addrStr);
        Function func = getFunctionAt(entry);
        if (func == null) {
            throw new RuntimeException("No function at " + addrStr);
        }

        DecompInterface iface = new DecompInterface();
        iface.openProgram(currentProgram);
        DecompileResults res = iface.decompileFunction(func, 120, monitor);
        if (!res.decompileCompleted()) {
            throw new RuntimeException("Decompile failed for " + func.getName());
        }

        try (FileWriter fw = new FileWriter(outPath)) {
            fw.write("FUNCTION " + func.getName() + " @ " + addrStr + "\n\n");
            fw.write(res.getDecompiledFunction().getC());
            fw.write("\n");
        }
        iface.dispose();
        println("wrote " + outPath);
    }
}
