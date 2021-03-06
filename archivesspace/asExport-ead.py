#!/usr/bin/env python

import os, requests, json, sys, logging, ConfigParser

config = ConfigParser.ConfigParser()
config.read('local_settings.cfg')
dictionary = {'baseURL': config.get('ArchivesSpace', 'baseURL'), 'repository':config.get('ArchivesSpace', 'repository'), 'user': config.get('ArchivesSpace', 'user'), 'password': config.get('ArchivesSpace', 'password'), 'destination': config.get('Destinations', 'EADdestination')}

# parses arguments, if any. This allows you to pass in an string to match against resource IDs
exportIds = sys.argv[1]
logging.basicConfig(filename='simple-log.txt',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

# authenticates the session
def authenticate():
    auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
    session = auth["session"]
    headers = {'X-ArchivesSpace-Session':session}
    return headers

headers = authenticate()

# Gets the IDs of all resources in the repository
logging.info('Getting a list of resources')
resourceIds = requests.get(baseURL + '/repositories/'+repository+'/resources?all_ids=true', headers=headers)

# Exports EAD for all resources whose IDs contain argument
for id in resourceIds.json():
    if not requests.get(baseURL + '/repositories/'+repository+'/resources/' + str(id), headers=headers):
        headers = authenticate()
    resource = (requests.get(baseURL + '/repositories/'+repository+'/resources/' + str(id), headers=headers)).json()
    resourceID = resource["id_0"]
    if exportIds:
        if exportIds in resourceID:
            logging.info('Exporting ' + resourceID)
            ead = requests.get(baseURL + '/repositories/'+repository+'/resource_descriptions/'+str(id)+'.xml', headers=headers, stream=True)
            if not os.path.exists(destination):
                os.makedirs(destination)
            with open(destination+resourceID+'.xml', 'wb') as f:
                for chunk in ead.iter_content(10240):
                    f.write(chunk)
            f.close
    else:
        logging.info('Exporting ' + resourceID)
        ead = requests.get(baseURL + '/repositories/'+repository+'/resource_descriptions/'+str(id)+'.xml', headers=headers, stream=True)
        if not os.path.exists(destination):
            os.makedirs(destination)
        with open(destination+resourceID+'.xml', 'wb') as f:
            for chunk in ead.iter_content(10240):
                f.write(chunk)
        f.close
logging.info('Done!')
