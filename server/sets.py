'''
Functions for problem set interactions

License: MIT
'''

def create_set(db, name: str, problems: list):
    '''
    Create a new set entry
    Sets identified by a name
    Contains a list of problem documents
    '''
    sets = db['sets']

    # dont create set that already exists
    if set_exists(db, name):
        print('Set ' + name + ' already exists')
        return
    
    doc = {
        'name': name,
        'problems': problems,
        'size': len(problems)
    }
    sets.insert_one(doc)

def set_exists(db, name: str) -> bool:
    '''
    Check if problem set exists
    '''
    sets = db['sets']

    count = sets.count_documents({ 'name': name })
    return count == 1

def get_set(db, name: str) -> dict:
    '''
    Return the problem set with the given name
    '''
    sets = db['sets']

    if not set_exists(db, name):
        print('Cannot return set ' + name + ', does not exist')
        return None
    
    filter = { 'name': name }
    doc = sets.find_one(filter)
    return doc

def update_problem_list(db, name: str, problems: list):
    '''
    Update list of problems in a problem set
    '''
    sets = db['sets']
    if not set_exists(db, name):
        print('Set ' + name + ' does not exist. Cannot update problem set')
        return
    
    filter = { 'name': name }
    new_problems = { '$set': { 'problems': problems,
                               'size' : len(problems) 
                             } }
    sets.update_one(filter, new_problems)

def get_problem(db, name: str, idx: int) -> dict:
    '''
    Get a specific problem from a problem set
    '''
    sets = db['sets']
    doc = get_set(db, name)
    if doc == None:
        return None
    
    problems = doc['problems']
    
    # cannot get problem with invalid index
    if idx >= len(problems) or idx < 0:
        print('Invalid index for get_problem: ' + str(idx))
        return None
    
    prob = problems[idx]
    return prob

def get_size(db, name: str) -> int:
    '''
    Return size of problem set
    '''
    sets = db['sets']
    doc = get_set(db, name)
    if doc == None:
        return None
    
    return doc['size']