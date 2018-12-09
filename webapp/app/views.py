from django.shortcuts import render,HttpResponse
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt

from whoosh.analysis import NgramAnalyzer,SimpleAnalyzer
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
# Create your views here.
ix = open_dir(settings.WHOOSH_INDEX,indexname=settings.WHOOSH_INDEX_NAME)
tokenizer = SimpleAnalyzer()
searcher = ix.searcher()
corrector = searcher.corrector("name")
ngram = NgramAnalyzer(minsize=2,maxsize=4)
qp = QueryParser('title',schema=ix.schema)

def mainpage(request):
    return render(request,'app/index.html')

@csrf_exempt
def load(request):
    data = request.POST.get('data')
    last = None
    for token in tokenizer(data):
        last = token.text
    print(last)
    query = qp.parse(' '.join([token.text for token in ngram(last)]),)
    all_results = searcher.search(query)
    Finalres = set()
    finalresult = []
    for i in all_results:
        if i['name'] not in Finalres:
            finalresult.append(i['name'])
            Finalres.add(i['name'])
    data = {'correction':corrector.suggest(last, limit=3),'suggestion':finalresult,'next_word':[]}
    return HttpResponse(json.dumps(data), content_type='application/json')
