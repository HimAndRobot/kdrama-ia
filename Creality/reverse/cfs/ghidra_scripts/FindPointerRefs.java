import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSetView;
import ghidra.program.model.listing.Function;
import ghidra.program.model.mem.Memory;
import ghidra.program.model.mem.MemoryBlock;

public class FindPointerRefs extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Memory mem = currentProgram.getMemory();
        int[] targets = new int[] { 0x0002f7d4, 0x0002f810, 0x0002f868, 0x0002f9b0 };
        for (int target : targets) {
            println(String.format("=== TARGET %08x ===", target));
            for (MemoryBlock block : mem.getBlocks()) {
                if (!block.isInitialized()) continue;
                Address start = block.getStart();
                Address end = block.getEnd();
                long len = end.subtract(start) + 1;
                if (len < 4) continue;
                for (long off = 0; off <= len - 4; off += 4) {
                    Address a = start.add(off);
                    int v;
                    try {
                        v = mem.getInt(a);
                    } catch (Exception ex) {
                        continue;
                    }
                    if (v == target) {
                        println("ref @ " + a + " in " + block.getName());
                        for (int i = -2; i <= 3; i++) {
                            Address p = a.add(i * 4L);
                            try {
                                int w = mem.getInt(p);
                                println(String.format("  %s : %08x", p, w));
                                Function f = getFunctionAt(toAddr(String.format("%08x", w)));
                                if (f != null) println("    -> func " + f.getName());
                            } catch (Exception ex) {
                            }
                        }
                    }
                }
            }
        }
    }
}
