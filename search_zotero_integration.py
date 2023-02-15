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
from time import sleep
from scholarly import scholarly
from search_integration_tools import read_topics_from_file, parse_importance, radial_queries

queries = radial_queries("keywords_new.txt")

with open("out", "w") as f:
    for i in queries:
        f.write(i + "\n")

print(len(queries))

"""This section handles getting and storing found publications from google scholar."""
publications = []
for i in range(1):
    response_object = scholarly.search_pubs(queries[i])
    publications.append(next(response_object))
    sleep(1.23562)

with open("publications.txt", "w") as f:
    f.write(pprint.pformat(publications[0]))
    pass
# scholarly.pprint(next(responses))
# scholarly.pprint(next(responses))
# responses = scholarly.search_pubs(query)
# scholarly.pprint(next(responses))