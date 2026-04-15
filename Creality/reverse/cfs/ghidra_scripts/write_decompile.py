#@category Codex

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

args = getScriptArgs()
if len(args) < 2:
    raise Exception("Usage: write_decompile.py <addr> <outPath>")

addr = toAddr(args[0])
out_path = args[1]
func = getFunctionAt(addr)
if func is None:
    func = getFunctionContaining(addr)
if func is None:
    raise Exception("No function at/containing %s" % args[0])

iface = DecompInterface()
iface.openProgram(currentProgram)
res = iface.decompileFunction(func, 120, ConsoleTaskMonitor())
if not res.decompileCompleted():
    raise Exception("Decompile failed for %s" % func.getName())

with open(out_path, "w") as f:
    f.write("FUNCTION %s @ %s\n\n" % (func.getName(), str(func.getEntryPoint())))
    f.write(res.getDecompiledFunction().getC())
    f.write("\n")

print("wrote %s" % out_path)
