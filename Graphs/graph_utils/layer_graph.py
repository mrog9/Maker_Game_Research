import networkx as nx
import pandas as pd

def layer_graph():

    df = pd.read_csv("certificate/certificate.csv")
    df = df['construction'] + df['reference']

    G = nx.DiGraph()

    # every parenthesized expression gets its own node, named like 598.1 (the 1st child of card 598)
    for ind, construct in df.items():

        tokens = construct.split()

        stack = [tokens[0]]

        count = {tokens[0]: 0}

        for c in tokens[2:]:

            parent = stack[-1]

            count[parent] += 1

            if c.startswith("("):

                child = parent + "." + str(count[parent])

                G.add_edge(parent, child)

                stack.append(child)

                count[child] = 0

                continue

            G.add_edge(parent, c.strip(")").split(":")[0])

            for _ in range(c.count(")")):

                stack.pop()

    # the base cards 0 to 5 are Snaky with one cell missing, so Maker's last move from any of them completes Snaky
    for b in range(6):

        G.add_edge(str(b), "Snaky")

    # h = number of Maker moves a card needs: 0 for Snaky, 1 for the bases 0 to 5, else 1 + the largest h of its children
    h = {}

    for n in reversed(list(nx.topological_sort(G))):

        h[n] = 1 + max([h[c] for c in G.successors(n)], default=-1)

    rows = {}

    for n in sorted(G.nodes(), key=lambda n: [-1] if n == "Snaky" else [int(p) for p in n.split(".")]):

        rows.setdefault(h[n], []).append(n)

    # start each row in card order, then reorder it by the average x of each card's neighbors to cut down crossings
    x = {}

    for row in rows.values():

        for i, n in enumerate(row):

            x[n] = i - (len(row) - 1) / 2

    for _ in range(20):

        for row in rows.values():

            row.sort(key=lambda n: sum(x[m] for m in nx.all_neighbors(G, n)) / G.degree(n))

            for i, n in enumerate(row):

                x[n] = i - (len(row) - 1) / 2

    colors = {'snaky': (210, 50, 50), 'base': (60, 170, 90), 'card': (60, 110, 220), 'inline': (235, 140, 40)}

    for n in G.nodes():

        kind = 'snaky' if n == "Snaky" else 'inline' if "." in n else 'base' if int(n) < 6 else 'card'

        r, g, b = colors[kind]

        G.nodes[n]['h'] = h[n]

        G.nodes[n]['kind'] = kind

        G.nodes[n]['viz'] = {
            'position': {'x': 20.0 * x[n], 'y': 150.0 * h[n], 'z': 0.0},
            'size': 3.0 if kind == 'inline' else 8.0 if kind == 'snaky' else 5.0,
            'color': {'r': r, 'g': g, 'b': b, 'a': 1.0}
        }

    nx.write_gexf(G, "certificate/graph_layered.gexf")

    print(G.number_of_nodes(), "nodes,", G.number_of_edges(), "edges")

    print(sorted((k, len(r)) for k, r in rows.items()))

if __name__ == "__main__":

    layer_graph()
