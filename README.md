Packages:
    pandas
    networkx
    scipy

Graphs folder contains the data (parsed certificate in csv file, node features from the graph constructed using networkx, and the constructed graph itself in graphml extension). The graph is directed, with an edge from each card to every card its line uses. A parenthesized expression in a line is a card written in place (Section 3.1 of the paper), so the cards inside it count as used by that line.

Use Gephi Lite to look at the graph in browser