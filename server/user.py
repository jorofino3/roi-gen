'''
Functions for user interactions

License: MIT
'''

import pymongo
import hashlib
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

def create_user(db, email: str, password: str, name: str = "unnamed") -> bool:
    '''
    Create a new user entry
    Users identified by email
    Will not allow multiple accounts with the same email
    '''
    users = db['users']
    
    # dont create user that already exists
    if user_exists(db, email):
        print('User ' + email + ' already exists')
        return
    
    # hash password
    password = password + '10millionfireflies'
    hash_pwd = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    doc = {
            'email': email,
            'password': hash_pwd,
            'name': name,
            'global_stats': {},
            'set_info': [],
            'bookmarked': [],
            'date_created': str(date.today())
            }
    users.insert_one(doc)

    return True

def user_exists(db, email: str) -> bool:
    '''
    Check if user exists
    '''
    users = db['users']

    count = users.count_documents({ 'email': email })
    return count == 1

def update_user_param(db, email: str, key: str, value):
    '''
    Update/insert new parameter into given user
    '''
    users = db['users']
    if not user_exists(db, email):
        print('User ' + email + ' does not exist. Cannot update ' + key)
        return
    if key == 'email' or key == 'password':
        print('Cannot update param ' + key + ' of user ' + email)
        return

    filter = { 'email': email }
    new_param = { '$set': { key: value } }
    users.update_one(filter, new_param)

def valid_login(db, email: str, password: str) -> bool:
    '''
    Determine if login attempt is successful
    '''
    users = db['users']

    if not user_exists(db, email):
        print('Login failed, user does not exist')
        return False
    
    filter = { 'email': email }
    doc = users.find_one(filter)
    stored_pwd = doc['password']
    password = password + '10millionfireflies'
    hash_pwd = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    return stored_pwd == hash_pwd

def guest_login(db):
    '''
    Login as guest, no sign in required, just make sure that guest exists
    '''
    users = db['users']

    if not user_exists(db, 'guest'):
        create_user(db, 'guest', 'guest', 'Guest User')

def user_is_guest(db, email) -> bool:
    '''
    Return if current user is guest
    '''
    return email == 'guest'

def get_user(db, email: str) -> dict:
    '''
    Return a user identified by the email
    '''
    users = db['users']

    if not user_exists(db, email):
        print('Cannot return user ' + email + ', does not exist')
        return None

    filter = { 'email': email }
    doc = users.find_one(filter)
    return doc

def get_user_param(db, email: str, key: str):
    '''
    Return corresponding value in user
    '''
    if key == 'password':
        print('Cannot return password of user ' + email)
        return

    doc = get_user(db, email)
    if key in doc.keys():
        return doc[key]
    return None

def update_set_stats(db, email: str, name: str, att: int, corr: int, done: list):
    '''
    Update user statistics for a problem set
    '''
    if not user_exists(db, email):
        print('User ' + email + ' does not exist, cannot init problem set.')
        return
    
    # create/update entry
    set_info = get_user_param(db, email, 'set_info')
    idx = get_set_idx(db, email, name)
    if idx == -1:
        doc = {
            'name': name,
            'attempts': att,
            'correct': corr,
            'done': done
        }
        set_info.append(doc)
    else:
        set_info[idx]['attempts'] = att
        set_info[idx]['correct'] = corr
        set_info[idx]['done'] = done
    
    # update db with new info
    update_user_param(db, email, 'set_info', set_info)

def init_set_stats(db, email: str, name: str):
    '''
    Init user statistics for a problem set
    '''
    update_set_stats(db, email, name, 0, 0, [])

def correct_ans(db, email: str, name: str, corr_idx: int):
    '''
    Update corresponding user stats with correct problem
    '''
    users = db['users']
    if not user_exists(db, email):
        print('Cannot update user ' + email + ', does not exist')
        return

    # get specific problem set doc
    set_info = get_user_param(db, email, 'set_info')
    idx = get_set_idx(db, email, name)
    if idx == -1:
        print('Set not in user set info. Returning')
        return
    
    # update params and send to db
    att = set_info[idx]['attempts'] + 1
    corr = set_info[idx]['correct'] + 1
    done = set_info[idx]['done']
    if corr_idx not in done:
        done.append(corr_idx)
    update_set_stats(db, email, name, att, corr, done)
    increment_total_stats(db, email, True, True)

