#Author -Chit Zin Win
import requests, json
import pandas as pd

def load_datasets_web():
    url="http://grdata-grandrapids.opendata.arcgis.com/api/v3/datasets" 
        
    #GRData's id = L81TiOwAPO1ZvU9b
    params = {"page[size]":90, "filter[orgId]":"L81TiOwAPO1ZvU9b", "filter[type]":"any(Feature Layer,Table)"} 
    
    r=requests.post(url,params=params)
    
    dr=json.loads(r.content.decode('utf-8'))
    
    df=dr['data']    
    
    while("next" in dr['links']):
        r=requests.post(dr['links']['next'])
        dr=json.loads(r.content.decode('utf-8'))
        if 'data' in dr: df=df+dr['data']
        
    df=pd.DataFrame([i['attributes'] for i in df])[["name","id","fieldNames","recordCount","size",'description','type','statistics','tags','serverCapabilities','orgName','created','url']]
        
    return(df)



from arcgis.gis import GIS
from arcgis import features

gis = GIS()

#GRDATA's orgId on opendata is L81TiOwAPO1ZvU9b
def load_datasets():
   items = gis.content.search(query="orgid: L81TiOwAPO1ZvU9b AND type: Feature Layer OR Table", max_items=10000)
   return(pd.DataFrame([dict(i.items()) for i in items])[["title","id","snippet",'description','tags','type','url']])


def getdf_byid(id, layer=0,query="1=1"):
    item=gis.content.get(id)
    return(features.FeatureLayer.fromitem(item,int(layer)).query(where=query).df)
    
    
def get_layersinfo(id):
    item=gis.content.get(id)
    if "layers" in item:
        return(pd.DataFrame([{"name":l.properties.name, "fields": ",".join([f['name'] for f in l.properties.fields]), "type":l.properties.type, "url":l.url, "serviceItemId": None if "serviceItemId" not in l.properties else l.properties.serviceItemId, "layer_number": l.properties.id} for l in item.layers]))
    else: 
        return(None)
        
        
def get_fieldsinfo(id, layer=0):
    return(pd.DataFrame(features.FeatureLayer.fromitem(gis.content.get(id),int(layer)).properties.fields))
    
def getdf_bytitle(title, layer=0):
   fl = gis.content.search("title: %s" % title, item_type="Feature Layer")
   if len(fl) > 0:
       fl=fl[int(layer)]
   else:
       return None
   
   if len(fl.layers) > 0:
       return(fl.layers[0].query().df)
   elif len(fl.tables) > 0:
       return(fl.tables[0].query().df)
   
    
    
    

    
    
    

#for i in items:
#    tbls = i.tables
#    if tbls is not None and len(tbls) > 0:
#        print(tbls) 
#    else:
#        if  i.layers is not None and len(i.layers) > 0:
#            print(i.layers[0])
    

    
#
#for f in fs.properties.fields:
#    print(f['name'])
#    
#    
#for i in df:
#    print(i['attributes']['name'])
#    print([v['name'] for v in FeatureLayer(i['attributes']['url']).properties.fields])