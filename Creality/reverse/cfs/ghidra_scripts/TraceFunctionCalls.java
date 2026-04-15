import java.util.*;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;

public class TraceFunctionCalls extends GhidraScript {

    private static final String[] ENTRIES = {
        "0002bac4", // cmd_send_data_with_response wrapper
        "0003427c"  // raw_send_wait_ack wrapper
    };

    @Override
    protected void run() throws Exception {
        ReferenceManager refman = currentProgram.getReferenceManager();
        Listing listing = currentProgram.getListing();

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

            Set<String> seen = new LinkedHashSet<>();
            InstructionIterator it = listing.getInstructions(func.getBody(), true);
            while (it.hasNext() && !monitor.isCancelled()) {
                Instruction ins = it.next();
                FlowType flow = ins.getFlowType();
                if (!flow.isCall()) {
                    continue;
                }
                Reference[] refs = ins.getOperandReferences(0);
                if (refs == null || refs.length == 0) {
                    println("call @ " + ins.getAddress() + " -> unresolved: " + ins);
                    continue;
                }
                for (Reference ref : refs) {
                    Address to = ref.getToAddress();
                    Function callee = getFunctionAt(to);
                    String line = "call @ " + ins.getAddress() + " -> " + to +
                        (callee != null ? (" (" + callee.getName() + ")") : "");
                    if (seen.add(line)) {
                        println(line);
                    }
                }
            }
        }
    }
}
