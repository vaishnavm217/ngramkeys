index_dir = 'stories_index'
import operator
import urllib
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import Every
from whoosh.analysis import StemmingAnalyzer,NgramFilter,StandardAnalyzer,SimpleAnalyzer


def main():
    q = raw_input('Enter Event to search:')
    ix = open_dir(index_dir)
    words = urllib.splitquery(q) # use tokenizers / analyzers or self implemented
    queryString = q # would be better to actually create a query
    print queryString   
    # with ix.reader() as r:
    #     sug=[(s[0],s[1].doc_frequency()) for s in r.iter_prefix('key','pop')]
    #     print sorted(sug,key=operator.itemgetter(1),reverse=True)
    # for word in words:
    #     if word:
    #         queryString = queryString + " " + word # would be better to actually create a query      
    qp = QueryParser('key',schema=ix.schema)
    co = ix.searcher().collector(collapse='key')
    corrector = ix.searcher().corrector("word")
    print corrector.suggest(q, limit=3)
    my_analyzer = SimpleAnalyzer() | NgramFilter(minsize=2, maxsize=4)
    # all_results = ix.searcher().search(qp.parse(''))
    for term in my_analyzer(unicode(q)):
        print term.text
        all_results = ix.searcher().search(qp.parse(term.text))
    for i in all_results:
        print i['word'],i['key'],i.score


if __name__ == '__main__':
    main()
