from __future__ import annotations
import re

class QueryNode():
    keywords: list[str]
    name: str
    childs: list[QueryNode]
    parent: QueryNode
    node_type: str
    strength: int

    def __init__(self, name, node_type="CONSTRAINT"):
        self.name = name
        self.keywords = []
        self.childs = []
        self.node_type = node_type
        self.strength = 0
        # Self.parent?
    
    def add_child(self, i: QueryNode):
        if not QueryNode:
            return False
        self.childs.append(i)
        i.parent = self
        return True
    
    def add_keyword(self, word):
        self.keywords.append(word)

    def set_strength(self, new_strength):
        self.strength = new_strength



class QueryTree():
    root: QueryNode
    queries: list[str]

    def __init__(self):
        self.root = QueryNode(name="qt_root")
        self.queries = []

    def get_root(self) -> QueryNode:
        return self.root
    
    def parse_keywords(self, filename: str, auto_strength=False):
        """
        Parses the keywords from the specified file and builds the QueryTree, which is a n-ary tree structure that can be iterated to generate 
        #leaf number of queries.

        Args:
            filename (str): The name of the file to parse.
            auto_strength (bool, optional): Flag indicating whether to automatically determine the strength of SUBTOPICS. Defaults to False.
    
        Returns:
            None
        """
    
        with open(filename, "r") as f:
            text = f.readlines()
    
        last_nodes = {-1: self.get_root()}
        current_node = last_nodes[-1]
    
        for line in text:
            level = self.find_indentation(line)
            data = line.strip()
    
            if data == "":
                continue
    
            current_node = last_nodes[level-1]
            print(level, data)
    
            if data.startswith(":SUBTOPICS"):
                new_node = QueryNode(data.replace(":SUBTOPICS", "").strip(), node_type="SUBTOPICS")
    
                if auto_strength:
                    # Find strength of SUBTOPICS
                    match = re.match(r"-strength \d", data)
                    print(match)
    
                    if match:
                        print(match)
                        new_node.set_strength(match.group(1))
    
                current_node.add_child(new_node)
                last_nodes[level] = new_node
    
            elif data.startswith(":CONSTRAINT"):
                new_node = QueryNode(data.replace(":CONSTRAINT".strip(), ""))
                current_node.add_child(new_node)
                last_nodes[level] = new_node
    
            elif not data.startswith("--"):
                last_nodes[level].add_keyword(data)
    
        self.printTree(self.get_root())

    def printTree(self, cur: QueryNode):
        print(cur.name, cur.node_type)
        for i in cur.childs:
            self.printTree(i)

    def or_together(self, keywords):
        query: str = ""
        for i in keywords:
            query += "\"" + i + "\""
            query += "|"
        query = query[:-1]
        return query
    
    def create_queries(self, cur: QueryNode = None, parent_query: str = "", auto_strength = False):
        self.queries = []
        self._create_queries(self.root, parent_query=parent_query)
        if cur:
            self._create_queries(cur, parent_query=parent_query)

    def _create_queries(self, cur: QueryNode, parent_query: str = "", auto_strength = False):
        """
        Recursively creates queries based on the given QueryNode and its children.
    
        Args:
            cur (QueryNode): The current QueryNode being processed.
            parent_query (str, optional): The parent query to be appended to the current query. Defaults to "".
            auto_strength (bool, optional): Flag indicating whether to include the strength of the current QueryNode in the query. Defaults to False.
    
        Returns:
            None
        """
        if cur.node_type == "SUBTOPICS":
            for i in cur.keywords:
                if auto_strength:
                    self.queries.append((str(cur.strength) + parent_query[5:] + ' AND ' + '"' + i + '"'))
                else:
                    self.queries.append((parent_query[5:] + ' AND ' + '"' + i + '"'))
            return
    
        for i in cur.childs:
            if i.node_type == "SUBTOPICS":
                self._create_queries(i, parent_query)
            else:
                self._create_queries(i, parent_query+" AND "+self.or_together(i.keywords))
    
    def save_queries(self, filename):
        """
        Saves the generated queries to a file.
    
        Args:
            filename (str): The name of the file to save the queries to.
    
        Returns:
            None
        """
        with open(filename, "w") as f:
            f.write("\n".join(self.queries))

    @staticmethod
    def find_indentation(string, indent_length=4):
        numSpaces = 0
        for i in string:
            if i == " ":
                numSpaces += 1
            else:
                break
        return numSpaces//indent_length