# Summary

Goal: Enable massive and comprehensive literary search by searching multiple sources (peer reviewed papars, editorials, social media, papers in other languages, etc) for a list of topics and compiling the results in a zotero database. 

The Whole Student Team implemented a novel literature review process designed to eliminate bias and achieve comprehensiveness by drawing from a pre-screening collection of 1071 academic papers, articles, and multimedia sources, which are available here under the queries_folder directory. The literature review process for a topic intimately connected with its researchers faces threats from experiential bias and domain knowledge bias. Also, literature review with any large research team faces the problem of topic clustering, which severely limits the review's comprehensiveness. (Topic clustering is where multiple members overlap on literature review research leading to both decreased efficiency and decreased comprehensiveness.)

 By building a comprehensive database of keywords through careful evaluation and designing a computer algorithm to target each topic in the context of undergraduates and mental health, we solve both problems. This algorithm produced 923 pieces of material and an additional 148 were procured by team members from sources such as video, multimedia, and government records, which the algorithm has a limited ability to identify. The sourced material was divided into 51 topics, which were randomly assigned to members for screening to prevent domain knowledge bias. Members screened material through title and abstract based on relevance, selecting 10% of materials to contribute to our analysis.  

# Implementation Details:
Automatically return results from keywords and scrape their PMIDs or other IDs. 
Python Ebscohost discovery API may be used; Google scholar may be used.
Use IDs to automatically populate zotero database. 

The 51 subtopics are available for review in the "weighted_queries.txt" file.

Google Scholar Problems. Google scholar is not very accepting of long queries. Boolean Expressions cannot incorporate parantheses. "|" is used instead of "OR" to preserve order of operations.

Limit search to 2000-2023 to produce relevant data.