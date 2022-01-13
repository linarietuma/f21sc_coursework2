import graphviz

class graph:
    def __init__(self, dic, top_docs, doc_uuid, user_uuid=None):
        self.dic = dic # dictionary of readers as keys and documents read by each reader as elements
        self.doc_uuid = doc_uuid # input document uuid
        self.top_docs = top_docs # top 'also likes' documents 
        self.user_uuid = user_uuid
    
    def also_likes(self):
        """ Creates an 'also likes' graph in a pdf format. """
        # create a digraph (directed graph) object 
        dot = graphviz.Digraph(filename='also_likes.gv')
        dot.format = 'pdf' # specify output format

        # create a subgraph of reader uuids
        with dot.subgraph() as r:
            r.attr(rank='same') # ensures all nodes are displayed on the same level
            r.node('User UUID', shape='plaintext') # label node
            # create a node for the input reader if provided
            if self.user_uuid is not None and len(self.user_uuid) >0:
                r.node(self.user_uuid[-4:], style='filled', fillcolor='forestgreen', shape='box')
                # create a link between the input reader and the input document
                dot.edge(self.user_uuid[-4:], self.doc_uuid[-4:]) 
            # for each reader in the dictionary (each key is a reader)
            for reader in self.dic.keys():
                r.node(reader, shape='box')
                # create a link between the reader and the input document
                dot.edge(reader, self.doc_uuid[-4:])
                # create a link between a document read by the reader
                # if the document is among the top 10 most read 'also likes' documents 
                for doc in self.dic[reader]:
                    if doc in [el[1] for el in self.top_docs]:
                        dot.edge(reader, doc[-4:])

        # create a subgraph of document uuids
        with dot.subgraph() as d:
            d.attr(rank='same') # ensures all nodes are displayed on the same level
            # create a node for the input document uuid
            d.node(self.doc_uuid[-4:], style='filled', fillcolor='forestgreen', shape='circle')
            # create a node for each document in the top 'also likes' documents
            for doc in self.top_docs:
                doc_uuid = doc[1]
                d.node(doc_uuid[-4:], shape='circle')
            d.node('Document UUID', shape='plaintext') # label node
            dot.edge('User UUID', 'Document UUID') # create a link between the label nodes
    
        dot.view() # return a graph
