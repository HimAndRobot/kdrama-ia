import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.listing.Listing;

public class ListFunctionsByName extends GhidraScript {
    @Override
    protected void run() throws Exception {
        String needle = getScriptArgs().length > 0 ? getScriptArgs()[0].toLowerCase() : "";
        Listing listing = currentProgram.getListing();
        FunctionIterator it = listing.getFunctions(true);
        while (it.hasNext()) {
            Function f = it.next();
            String name = f.getName();
            if (needle.isEmpty() || name.toLowerCase().contains(needle)) {
                println(f.getEntryPoint() + " " + name);
            }
        }
    }
}
