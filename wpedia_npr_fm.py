import urllib.request
import json

req = urllib.request.urlopen('https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvlimit=1&rvprop=content&format=json&titles=List_of_NPR_stations')
resp = json.loads(req.read())
wikitext = list(resp['query']['pages'].values())[0]['revisions'][0]['*'] 

stations = [x for x in wikitext.split('|-') if 'FM' in x]
md = [(x[0], x[-2], x[-1]) for x in [ [x.strip().replace('[','').replace(']','') for x in station.split('|') if len(x) > 2 and 'style' not in x and 'colspan' not in x] for station in stations]]
out = '\n'.join([x for x in ['|'.join(x) for x in md] if 'FM' in x])
print(out)
open('npr.tb', 'w').write(out)
