from pyzotero import zotero

zot = zotero.Zotero("4939465", "group", "MLD9GooAjlNi3H5XdkW7dijP")

template = zot.item_template('JournalArticle')
print(template)