import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.mem.Memory;
import ghidra.program.model.mem.MemoryBlock;

public class FindBssSlotRefs extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Memory mem = currentProgram.getMemory();
        int[] targets = new int[] {
            0x00052a70, 0x00052a74, 0x00052a78, 0x00052a7c, 0x00052a80, 0x00052a84,
            0x00052a88, 0x00052a8c, 0x00052a90, 0x00052a94, 0x00052a98, 0x00052a9c,
            0x00052aa0, 0x00052aa4, 0x00052aa8, 0x00052aac, 0x00052ab0,
            0x00052ad0, 0x00052adc, 0x00052b48, 0x00052b68, 0x00052b90,
            0x00052c0c, 0x00052c2c, 0x00052c94, 0x00052cb0, 0x00052d70, 0x00052d88, 0x00052dd8
        };
        for (int target : targets) {
            println(String.format("=== SLOT %08x ===", target));
            for (MemoryBlock block : mem.getBlocks()) {
                if (!block.isInitialized()) continue;
                Address start = block.getStart();
                Address end = block.getEnd();
                long len = end.subtract(start) + 1;
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
                        for (int i = -2; i <= 4; i++) {
                            Address p = a.add(i * 4L);
                            try {
                                int w = mem.getInt(p);
                                println(String.format("  %s : %08x", p, w));
                            } catch (Exception ex) {
                            }
                        }
                    }
                }
            }
        }
    }
}
