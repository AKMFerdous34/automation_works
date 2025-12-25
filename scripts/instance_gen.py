import re
import sys
from pathlib import Path

def parse_verilog_module(filepath):
    text = Path(filepath).read_text()

    # Collapse multiline parameter/port lists
    text = re.sub(r"\s+", " ", text)

    # ----- Extract module header -----
    module_regex = re.compile(
        r"module\s+(\w+)\s*"
        r"(#\s*\((.*?)\))?\s*"        # parameters (optional)
        r"\((.*?)\)\s*;",             # ports
        re.IGNORECASE
    )

    m = module_regex.search(text)
    if not m:
        raise ValueError("Could not find module definition!")

    module_name = m.group(1)
    raw_params = m.group(3) or ""
    raw_ports = m.group(4)

    # ----- Parse parameters -----
    params = []
    for p in raw_params.split(","):
        p = p.strip()
        if p.startswith("parameter"):
            p = p.replace("parameter", "").strip()
        if p:
            params.append(p)

    # ----- Parse ports -----
    ports = []
    for p in raw_ports.split(","):
        p = p.strip()

        # direction, width, name
        pm = re.match(r"(input logic|output logic|inout logic)?\s*(\[[^\]]+\])?\s*(\w+)", p)
        if pm:
            direction, width, name = pm.groups()
            ports.append((direction, width, name))

    return module_name, params, ports


def generate_instance(name, params, ports):
    out = []

    # ----- Parameter instance -----
    if params:
        out.append(f"{name} #(")
        for i, p in enumerate(params):
            pname = p.split("=")[0].strip()
            comma = "," if i < len(params)-1 else ""
            out.append(f"    .{pname}({pname}){comma}")
        out.append(") u_" + name + " (")
    else:
        out.append(f"{name} u_{name} (")

    # ----- Port instance -----
    for i, (direction, width, portname) in enumerate(ports):
        comma = "," if i < len(ports)-1 else ""
        out.append(f"    .{portname}({portname}){comma}")

    out.append(");")
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gen_instance.py <verilog_file.v>")
        sys.exit(1)

    module_name, params, ports = parse_verilog_module(sys.argv[1])
    print(generate_instance(module_name, params, ports))

