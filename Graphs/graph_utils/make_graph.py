import networkx as nx
import pandas as pd

def create_graph():

    df = pd.read_csv("certificate/certificate.csv")
    df = df['construction']

    G = nx.Graph()

    G.add_nodes_from([i for i in range(727)])

    for ind, construct in df.items():
        
        construct = construct.strip()
        child_list = construct.split(" ")[2:]

        for c in child_list:

            other_node = None

            if not (c.find(":") == -1):

                other_node = int(c.split(":")[0])

            else:

                other_node = int(c)

            

            G.add_edge(ind+6, other_node)

    data =[]

    for n,d in G.degree():

        data.append([n,d])

    df_deg = pd.DataFrame(data = data, columns=['card', 'degree'])

    data = []

    bc_dict = nx.betweenness_centrality(G)
    pr_dict = nx.pagerank(G)

    for card in df_deg['card']:

        data.append([bc_dict[card], pr_dict[card]])

    df_other = pd.DataFrame(data = data, columns=["betweeness_centrality", "pagerank"])

    df_main = pd.concat([df_deg,df_other], axis=1)

    df_main.to_csv('certificate/node_features.csv')

    nx.write_graphml(G, "certificate/graph.graphml")

    print(df_main.nlargest(n=10, columns=['degree']))
    print(df_main.nlargest(n=10, columns=['betweeness_centrality']))
    print(df_main.nlargest(n=10, columns=['pagerank']))

if __name__ == "__main__":

    create_graph()


            