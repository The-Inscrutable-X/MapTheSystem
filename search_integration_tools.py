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
            query = keyword + " AND "
            query += or_together(topics, "College", "important")
            queries.append(query)

    base_query = \
    or_together(topics, "Mental Health", "important")\
    + " AND " \
    + or_together(topics, "College", "important")

    for optional in topics["Access"] + topics["Stakeholders"] + topics["Current Institutions Helping"] + topics["Specific Causes"]:
        optional, importance = parse_importance(optional)
        if importance == "normal" or importance == "important":
            optional_query = base_query + " AND " + optional
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