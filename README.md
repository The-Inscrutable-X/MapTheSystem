# MapTheSystem

Goal: Enable massive and comprehensive literary search by searching multiple sources (peer reviewed papars, editorials, social media, papers in other languages, etc) for a list of topics and compiling the results in a zotero database. The Journal of Medical Internet Research (JMIR) has many examples of people who may find this tool useful in literary search.

Notes: Automatically return results from keywords and scrape their PMIDs or other IDs. Python Ebscohost discovery API may be used (account needed); Google scholar may be used (more work needed with scholarly and ScraperAPI) Use IDs to automatically populate zotero database.

Google Scholar Problems. Google scholar is not very accepting of long queries. Boolean Expressions cannot incorporate parantheses. | is used instead of OR to serve as a sort of pseduo parathesis based on order of operations, it seems to have a limited but observable effect.

Correction: Boolean Search appears to work, but longer queries are cut off and the operation precedence is abnormal. AND and OR seem not to have usual precedence, although && is still higher in precedence than OR, and presumably | is higher in precedence than AND (it so far seems this way).

Limit search to 2003-2023.