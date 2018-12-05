index_dir = 'stories_index'

import urllib
from whoosh.index import open_dir
from whoosh.qparser import QueryParser


def main():
    q = raw_input('Enter Event to search:')
    ix = open_dir(index_dir)
    words = urllib.splitquery(q) # use tokenizers / analyzers or self implemented
    queryString = q # would be better to actually create a query
    print queryString   
    for word in words:
        if word:
            queryString = queryString + " " + word # would be better to actually create a query      

    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(unicode(queryString))
        results = searcher.search(query, limit=None)
        if len(results) != 0: 
            for res in results:
                print 'title : ',  res['title']
        else:
            print "No Documents Found for the given query %s" % queryString


if __name__ == '__main__':
    main()
