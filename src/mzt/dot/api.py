import re
from typing import List, Optional, TextIO


def node(x: str) -> str:
    return x.replace("%", "node")


def label(l: str) -> str:
    r = "\n" + l.strip(" \n") + "\n"
    r = r.replace('"', '\\"')
    r = r.replace("\n| |", "\n| -")
    r = r.replace("| ", "")
    r = r.replace(">", "\\>")
    r = r.replace("<", "\\<")
    r = r.replace("{", "\\{")
    r = r.replace("}", "\\}")
    r = r.strip(" \n")
    r = r.replace("\n", "\\l") + "\\l"
    return r


def generate_graph(out: TextIO, lines: List[str], title: Optional[str] = None) -> None:
    nodes = []
    edges = set()
    current_node = None

    # print("-" * 80)
    # print("\n".join(lines))
    # print("-" * 80)

    for line in lines:
        if line.startswith("%"):
            current_node = dict()
            current_node["name"] = line[: line.find(" ")]
            current_node["text"] = ""
        elif len(line) == 0:
            if current_node is not None:
                nodes.append(current_node)
            current_node = None
        elif current_node is not None:
            current_node["text"] += "\n" + line

    if current_node is not None:
        nodes.append(current_node)

    for n in nodes:
        for d in re.findall(r"%\d+", n["text"]):
            edges.add((d, n["name"]))

    if title:
        out.write('digraph G {\n    label="%s"\n' % (label(title)))
    else:
        out.write("digraph G {\n")

    for n in nodes:
        out.write(
            '    %s [shape = record, label="%s"]\n'
            % (node(n["name"]), label(n["text"]))
        )

    for e in edges:
        out.write(
            '    %s -> %s [label = "%s"]\n' % (node(e[0]), node(e[1]), label(e[0]))
        )

    out.write("}\n")
