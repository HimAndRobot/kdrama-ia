import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;

public class FindContainingFunction extends GhidraScript {
    @Override
    protected void run() throws Exception {
        if (getScriptArgs().length == 0) {
            throw new RuntimeException("Usage: FindContainingFunction.java <addr> [...]");
        }
        for (String s : getScriptArgs()) {
            Address a = toAddr(s);
            Function f = getFunctionContaining(a);
            println("=== " + s + " ===");
            if (f == null) {
                println("no function");
            } else {
                println("entry: " + f.getEntryPoint());
                println("name: " + f.getName());
            }
        }
    }
}
