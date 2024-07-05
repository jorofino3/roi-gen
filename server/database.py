'''
MongoDB skeleton for ROI generator/solver app

License: MIT
'''

import pymongo
from user import *
from sets import *
from tests import *


def cluster_connect(cluster_URI) -> pymongo.database.Database:
    '''
    Connect to cluster
    '''
    try:
        client = pymongo.MongoClient(cluster_URI)
    except pymongo.errors.ConfigurationError:
        print('Invalid URI host error, check connection string for valid params')
        return None

    # return database
    return client.ROI

if __name__ == '__main__':
    uri = input('cluster uri: ')
    db = cluster_connect(uri)
    #db['users'].drop() # drop db for tests
    #db['sets'].drop() # drop db for tests
    
    #test_create_user(db)
    #test_set(db)
    #test_stats(db)
    #get_timeframe_stats(db)
    #new_stats_test(db)
    #test_get_users(db)
    create_users_test(db)
