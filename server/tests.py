'''
Unit tests and feature demos

License: MIT
'''

from user import *
from sets import *
from stats import *

problems = [
        {
            'statements': ['p->q', 'q'],
            'solutions': ['p']
        },
        {
            'statements': ['p->q', '~q'],
            'solutions': ['~p']
        },
        {
            'statements': ['p->q', 'q->r'],
            'solutions': ['p->r']
        }
    ]


def test_create_user(db):

    email = 'test@test.com'
    password = 'pass'
    name = 'Test User'

    print('\nCreating user with following params:')
    print('email: ' + email)
    print('password: ' + password)
    print('name: ' + name)
    create_user(db, email, password, name)
    print()

    print('Testing login with original password')
    print(valid_login(db, email, password))

    print('Testing login with incorrest password: pasw')
    print(valid_login(db, email, 'pasw'))
    print()

def test_set(db):
    email = 'tristan@test.com'
    pwd = 'password'
    usr_name = 'Tristan Rogers'
    create_user(db, email, pwd, usr_name)

    set_name = 'rules'
    
    create_set(db, set_name, problems)
    init_set_stats(db, email, set_name)
    
    # showcase problems
    for i in range(0, get_size(db, set_name)):
        print('Question ' + str(i) + ':')
        p = get_problem(db, set_name, i)
        for statement in p['statements']:
            print(statement)
        ans = input('answer: ')
        if ans == p['solutions'][0]:
            print('Correct!')
            correct_ans(db, email, set_name, i)
        else:
            print('Incorrect.')
            incorrect_ans(db, email, set_name)
        print()

    user_doc = get_user(db, email)
    set_idx = get_set_idx(db, email, set_name)
    set_doc = get_user_param(db, email, 'set_info')[set_idx]
    print('User stats:')
    print('Name: ' + user_doc['name'])
    print('Total attempts: ' + str(user_doc['total_attempts']))
    print('Total correct: ' + str(user_doc['total_correct']))
    #percent = float(user_doc['total_correct']) / float(user_doc['total_attempts'])
    #print('Percent correct: ' + str(percent))

    print('Problem set: ' + set_doc['name'])
    print('Attempts: ' + str(set_doc['attempts']))
    print('Correct: ' + str(set_doc['correct']))
    print('Done: ' + str(set_doc['done']))
    

def test_bookmark(db):
    email = 'bookmark@test.com'
    pwd = 'password'
    usr_name = 'Book Mark'
    create_user(db, email, pwd, usr_name)

    hard_prob = problems[0]
    add_bookmarked_prob(db, email, hard_prob)
    hard_prob = problems[2]
    add_bookmarked_prob(db, email, hard_prob)
    
    # get length of bookmarked prob list
    sz = get_bookmarked_len(db, email)
    print('Size of bookmarked list: ' + str(sz) + '\n')

    # lets see what we bookmarked - easy to iterate over
    print('Current bookmarked probs:')
    for idx in range(0, sz):
        print(get_bookmarked_prob(db, email, idx))
    print()

    # try to access invalid index
    print('Attempting to access invalid index: 2')
    prob = get_bookmarked_prob(db, email, 2)
    print()
    
    # remove problem and loop again using previous size: will return None for idx == 1
    print('Removing index 0 from list and attempting same loop as before:')
    remove_bookmarked_prob(db, email, 0)
    for idx in range(0, sz):
        print(get_bookmarked_prob(db, email, idx))
    print('The correct problem was removed, and index 1 is now invalid as the size has decreassed')


