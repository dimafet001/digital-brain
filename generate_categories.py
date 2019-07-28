#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 17:50:58 2019

@author: marley
"""

import json
import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/marley/Downloads/googlecloudcredential.json"
client = language.LanguageServiceClient()

def get_category(url):
    r = requests.get(url)
    text = r.text
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')
    document = types.Document(
        content=text.encode('utf-8'),
        type=language.enums.Document.Type.HTML)
    try:
        categories = client.classify_text(document).categories
    except:
        return "error"
    if len(categories):
        return categories[0].name
    else:
        return "error"

# read file
with open('hist1000.json', 'r') as myfile:
    f=myfile.read()
    # parse file
    history = json.loads(f)
data = {}

def isvalid(row):
    title = row['title'].lower()
    if "google" in title or "gmail" in title or "facebook" in title or "sign in" in title or "youtube" in title:
        return False
    return True

idx = 0
for row in history:
    idx +=1
    if isvalid(row):
        data[row['id']] = row
        if idx % 20 == 0:
            print(row['title'])

""" create a new structure for organizing the content by category
    {group_name: {
                    data_: []
                    subgroup1: {...}
                    subgroup2: {...}
                }
    }
"""
import time
start_time = time.time()
group = {}
valid_ids = []
num_done = 0
for id, info in data.items():
    category = get_category(info['url'])
    info['category'] = category
    if category != "error":
        num_done +=1
        if num_done % 10 == 0:
            print("finished {} in {} seconds".format(num_done, time.time() - start_time))
        valid_ids.append(id)
        curr_group = group
        for subset in category.split('/'):
            if subset in curr_group:
                curr_group[subset]['data'].append(id)
            else:
                curr_group[subset] = {'data':[id]}
            curr_group = curr_group[subset]
group = group['']

""" sort data by importance (right now 'importance' is visitCount)

"""
def sort_arr(arr):
    d = {}
    for id in arr:
        d[id] = data[id]['visitCount']
    d = sorted(d.items(), key=lambda x: x[1], reverse=True)
    new_arr = [k for k,v in d]
    return new_arr
def sort_data(group):
    for key, info in group.items():
        if key == 'data':
            group[key] = sort_arr(info)
        else:
            sort_data(info)


metadata = {}
import datetime
import random
now = datetime.datetime.strptime("7/27/2019","%m/%d/%Y")

def get_info(prev_dict):
    new_dict = {}
    then = datetime.datetime.strptime(prev_dict['lastVisitTimeLocal'].split(',')[0], "%m/%d/%Y")
    delta = (then-now)
    time_str = ""
    if delta.days > 7:
        time_str = str(int(delta.days/7)) + " weeks ago"
    else:
        time_str = str(delta.days) + " days ago"
    new_dict['lastVisited'] = time_str
    new_dict['visitCount'] = prev_dict['visitCount']
    new_dict['hours'] = random.randint(1, int(prev_dict['visitCount']*1.5))/2
    new_dict['url'] = prev_dict['url']
    new_dict['title'] = prev_dict['title']

    return new_dict
    
for id in valid_ids:
    metadata[id] = get_info(data[id])
