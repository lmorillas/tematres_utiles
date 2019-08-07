import requests
import json

topterms = "http://ibersid.eu/tesauros/tesauro_03/vocab/services.php?task=fetchTopTerms&output=json"

buscar = "http://ibersid.eu/tesauros/tesauro_03/vocab/services.php?task=search&output=json&arg=oveja"

exacto = "http://ibersid.eu/tesauros/tesauro_03/vocab/services.php?task=fetch&output=json&arg=oveja"

empieza_por = "http://ibersid.eu/tesauros/tesauro_03/vocab/services.php?task=suggest&arg=ove"

fetchTerm = "http://ibersid.eu/tesauros/tesauro_03/vocab/services.php?task=fetchTerm&arg=1"

fetchAlt = "http://ibersid.eu/tesauros/tesauro_03/vocab/services.php?task=fetchAlt&arg={}&output=json"

fetchDown = "http://ibersid.eu/tesauros/tesauro_03/vocab/services.php?task=fetchDown&arg={}&output=json"

fetchUp  = "http://ibersid.eu/tesauros/tesauro_03/vocab/services.php?task=fetchUp&arg=1&output=json"

fetchRelated  = "http://ibersid.eu/tesauros/tesauro_03/vocab/services.php?task=fetchRelated&arg={}&output=json"

# Retrieve alternative, related and direct hieraquical terms for one term_id
fetchDirectTerms = "http://ibersid.eu/tesauros/tesauro_03/vocab/services.php?task=fetchDirectTerms&arg=1&output=json"

targedTerms = "http://ibersid.eu/tesauros/tesauro_03/vocab//services.php?task=fetchTargetTerms&arg=1&output=json"

relatedTerms = "http://ibersid.eu/tesauros/tesauro_03/vocab/services.php?task=fetchRelatedTerms&arg=1,4"

similar = "http://ibersid.eu/tesauros/tesauro_03/vocab/services.php?task=fetchSimilar&arg=a"

# top 
def get_top_ids():
    r = requests.get(topterms)
    top = json.loads(r.text)
    topids = top.get('result').keys()
    return topids
    
def get_top_values():
    r = requests.get(topterms)
    top = json.loads(r.text)
    topvalues = top.get('result').values()
    return topvalues

def get_hijos(term_id):
    r = requests.get(fetchDown.format(term_id))
    hijos = json.loads(r.text).get('result')
    if hijos:
        return hijos.values()
    else:
        return []

def get_related(term_id):
    r = requests.get(fetchRelated.format(term_id))
    related = json.loads(r.text).get('result')
    if related:
        return related.values()
    else:
        return []

def ingles(termino):
    r = requests.get(fetchAlt.format(termino))
    try:
      data = json.loads(r.text).get('result').popitem()[1]
      return data.get('string')
    except:
      return None

def get_termino(termino):
    tag = termino.get('string')
    clave = ingles(termino.get('term_id'))
    if not clave:
        clave = tag+'_XXX'
    hijos = get_hijos(termino.get('term_id'))
    related = get_related(termino.get('term_id'))
    data = {}
    data['tag'] = tag
    if related:
        data['related'] = [ingles(r.get('term_id')) for r in related]
    data['keywords'] = [tag]
    data['children'] = [get_termino(x) for x in hijos]
    return {clave : data }

def get_arbol():
    top = get_top_values()    
    return [get_termino(t) for t in top]


if __name__ == '__main__':
    # para usar con api local dockerizada o en remoto en ibersid.eu
    LOCAL = False
    if LOCAL:
        remote = 'http://ibersid.eu/tesauros/tesauro_03/vocab/services.php'
        local = 'http://localhost:8001/vocab/services.php'
        fetchAlt = fetchAlt.replace(remote, local)
        fetchDown = fetchDown.replace(remote, local)
        topterms = topterms.replace(remote, local)
        fetchRelated = fetchRelated.replace(remote, local)

    lista = get_arbol()
    data = dict((key, d[key]) for d in lista for key in d)
    json.dump(data, open('listado_tesauro.json', 'w'))