def test_stats(db):
    email = 'stats@test.com'
    pwd = 'password'
    usr_name = 'Stats Test'
    create_user(db, email, pwd, usr_name)

    # update global stats using functions
    increment_global_stats(db, email, True)
    increment_global_stats(db, email, False)
    increment_global_stats(db, email, True)
    print('Updating values with functions: ')
    print(get_global_stats(db, email))

    # manually insert values to test list sorting
    key = '2023-01-01'
    val = (4, 3)
    glob = get_user_param(db, email, 'global_stats')
    glob[key] = val
    update_user_param(db, email, 'global_stats', glob)

    key = '2023-02-26'
    val = (15, 13)
    glob = get_user_param(db, email, 'global_stats')
    glob[key] = val
    update_user_param(db, email, 'global_stats', glob)

    key = '2023-02-28'
    val = (12, 11)
    glob = get_user_param(db, email, 'global_stats')
    glob[key] = val
    update_user_param(db, email, 'global_stats', glob)

    print('Manually inserting values: ')
    print(get_global_stats(db, email))

    # update today's value again!
    increment_global_stats(db, email, True)
    print('Updated value for today')
    print(get_global_stats(db, email))

def get_timeframe_stats(db):
    email = 'stats@test.com'
    pwd = 'password'
    usr_name = 'Stats Test'
    create_user(db, email, pwd, usr_name)

    print('Testing zero inputs')
    print(get_day_stats(db, email))
    print(get_week_stats(db, email))
    print(get_month_stats(db, email))
    print(get_3month_stats(db, email))
    print(get_6month_stats(db, email))


    # insert stats for today
    increment_global_stats(db, email, True)
    increment_global_stats(db, email, False)
    increment_global_stats(db, email, True)

    # insert stats for this week
    key = '2023-10-25'
    val = (1, 1)
    glob = get_user_param(db, email, 'global_stats')
    glob[key] = val
    update_user_param(db, email, 'global_stats', glob)

    # insert stats for this month 
    key = '2023-10-03'
    val = (1, 1)
    glob = get_user_param(db, email, 'global_stats')
    glob[key] = val
    update_user_param(db, email, 'global_stats', glob)

    # insert stats for three months
    key = '2023-09-03'
    val = (1, 1)
    glob = get_user_param(db, email, 'global_stats')
    glob[key] = val
    update_user_param(db, email, 'global_stats', glob)

    # insert stats for six months
    key = '2023-05-03'
    val = (1, 1)
    glob = get_user_param(db, email, 'global_stats')
    glob[key] = val
    update_user_param(db, email, 'global_stats', glob)
    
    print('Should see correct timeframe for each set of keys')
    print(get_day_stats(db, email))
    print(get_week_stats(db, email))
    print(get_month_stats(db, email))
    print(get_3month_stats(db, email))
    print(get_6month_stats(db, email))


def new_stats_test(db):
    email = 'stats2@test.com'
    pwd = 'password'
    usr_name = 'Stats Test'
    create_user(db, email, pwd, usr_name)

    print('Testing zero inputs')
    print(get_day_stats(db, email))
    print(get_week_stats(db, email))
    print(get_month_stats(db, email))
    print(get_3month_stats(db, email))
    print(get_6month_stats(db, email))


    # insert stats for today
    increment_global_stats(db, email, 'beginner', True)
    increment_global_stats(db, email, 'beginner', False)
    increment_global_stats(db, email, 'beginner', True)

    increment_global_stats(db, email, 'intermediate', True)
    increment_global_stats(db, email, 'intermediate', True)
    increment_global_stats(db, email, 'intermediate', True)

    increment_global_stats(db, email, 'advanced', False)
    increment_global_stats(db, email, 'advanced', False)
    increment_global_stats(db, email, 'advanced', True)

    print('day stats:')
    print(get_day_stats(db, email))

def test_get_users(db):
    email = 'email@email.com'
    pwd = 'password'
    usr_name = 'Test1'
    create_user(db, email, pwd, usr_name)


    print(get_existing_users(db))


def create_users_test(db):
    create_user(db, 'a', 'pass', 'a name')
    create_user(db, 'b', 'pass', 'b name')
    create_user(db, 'c', 'pass', 'c name')

    print(get_existing_users(db))
