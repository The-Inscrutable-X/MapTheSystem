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


def add_to_zotero(scholarly_json, query, collection_key = "AFMZXANB"):
    """Grab a scholarly response and add it to a particular collection with a tag that 
    cooresponds to the google scholar query that produced it."""
    template = zot.item_template('JournalArticle')
    template["title"] = scholarly_json["bib"]["title"]
    template["url"] = scholarly_json["pub_url"]
    template["publicationTitle"] = scholarly_json["bib"]["venue"]
    resp = zot.create_items([template])
    item_key = resp["successful"]["0"]["key"]
    print(item_key)
    zot.add_tags(zot.item(item_key), query)
    success = zot.addto_collection(collection_key, zot.item(item_key))
    print(success)

# add_to_zotero(pub, "TEST|query")