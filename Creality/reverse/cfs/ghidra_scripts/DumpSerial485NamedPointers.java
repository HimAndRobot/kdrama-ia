import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.Function;
import ghidra.program.model.mem.Memory;

public class DumpSerial485NamedPointers extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Memory mem = currentProgram.getMemory();
        Address basePtrAddr = toAddr("0005229c");
        int base = mem.getInt(basePtrAddr);
        println(String.format("PTR_DAT_0005229c -> %08x", base));

        int[] offsets = new int[] {
            0x2a7c, 0x2a94, 0x2b48, 0x2b68, 0x2b90, 0x2c0c, 0x2d70, 0x2dd8, 0x2f70, 0x2fa0
        };

        for (int off : offsets) {
            Address slot = toAddr(String.format("%08x", base + off));
            int ptr = mem.getInt(slot);
            println(String.format("[%04x] slot=%s -> %08x", off, slot, ptr));
            if (ptr <= 0) {
                continue;
            }
            Address p = toAddr(String.format("%08x", ptr));
            Function f = getFunctionAt(p);
            if (f != null) {
                println("  func: " + f.getName() + " @ " + p);
                continue;
            }
            Data d = getDataAt(p);
            if (d != null) {
                println("  data: " + d);
            }
            println("  sym: " + getSymbolAt(p));
        }
    }
}
