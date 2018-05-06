#!/bin/env python

import json, traceback, requests, types, re, getpass, sys, os
from pprint import pformat
import logging
import tarfile
from hysds.celery import app
import boto3
from urlparse import urlparse
#import boto
from hysds_commons.job_rest_utils import single_process_and_submission

import osaka.main


#TODO: Setup logger for this job here.  Should log to STDOUT or STDERR as this is a job
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("copy_data")

def copy_data(dest, query=None):
    print("query : %s" %query)
    print("destination : %s" %dest)

    # query
    es_url = app.conf["GRQ_ES_URL"]
    es_index = app.conf["DATASET_ALIAS"]
    search_url=""   
    if es_url.endswith('/'):
        search_url = '%s%s/_search' % (es_url, es_index)
    else:
        search_url = '%s/%s/_search' % (es_url, es_index)
    print("search_url : %s" %search_url)
    r = requests.post(search_url, data=json.dumps(query))
    
    if r.status_code == 200:
        result = r.json()
        #logging.info("result: %s" % result)
        total = result['hits']['total']
    else:
        logging.error("Failed to query %s:\n%s" % (es_url, r.text))
        logging.error("query: %s" % json.dumps(query, indent=2))
        logging.error("returned: %s" % r.text)
        if r.status_code == 404: total, id = 0, 'NONE'
        else: r.raise_for_status()
    
    print("total : %s" %total)
    # Elastic Search seems like it's returning duplicate urls. Remove duplicates
    unique_urls=[]
    for hit in result['hits']['hits']:
        url = hit['_source']['urls'][0]
        if url not in unique_urls:
            unique_urls.append(url)
    for url in unique_urls:
        dest_url=dest
        print(url)
        dir_name=url.split('/')[-1]
        path=os.path.join(os.getcwd(), dir_name)
        print(path)
	if dest.startswith('http'):
	    dest_url="dav%s" %dest[4:]
	    
        destination=os.path.join(dest_url, dir_name)
	print("Copying %s to %s" %(url, destination))
        osaka.main.transfer(url, destination, measure=True,output="./pge_metrics.json")

def main(query, destination, rulename):
    copy_data(destination, query)

if __name__ == "__main__":
    '''
    Main program of moving data to a specific endpoint
    '''
    #encoding to a JSON object
    query = {}
    query=json.loads(sys.argv[1])
    destination = sys.argv[2]
    rule_name = sys.argv[3]
    # getting the script
    main(query, destination, rule_name)
