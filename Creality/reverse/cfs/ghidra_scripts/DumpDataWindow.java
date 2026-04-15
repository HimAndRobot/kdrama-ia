import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.mem.Memory;

public class DumpDataWindow extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Memory mem = currentProgram.getMemory();
        String[] centers = { "00050f00", "00051780", "00051a00" };
        for (String c : centers) {
            Address center = toAddr(c);
            println("=== WINDOW " + center + " ===");
            for (int i = -0x20; i <= 0x40; i += 4) {
                Address a = center.add(i);
                try {
                    int w = mem.getInt(a);
                    println(String.format("%s : %08x", a, w));
                    Function f = getFunctionAt(toAddr(String.format("%08x", w)));
                    if (f != null) {
                        println("  -> func " + f.getName());
                    }
                } catch (Exception ex) {
                    println(a + " : <err>");
                }
            }
        }
    }
}
