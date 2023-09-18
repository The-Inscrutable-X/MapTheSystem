import gradio as gr
import pprint
import json
from time import sleep
from scholarly import scholarly
from search_integration_tools import radial_queries, process_x_queries, read_queries_and_numbers, parse_keywords
from zotero_integration_tools import add_to_zotero, mass_read, mass_add_to_zotero
from pathlib import Path
from pyzotero import zotero

def search_zotero_integration(jobpath, process_queries=False, read_publications=False, add_to_zotero=False):
    # This code block is responsible for generating queries based on a list of keywords in a file called
    # "keywords_new.txt". The radial_queries function takes in the file name and generates a list of
    # queries based on the keywords. These queries are then written to a file called "queries.txt".

    if process_queries:
        parsed_tree = parse_keywords(jobpath / "keywords.txt")
        parsed_tree.create_queries()
        # print(*parsed_tree.queries, sep="\n")
        parsed_tree.save_queries(jobpath / "queries.txt")

    if read_publications:
        queries, numbers = read_queries_and_numbers(jobpath)
        process_x_queries(100, 0, queries, numbers, jobpath)

    if add_to_zotero:
        publications = mass_read(jobpath, 12, 13)
        zot = zotero.Zotero("5169855", "group", "1sBBLDs3c6BMvSPzSL8MqHmt")
        mass_add_to_zotero(zot, publications, collection_key="MWV58QF6")

def search_zotero_integration_app(jobpath):
    process_queries = gr.inputs.Checkbox(label="Process Queries")
    read_publications = gr.inputs.Checkbox(label="Read Publications")
    add_to_zotero = gr.inputs.Checkbox(label="Add to Zotero")

    def run_pipeline(process_queries, read_publications, add_to_zotero):
        search_zotero_integration(jobpath, process_queries, read_publications, add_to_zotero)

    iface = gr.Interface(
        fn=run_pipeline,
        inputs=[process_queries, read_publications, add_to_zotero],
        outputs=None,
        title="Search and Zotero Integration",
        description="Perform search and Zotero integration based on the provided job path.",
        theme="default"
    )
    return iface

if __name__ == '__main__':
    jobpath = Path("jobs/job3")
    iface = search_zotero_integration_app(jobpath)
    iface.launch()
