import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.mem.Memory;

public class DumpDataPointers extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Memory mem = currentProgram.getMemory();
        Address start = toAddr("00040590");
        for (int i = 0; i < 48; i++) {
            Address a = start.add(i * 16);
            int w0 = mem.getInt(a);
            int w1 = mem.getInt(a.add(4));
            int w2 = mem.getInt(a.add(8));
            int w3 = mem.getInt(a.add(12));
            println(String.format("%s: %08x %08x %08x %08x", a, w0, w1, w2, w3));
            for (int j = 0; j < 4; j++) {
                int w = new int[] {w0, w1, w2, w3}[j];
                if (w <= 0) {
                    continue;
                }
                Address p = toAddr(String.format("%08x", w));
                Function f = getFunctionAt(p);
                if (f != null) {
                    println("  -> func " + p + " " + f.getName());
                    continue;
                }
                Data d = getDataAt(p);
                if (d != null) {
                    println("  -> data " + p + " " + d.toString());
                }
            }
        }
    }
}
