index_dir = 'stories_index'
import operator
import urllib
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import Every
from whoosh.analysis import StemmingAnalyzer,NgramAnalyzer,StandardAnalyzer,SimpleAnalyzer


def main():
    ngramanalyzer = NgramAnalyzer(minsize=2)
    q = input('Enter Event to search:')
    ix = open_dir(index_dir)
    # words = urllib.splitquery(q) # use tokenizers / analyzers or self implemented
    queryString = q # would be better to actually create a query
    print(queryString)
    # with ix.reader() as r:
    #     sug=[(s[0],s[1].doc_frequency()) for s in r.iter_prefix('key','pop')]
    #     print sorted(sug,key=operator.itemgetter(1),reverse=True)
    # for word in words:
    #     if word:
    #         queryString = queryString + " " + word # would be better to actually create a query
    qp = QueryParser('title',schema=ix.schema)
    corrector = ix.searcher().corrector("name")
    print(corrector.suggest(q, limit=3))
    # all_results = ix.searcher().search(qp.parse(''))
    print(qp.parse(' '.join([token.text for token in ngramanalyzer(q)])))
    all_results = ix.searcher().search(qp.parse(' '.join([token.text for token in ngramanalyzer(q)])))
    Finalres = set()
    finalresult = []
    for i in all_results:
        if i['name'] not in Finalres:
            finalresult.append(i)
            Finalres.add(i['name'])

    for i in finalresult:
        print(i['name'])


if __name__ == '__main__':
    main()
