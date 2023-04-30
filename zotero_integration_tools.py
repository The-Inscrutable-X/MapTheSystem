from pyzotero import zotero
import pprint
import json

"""
The key of the automation directory is AFMZXANB
"""

zot = zotero.Zotero("4939465", "group", "MLD9GooAjlNi3H5XdkW7dijP")

# with open("publications_storage.txt") as f:  # Creates a sample scholarly output.
#     pub = json.loads(f.read())  # stores it to pub

# print(pub)

# template["title"] = pub["bib"]["title"]
# template["url"] = pub["pub_url"]

# pprint.pprint(template)
# print(zot.collections())
# resp = zot.create_items([template])
# print("ADDED@!")
# item_key = resp["successful"]["0"]["key"]
# print(item_key)
# success = zot.addto_collection("AFMZXANB", zot.item(item_key))
# print("original", resp)
# print("\n\n\n\n")
# print(success)
# print("moved", zot.collection_items("AFMZXANB"))


def query_to_tag(query: str) -> str:
    """Queries are too long to be useful as tag in zotero, shorten them down to their specific topics."""
    query = query.split(" AND ")
    tag: str = str()
    if len(query) <= 2:
        tag = "Maj:" + query[0]
    else:
        tag = query[-1]
    return tag

def add_to_zotero(scholarly_json, query, collection_key = "AFMZXANB"):
    """Obsolete: Grab a scholarly response and add it to a particular collection with a tag that 
    cooresponds to the google scholar query that produced it."""
    if isinstance(query, list):
        amount = 0
        for i in query:
            pass

    print(scholarly_json["bib"]["pub_year"])
    if int(scholarly_json["bib"]["pub_year"]) < 2003:  # Catch a published too early to be relevent error.
        print(scholarly_json["bib"]["title"], "was published before 2003 on", scholarly_json["bib"]["pub_year"])
        return
    template = zot.item_template('JournalArticle')
    template["title"] = scholarly_json["bib"]["title"]
    template["url"] = scholarly_json["pub_url"]
    template["publicationTitle"] = scholarly_json["bib"]["venue"]
    # template["date"] = scholarly_json["bib"]["pub_year"]
    resp = zot.create_items([template])
    item_key = resp["successful"]["0"]["key"]
    print(item_key)
    zot.add_tags(zot.item(item_key), query)
    success = zot.addto_collection(collection_key, zot.item(item_key))
    print(success)

def mass_read(queries, start, stop):
    """Reads all json publications for every query up to the query index specified in 'stop'."""
    publications = dict()
    for i in range(start, stop):
        publications[queries[i]] = list()
        with open(f"No.{i}_query_results.txt", "r") as f:  #FHook1
            print(f"opening No.{i}_query_results.txt")
            publications[queries[i]] = [json.loads(i.strip()) for i in f.readlines()[1:]]
    return publications

def mass_add_to_zotero(publications, collection_key = "AFMZXANB"):
    """Grab a scholarly response and add it to a particular collection with a tag that 
    cooresponds to the google scholar query that produced it."""
    
    for query in publications:
        templates = list()
        count = 0
        shortened_query = query_to_tag(query)
        for scholarly_json in publications[query]:
            if scholarly_json["bib"]["pub_year"] == "NA":
                scholarly_json["bib"]["pub_year"] = "3000"
            if int(scholarly_json["bib"]["pub_year"]) < 2000:  # Catch a published too early to be relevent error.
                print(scholarly_json["bib"]["title"], "was published before 2003 on", scholarly_json["bib"]["pub_year"])
                continue
            try:
                template = zot.item_template('JournalArticle')
                template["title"] = scholarly_json["bib"]["title"]
                template["url"] = scholarly_json["pub_url"]
                template["publicationTitle"] = scholarly_json["bib"]["venue"]
                template["date"] = scholarly_json["bib"]["pub_year"]
            # template["creators"][0]["creatorType"] = "author"
            # template["creators"][0]["firstName"] = "MTSLitScraper"
                templates.append(template)
                count += 1
            except Exception as e:
                print("ERROR ON", query, "Error is", repr(e))
                continue
            if count >= 47:
                resp = zot.create_items(templates)  #FHook2
                for i in range(count):
                    item_key = resp["successful"][str(i)]["key"]
                    print(f"{i}th Added Item to {shortened_query}", item_key)
                    zot.add_tags(zot.item(item_key), shortened_query)
                    success = zot.addto_collection(collection_key, zot.item(item_key))
                    print(success)
                templates = list()
                count = 0
        resp = zot.create_items(templates)  #FHook2
        for i in range(count):
            item_key = resp["successful"][str(i)]["key"]
            print(i)
            print(f"{i}th Added Item to {shortened_query}", item_key)
            zot.add_tags(zot.item(item_key), shortened_query)
            success = zot.addto_collection(collection_key, zot.item(item_key))
            print(success)
        templates = list()
        count = 0

# add_to_zotero(pub, "TEST|query")