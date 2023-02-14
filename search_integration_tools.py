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
