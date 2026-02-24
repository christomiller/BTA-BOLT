import html
import json

jsonpath = 'properties/bta_properties.json'
templatepath = 'PropertyTemplate.html'


try:
    with open(jsonpath, 'r') as file:
        data = json.load(file)
        
#        for obj in data:
#            print(obj['key'])
        
except FileNotFoundError:
    print('Error: The file',filepath,'was not found.')
except json.JSONDecodeError:
    print("Error: Failed to decode JSON from the file (malformed JSON).")

with open(templatepath, 'r') as t:
    template = t.read()
    t.close()
    
def getProperties(jsondata):
    properties = {}
    for prop in jsondata:
        properties[prop['key']] = prop
    return properties
        
def setHtml(html, prop):
    propPage = ''
    newPage = html
    
    
    
#    CR PDF
    newPage = newPage.replace('__CR_PDF__', '')
#    prop['Property'])
#    EASEMENT PDF
    newPage = newPage.replace('__EASEMENT_PDF__', '')
#    prop['Property'])
#    LEASE
    newPage = newPage.replace('__LEASE__', '')
#    prop['Property']),
#    DEED PDF
    newPage = newPage.replace('__DEED_PDF__', '')
#    prop['Property'])
#    SCANNED DOCS PDF
    newPage = newPage.replace('__DOCS_PDF__', '')
#    prop['Property'])
    
#    PropertyName
    newPage = newPage.replace('__PROPERTY_NAME__', prop['Property'])
#    PropertyType
    if prop['property id'] <= 17:
        pType = 'FEE'
    else:
        pType = "CR"
    newPage = newPage.replace('__PROPERTY_TYPE__', pType)
#    Location
    newPage = newPage.replace('__LOCATION__', prop['Address'])
#    Entry
    newPage = newPage.replace('__ENTRY__', prop['best_entry'])
#    Size
    newPage = newPage.replace('__SIZE__', str(prop['Acres']))
#    Present Use
    newPage = newPage.replace('__PRESENT_USE__', prop['present_use'])
#    Owner
    newPage = newPage.replace('__OWNER__', prop['Owner'])
#    CR?
    newPage = newPage.replace('__CR?__', prop['CR'])
#    CR Owner
    newPage = newPage.replace('__CR_OWNER__', '') 
    #prop['CR_Owner'])
    
#    Map Link
    newPage = newPage.replace('__MAP_LINK__', prop['google_link'])
    
#    Image
    newPage = newPage.replace('__IMAGE__',  '../images/'+prop['image_name']) 
    with open('properties/pages/'+prop['Property']+'.html', 'w') as wp:
        wp.write(newPage)
        wp.close()
    
    
#    print(html)
    
if __name__ == '__main__':
    print('running')
    properties = getProperties(data)
    print(properties['achenbach'])
    for prop in properties:
        setHtml(template, properties[prop])