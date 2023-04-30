import re
import pprint
import json
from time import sleep
from scholarly import scholarly
# from search_integration_tools import read_topics_from_file, parse_importance, radial_queries
# from zotero_integration_tools import add_to_zotero

def read_topics_from_file(file_path):
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
    for i in keyword:
        if i == "!":
            return (keyword.replace("!", "").strip(), "important")
    for i in range(len(keyword) - 1):
        if keyword[i] + keyword[i + 1] == "[]":
            return (keyword.replace("[]", "").strip(), "unimportant")
    return (keyword.strip(), "normal")


def or_together(topics: dict, topic: str, filter = True):
    query: str = ""
    for i in topics[topic]:
        i, importance = parse_importance(i)
        if importance == filter or filter == True:
            query += "\"" + i + "\""
            query += "|"
    query = query[:-1]
    return query


def radial_queries(filename: str):
    topics = read_topics_from_file(filename)

    # all queries relating to just mental health and college, with various different words
    # for mental health highlighted.
    queries: list = []
    for keyword in topics["Mental Health"]:
        keyword, importance = parse_importance(keyword)
        if importance == "important" or importance == "normal":
            query =  "\"" + keyword + "\"" + " AND "
            query += or_together(topics, "College", "important")
            queries.append(query)

    base_query = \
    or_together(topics, "Mental Health", "important")\
    + " AND " \
    + or_together(topics, "College", "important")

    for optional in topics["Access"] + topics["Stakeholders"] + topics["Current Institutions Helping"] + topics["Specific Causes"]:
        optional, importance = parse_importance(optional)
        if importance == "normal" or importance == "important":
            optional_query = base_query + " AND " + "\"" + optional + "\""
            queries.append(optional_query)

    return queries
    # query = ""
    # for i in topics["Mental Health"]:
    #     i, importance = parse_importance(i)
    #     if importance == "important":
    #         query += "\"" + i + "\""
    #         query += "|"
    # query = query[:-1] + " AND "
    # for i in topics["College"]:
    #     i, importance = parse_importance(i)
    #     if importance == "important":
    #         query += "\"" + i + "\""
    #         query += "|"
    # query = query[:-1] + ""
    # print(query)

def read_queries_and_numbers(file = "weighted_queries.txt"):
    """Reads queries and their matching amount of pubs you want to find."""
    with open("queries.txt") as f:
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

def process_x_queries(x, startfrom_xth_query, queries, numbers):
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
    for i in range(startfrom_xth_query, startfrom_xth_query+x):
        print("Searching under the query", queries[i])
        response_object = scholarly.search_pubs(queries[i])
        publications = []
        for j in range(numbers[queries[i]]):
            print("\r", j, f"/{numbers[queries[i]]}th query under", queries[i])
            source = next(response_object)
            source["query"] = queries[i]
            publications.append(source)
            print("-")
            sleep(0.23562)

        with open(f"No.{i}_query_results.txt", "w") as f:  #FHook1
            f.write(str(numbers[queries[i]])+"\n")
            for k in publications:
                # f.write(pprint.pformat(publications[i]))
                my_json = json.dumps(k)
                f.write(my_json+"\n")
            pass


# process_x_queries(2, 0)