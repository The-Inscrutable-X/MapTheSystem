import re
import pprint
import json
from time import sleep
from scholarly import scholarly
from query_tree_utilities import QueryNode, QueryTree
import os
# from search_integration_tools import read_topics_from_file, parse_importance, radial_queries
# from zotero_integration_tools import add_to_zotero

def read_topics_from_file(file_path):
    """
    This function reads topics and their associated content from a file and returns them as a
    dictionary.
    
    :param file_path: The file path is a string that specifies the location of the file that contains
    the topics and their associated subtopics
    :return: The function `read_topics_from_file` returns a dictionary where the keys are the topics and
    the values are lists of strings representing the subtopics under each topic.
    """
    topics = {}
    with open(file_path, "r") as file:
        current_topic = None
        for line in file:
            # print(line)
            if line == "\n":
                continue
            line = line.strip()
            if line.startswith("----"):
                topic = line[4:]
                current_topic = topic
                topics[current_topic] = []
            else:
                topics[current_topic].append(line)
    return topics


def parse_importance(keyword: str):
    """
    The above code contains two functions, `radial_queries` and `read_queries_and_numbers`, which are
    used to generate and read queries for a research project.
    
    :param keyword: A string representing a keyword or topic
    :type keyword: str
    :return: The functions `radial_queries` and `read_queries_and_numbers` are returning a list of
    strings (queries) and a tuple of a list of strings (queries) and a dictionary (numbers)
    respectively.
    """
    for i in keyword:
        if i == "!":
            return (keyword.replace("!", "").strip(), "important")
    for i in range(len(keyword) - 1):
        if keyword[i] + keyword[i + 1] == "[]":
            return (keyword.replace("[]", "").strip(), "unimportant")
    return (keyword.strip(), "normal")


def or_together(topics: dict, topic: str, filter = True):
    """
    This is a function definition in Python that takes in a dictionary of topics, a specific topic, and
    an optional filter parameter.
    
    :param topics: A dictionary containing topic names as keys and lists of strings as values. Each list
    contains the words associated with the corresponding topic
    :type topics: dict
    :param topic: a string representing the topic to be searched in the dictionary
    :type topic: str
    :param filter: The "filter" parameter is a boolean value that determines whether or not the function
    should filter out the topic being passed in from the dictionary of topics before performing the OR
    operation. If set to True (default), the function will exclude the topic being passed in from the OR
    operation. If set to False, defaults to True (optional)
    """
    query: str = ""
    for i in topics[topic]:
        i, importance = parse_importance(i)
        if importance == filter or filter == True:
            query += "\"" + i + "\""
            query += "|"
    query = query[:-1]
    return query

def parse_keywords(filename: str):
    tree = QueryTree()
    tree.parse_keywords(filename)
    return tree
    # for line in text.strip().split("\n"):
    #     if line.startswith(":CONSTRAINT"):
    #         current_constraint = re.search(r'-name <(.*?)>', line).group(1)
    #         parsed_data[current_constraint] = []
    #     elif line.startswith(":ROTATING_CONSTRAINT"):
    #         current_rotating_constraint = re.search(r'-name <(.*?)>', line).group(1)
    #         parsed_data[current_rotating_constraint] = {'SUBTOPICS': {}}
    #     elif line.startswith(":SUBTOPICS"):
    #         strength = re.search(r'-strength (\d+)', line).group(1)
    #         parsed_data[current_rotating_constraint]['strength'] = strength
    #     else:
    #         if current_rotating_constraint:
    #             parsed_data[current_rotating_constraint].append(line.strip())
    #         else:
    #             parsed_data[current_constraint].append(line.strip())
                
    # return parsed_data

def radial_queries(filename: str):
    """
    The function generates a list of queries related to mental health and college, as well as other
    optional topics, based on keywords parsed from a given file.
    
    :param filename: The name of the file containing the topics and their importance levels
    :type filename: str
    :return: The function `radial_queries` returns a list of queries related to mental health and
    college, as well as other optional topics, parsed from a file.
    """
    topics = read_topics_from_file(filename)

    # all queries relating to just mental health and college, with various different words
    # for mental health highlighted.
    queries: list = []
    for keyword in topics["CONSTRAINT A"]:
        keyword, importance = parse_importance(keyword)
        if importance == "important" or importance == "normal":
            query =  "\"" + keyword + "\"" + " AND "
            query += or_together(topics, "CONSTRAINT B", "important")
            queries.append(query)

    
    # all queries in general
    base_query = \
    or_together(topics, "CONSTRAINT A", "important")\
    + " AND " \
    + or_together(topics, "CONSTRAINT B", "important")

    # Edit subqueries inclusion
    for optional in topics["Access"] + topics["Stakeholders"] + topics["Current Institutions Helping"] + topics["Specific Causes"]:
        optional, importance = parse_importance(optional)
        if importance == "normal" or importance == "important":
            optional_query = base_query + " AND " + "\"" + optional + "\""
            queries.append(optional_query)

    return queries

def read_queries_and_numbers(job_directory, file = "weighted_queries.txt"):
    """Reads queries and their matching amount of pubs you want to find."""
    file = job_directory / file
    with open(file) as f:
        lines = f.readlines()
        numbers = dict()
        queries = list()
        for i in lines:
            match = re.match(r"(\d+)(.+)", i)
            number = match.group(1)
            query = match.group(2).strip()
            numbers[query] = int(number)
            queries.append(query)
    return queries, numbers

def process_x_queries(x, startfrom_xth_query, queries, numbers, job_directory: str):
    """Processes x full queries. e.g. x = 2 might scan for 200 publications 
    if you indicated you wanted 100 publications from each query. 
    Searches are according to the number of publications you specified to search for 
    under each query."""

    """This section handles getting and storing found publications from google scholar. 
    It also sets up the scraper API integration to make sure we won't get blocked."""

    from scholarly import scholarly, ProxyGenerator

    pg = ProxyGenerator()
    success = pg.ScraperAPI("bb352d5ec00ecbb6e8722f36df3a1e0f", premium=False)  # old key from hanqixiao.personal "86de3e274ab2ae881c6a803df2e90720" Was unable to access trial call.s
    print(success)
    scholarly.use_proxy(pg)
    if x > 0:
        if not os.path.exists(job_directory / "results"):
            os.mkdir(job_directory / "results")
    for i in range(startfrom_xth_query, startfrom_xth_query+x):
        print("Searching under the query", queries[i])
        response_object = scholarly.search_pubs(queries[i])
        publications = []
        for j in range(numbers[queries[i]]):
            print("\r", j+1, f"/{numbers[queries[i]]}th query")
            source = next(response_object)
            source["query"] = queries[i]
            publications.append(source)
            print("-")
            sleep(0.23562)
        save_path = job_directory / "results" / f"No.{i}_query_results.txt"
        with open(save_path, "w") as f:  #FHook1
            f.write(queries[i]+"\n")
            f.write(str(numbers[queries[i]])+"\n")
            for k in publications:
                # f.write(pprint.pformat(publications[i]))
                my_json = json.dumps(k)
                f.write(my_json+"\n")
            pass


# process_x_queries(2, 0)