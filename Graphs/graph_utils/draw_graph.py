import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

def draw_graph():

    # keep the card numbers as text in the PDF, so they can be searched
    matplotlib.rcParams["pdf.fonttype"] = 42

    G = "{http://www.gexf.net/1.2draft}"

    V = "{http://www.gexf.net/1.2draft/viz}"

    graph = ET.parse("certificate/graph_layered.gexf").getroot().find(G + "graph")

    titles = {a.get("id"): a.get("title") for a in graph.iter(G + "attribute")}

    # inches between neighbors in a row, and between rows
    slot, row = 0.3, 1.4

    nodes = {}

    for n in graph.iter(G + "node"):

        p = n.find(V + "position")

        c = n.find(V + "color")

        att = {titles[v.get("for")]: v.get("value") for v in n.iter(G + "attvalue")}

        nodes[n.get("id")] = {
            "x": float(p.get("x")) / 20 * slot,
            "y": int(att["h"]) * row,
            "h": int(att["h"]),
            "kind": att["kind"],
            "color": tuple(int(c.get(k)) / 255 for k in "rgb")
        }

    edges = [(e.get("source"), e.get("target")) for e in graph.iter(G + "edge")]

    # node diameter and label size in points
    diam = {"inline": 4.0, "card": 6.0, "base": 9.0, "snaky": 16.0}

    font = {"inline": 3.0, "card": 3.5, "base": 6.0, "snaky": 12.0}

    for k, n in nodes.items():

        n["d"] = 12.0 if k == "727" else diam[n["kind"]]

        n["font"] = 9.0 if k == "727" else font[n["kind"]]

    xs = [n["x"] for n in nodes.values()]

    top_h = max(n["h"] for n in nodes.values())

    left, right, bottom, top = min(xs) - 2.2, max(xs) + 0.6, -0.8, top_h * row + 3.2

    fig = plt.figure(figsize=(right - left, top - bottom))

    ax = fig.add_axes([0, 0, 1, 1])

    ax.set_xlim(left, right)

    ax.set_ylim(bottom, top)

    ax.axis("off")

    for s, t in edges:

        a, b = nodes[s], nodes[t]

        ax.add_patch(FancyArrowPatch(
            (a["x"], a["y"]), (b["x"], b["y"]), arrowstyle="-|>", mutation_scale=3.5,
            lw=0.2, color=(0.3, 0.3, 0.3, 0.45), shrinkA=a["d"] / 2, shrinkB=b["d"] / 2 + 0.3, zorder=1))

    for k, n in nodes.items():

        ax.scatter([n["x"]], [n["y"]], s=n["d"] ** 2, color=[n["color"]], edgecolors="white", linewidths=0.3, zorder=3)

        # many arrows land on the base cards and Snaky from above, so label them underneath
        below = n["kind"] in ("base", "snaky")

        ax.annotate(k, (n["x"], n["y"]), xytext=(0, -(n["d"] / 2 + 0.6) if below else n["d"] / 2 + 0.6),
                    textcoords="offset points", ha="center", va="top" if below else "bottom",
                    fontsize=n["font"], color="0.1", zorder=4)

    for h in range(top_h + 1):

        ax.text(min(xs) - 0.6, h * row, "h = " + str(h), ha="right", va="center", fontsize=20, color="0.25")

    ax.text(left + 0.4, top - 0.5, "Snaky in 21 Maker moves: the whole proof as a directed graph (certificate in Appendix D)",
            ha="left", va="top", fontsize=40)

    ax.text(left + 0.4, top - 1.4,
            f"{len(nodes):,} nodes, {len(edges):,} edges. Each card sits in the row for its height h, the number of Maker moves it needs. "
            "Every edge goes from a card down to one of its children.",
            ha="left", va="top", fontsize=20, color="0.25")

    legend = [("numbered card 6-727", "card"), ("inline card (parenthesized expression, named like 598.1)", "inline"),
              ("base card 0-5", "base"), ("Snaky, finished", "snaky")]

    for i, (label, kind) in enumerate(legend):

        color = next(n["color"] for n in nodes.values() if n["kind"] == kind)

        count = sum(1 for n in nodes.values() if n["kind"] == kind)

        y = top - 0.5 - i * 0.5

        ax.scatter([right - 9.5], [y], s=200, color=[color], zorder=3)

        ax.text(right - 9.2, y, f"{label} ({count:,})", ha="left", va="center", fontsize=18)

    # no creation date, so the same graph always gives the same file
    fig.savefig("certificate/graph_layered.pdf", metadata={"CreationDate": None})

if __name__ == "__main__":

    draw_graph()
