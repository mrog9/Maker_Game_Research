Packages:
    pandas
    networkx
    scipy

Graphs folder contains the data (parsed certificate in csv file, node features from the graph constructed using networkx, and the constructed graph itself in graphml extension). The graph is directed, with an edge from each card to every card its line uses. A parenthesized expression in a line is a card written in place (Section 3.1 of the paper), so the cards inside it count as used by that line.

graph_layered.gexf is the whole proof as a directed graph. Every parenthesized expression is its own node, named like 598.1 (the 1st child of card 598). One more node, Snaky, stands for the finished shape, and each base card 0 to 5 has an edge to it. That makes 1,627 nodes. Each node sits in the row for its height h, the number of Maker moves it needs: 0 for Snaky, otherwise 1 + the largest h of its children (so 1 for the base cards). Snaky is alone at the bottom, card 727 is alone at the top with h = 21, and every edge points down. Run graph_utils/layer_graph.py to make it. In Gephi Lite, open it without running a layout so the rows stay in place.

Use Gephi Lite to look at the graph in browser