def incorrect_ans(db, email: str, name: str):
    '''
    Update user stats with incorrect problem
    '''
    users = db['users']
    if not user_exists(db, email):
        print('Cannot update user ' + email + ', does not exist')
        return 
    
    # get specific problem set doc
    set_info = get_user_param(db, email, 'set_info')
    idx = get_set_idx(db, email, name)
    if idx == -1:
        print('Set not in user set info. Returning')
        return
    
    # update params and send to db
    att = set_info[idx]['attempts'] + 1
    corr = set_info[idx]['correct']
    done = set_info[idx]['done']
    update_set_stats(db, email, name, att, corr, done)
    increment_total_stats(db, email, True, False)

def get_set_idx(db, email: str, name: str) -> int:
    '''
    Return the index of a problem set in the set_info array
    Returns -1 if not in list
    '''
    set_info = get_user_param(db, email, 'set_info')
    idx = -1
    for i in range(0, len(set_info)):
        if set_info[i]['name'] == name:
            idx = i
            break
    return idx

def increment_total_stats(db, email: str, att: bool, corr: bool):
    '''
    Increment total stats for user
    '''
    if not user_exists(db, email):
        print('User ' + email + ' does not exist, cannot init problem set.')
        return
    
    # update entry
    attempts = get_user_param(db, email, 'total_attempts')
    if att:
        attempts += 1
    correct = get_user_param(db, email, 'total_correct')
    if corr:
        correct += 1
    
    # send results to db
    update_user_param(db, email, 'total_attempts', attempts)
    update_user_param(db, email, 'total_correct', correct)

def add_bookmarked_prob(db, email: str, prob: dict):
    '''
    Bookmark a given problem
    '''
    if not user_exists(db, email):
        print('User ' + email + ' does not exist, cannot bookmark problem.')
        return
    if user_is_guest(db, email):
        print('Guest user cannot bookmark problems')
        return
    
    bookmarked = get_user_param(db, email, 'bookmarked')

    if prob not in bookmarked:
        bookmarked.append(prob)
        update_user_param(db, email, 'bookmarked', bookmarked)
    else:
        print('Problem already exists in bookmarked set')

def get_bookmarked_len(db, email: str):
    '''
    Get number of bookmarked problems
    '''
    if not user_exists(db, email):
        print('User ' + email + ' does not exist, cannot retrieve bookmark len.')
        return
    if user_is_guest(db, email):
            print('Guest user cannot bookmark problems')
            return

    bookmarked = get_user_param(db, email, 'bookmarked')
    return len(bookmarked)

def get_bookmarked_prob(db, email: str, idx: int) -> dict:
    '''
    Return bookmarked problem in bookmarked list
    '''
    if not user_exists(db, email):
        print('User ' + email + ' does not exist, cannot bookmarked problem.')
        return
    if user_is_guest(db, email):
            print('Guest user cannot bookmark problems')
            return
    if idx >= get_bookmarked_len(db, email) or idx < 0:
        print('Invalid bookmark problem index: ' + str(idx))
        return

    bookmarked = get_user_param(db, email, 'bookmarked')
    return bookmarked[idx]
   
def remove_bookmarked_prob(db, email: str, idx: int):
    '''
    Remove problem from bookmarked list
    '''
    if not user_exists(db, email):
        print('User ' + email + ' does not exist, cannot remove bookmarked problem.')
        return
    if user_is_guest(db, email):
            print('Guest user cannot bookmark problems')
            return
    if idx >= get_bookmarked_len(db, email) or idx < 0:
        print('Invalid bookmark problem index: ' + str(idx))
        return

    bookmarked = get_user_param(db, email, 'bookmarked')
    rem = bookmarked[idx]
    bookmarked.remove(rem)
    update_user_param(db, email, 'bookmarked', bookmarked)

def get_existing_users(db) -> list:
    '''
    Return all users created in last 6 months for exporting user stats
    '''
    users = db['users']
    emails = []
    lim = datetime.today() + relativedelta(months=-6)
    lim = lim.date()

    # get all documents
    docs = users.find(None)

    for doc in docs:
        # pass on documents without date created (legacy docs)
        if 'date_created' not in doc.keys():
            continue

        # if date created within 6 months, append email
        date_created = doc['date_created']
        created = datetime.strptime(date_created, "%Y-%m-%d").date() 
        if created >= lim:
            emails.append(doc['email'])
            
    return emails 
