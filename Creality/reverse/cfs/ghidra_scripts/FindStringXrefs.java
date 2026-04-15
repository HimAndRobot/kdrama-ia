import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import ghidra.program.model.symbol.ReferenceManager;
import ghidra.program.model.mem.Memory;
import ghidra.program.model.mem.MemoryBlock;
import java.util.ArrayList;
import java.util.List;

public class FindStringXrefs extends GhidraScript {
    private Address findAscii(String needle) throws Exception {
        Memory mem = currentProgram.getMemory();
        byte[] pat = needle.getBytes("UTF-8");
        for (MemoryBlock block : mem.getBlocks()) {
            if (!block.isInitialized() || !block.isRead()) {
                continue;
            }
            if (!".rodata".equals(block.getName()) && !block.getName().contains("rodata")) {
                continue;
            }
            Address start = block.getStart();
            Address end = block.getEnd();
            Address cur = start;
            while (cur.compareTo(end) <= 0) {
                Address hit = mem.findBytes(cur, end, pat, null, true, monitor);
                if (hit == null) {
                    break;
                }
                return hit;
            }
        }
        return null;
    }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length == 0) {
            throw new RuntimeException("Usage: FindStringXrefs.java <string> [<string>...]");
        }

        ReferenceManager refman = currentProgram.getReferenceManager();
        for (String needle : args) {
            println("=== STRING: " + needle + " ===");
            Address strAddr = findAscii(needle);
            if (strAddr == null) {
                println("not found");
                continue;
            }
            println("addr: " + strAddr);
            List<String> seen = new ArrayList<>();
            ReferenceIterator refs = refman.getReferencesTo(strAddr);
            while (refs.hasNext()) {
                Reference ref = refs.next();
                Address from = ref.getFromAddress();
                Function func = getFunctionContaining(from);
                String line = from + " <- " + ref.getReferenceType() +
                    (func != null ? (" in " + func.getEntryPoint() + " " + func.getName()) : "");
                if (!seen.contains(line)) {
                    seen.add(line);
                    println(line);
                }
            }
        }
    }
}
