import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.mem.Memory;
import ghidra.program.model.mem.MemoryBlock;

public class FindSlotTableEntries extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Memory mem = currentProgram.getMemory();
        int[] slots = new int[] {
            0x00052a70, 0x00052a74, 0x00052a78, 0x00052a7c, 0x00052a80, 0x00052a84,
            0x00052a88, 0x00052a8c, 0x00052a90, 0x00052a94, 0x00052a98, 0x00052a9c,
            0x00052aa0, 0x00052aa4, 0x00052aa8, 0x00052aac, 0x00052ab0
        };
        for (int slot : slots) {
            println(String.format("=== SLOT %08x ===", slot));
            for (MemoryBlock block : mem.getBlocks()) {
                if (!block.isInitialized()) continue;
                if (!".data".equals(block.getName())) continue;
                Address start = block.getStart();
                Address end = block.getEnd();
                long len = end.subtract(start) + 1;
                for (long off = 0; off <= len - 8; off += 4) {
                    Address a = start.add(off);
                    int w1, w2;
                    try {
                        w1 = mem.getInt(a);
                        w2 = mem.getInt(a.add(4));
                    } catch (Exception ex) {
                        continue;
                    }
                    if (w1 == slot || w2 == slot) {
                        println("entry around " + a);
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
