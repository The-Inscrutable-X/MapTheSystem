"""
Goal: automatically return results from keywords and scrape their PMIDs or other IDs. 
Python Ebscohost discovery API may be used (account needed); Google scholar may be used (more work needed with scholarly and ScraperAPI)
Use IDs to automatically populate zotero database. 

Google Scholar Problems. Google scholar is not very accepting of long queries. Boolean Expressions cannot incorporate parantheses. 
| is used istead of OR to serve as a sort of pseduo parathesis based on order of operations, it seems to have a limited but observable effect.

Correction: Boolean Search appears to work, but longer queries are cut off and the operation precedence is abnormal. AND and OR seem not to have 
usual precedence, although && is still higher in precedence than OR, and presumably | is higher in precedence than AND (it so far seems this way).

Limit search to 2003-2023.

Note for the Zotero API:
You can quickly add items to your library if you already know their ISBN, DOI, PubMed ID, or arXiv ID. 

For searching the zotero data base, a potential solution is found for the constriction
only problem that was pointed out by Riley:
tag search. See the Search Syntax for details. More than one tag may be passed by passing a list of strings – These are treated as AND search terms, meaning only items which include all of the specified tags are returned. You can search for items matching any tag in a list by using OR: "tag1 OR tag2", and all items which exclude a tag: "-tag".
"""
import pprint
import json
from time import sleep
from scholarly import scholarly
from search_integration_tools import radial_queries, process_x_queries, read_queries_and_numbers, parse_keywords
from zotero_integration_tools import add_to_zotero, mass_read, mass_add_to_zotero
from pathlib import Path
from pyzotero import zotero
# This code block is responsible for generating queries based on a list of keywords in a file called
# "keywords_new.txt". The radial_queries function takes in the file name and generates a list of
# queries based on the keywords. These queries are then written to a file called "out".

jobpath = Path("jobs/job3")

if False:
    parsed_tree = parse_keywords(jobpath / "keywords.txt")
    parsed_tree.create_queries()
    # print(*parsed_tree.queries, sep="\n")
    parsed_tree.save_queries(jobpath / "queries")

if False:
    queries, numbers = read_queries_and_numbers(jobpath)

    process_x_queries(35, 0, queries, numbers, jobpath)

if True:
    publications = mass_read(jobpath, 0, 1)

    zot = zotero.Zotero("5169855", "group", "1sBBLDs3c6BMvSPzSL8MqHmt")

    mass_add_to_zotero(zot, publications, collection_key="MWV58QF6")