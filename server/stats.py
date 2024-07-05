'''
Functions for user interactions

License: MIT
'''

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from user import *


def increment_global_stats(db, email: str, diff: str, correct: bool):
    '''
    Update global stats after a user attempts a problem
    global_stats maps a date to a dictionary of tuples
    the tuples correspond to easy, medium, and hard problems
    each tuple contains stats for total attempts and number correct
    '''

    if not user_exists(db, email):
        print('User ' + email + ' does not exist. Cannot update global stats')
        return
    if user_is_guest(db, email):
        # do not track statistics for guest user
        print('Cannot update statistics for guest user')
        return
    if diff not in ['beginner', 'intermediate', 'advanced']:
        print('Invalid difficulty selection')
    
    # update global_stats entry
    global_stats = get_user_param(db, email, 'global_stats')
    current_date = str(date.today())

    tup = None
    if current_date in global_stats.keys():
        if diff in global_stats[current_date].keys():
            tup = global_stats[current_date][diff]
    else:
        # make sure that current_date's dict exists
        global_stats[current_date] = {}

    tup = update_tup(tup, correct)
    global_stats[current_date][diff] = tup
    update_user_param(db, email, 'global_stats', global_stats)

def update_tup(tup: tuple, correct: bool) -> tuple:
    '''
    Update/create a tuple of problem stats
    '''
    corr = 0
    if correct:
        corr = 1
    
    if tup == None:
        tup = (1, corr)
    else:
        att = tup[0] + 1
        cor = tup[1] + corr
        tup = (att, cor)
    
    return tup

def get_global_stats(db, email: str) -> dict:
    '''
    Return global stats dictionary
    Maps dates to (attemts, correct)
    '''
    if not user_exists(db, email):
        print('User ' + email + ' does not exist. Cannot retrieve global stats')
        return None
    if user_is_guest(db, email):
        # do not track statistics for guest user
        print('Cannot retrieve statistics for guest user')
        return None
    
    global_stats = get_user_param(db, email, 'global_stats')
    return global_stats

def get_stats_dates(db, email: str, timeframe: str) -> list:
    '''
    Return global stats dictionary
    Maps dates to (attemts, correct)
    '''
    if not user_exists(db, email):
        print('User ' + email + ' does not exist. Cannot retrieve global stats dates')
        return None
    if user_is_guest(db, email):
        # do not track statistics for guest user
        print('Cannot retrieve dates for guest user')
        return None
    
    global_stats = get_user_param(db, email, 'global_stats')
    keys = list(global_stats.keys()).copy()
    keys = sorted(keys)

    # handle case where no entries exist
    if len(keys) == 0:
        return []

    # get dates matching timeframe
    tod = date.today()
    lim = None
    match timeframe:
        case 'day':
            lim = tod + relativedelta(days=-1)
        case 'week':
            lim = tod + relativedelta(weeks=-1)
        case 'month':
            lim = tod + relativedelta(months=-1)
        case '3month':
            lim = tod + relativedelta(months=-3)
        case '6month':
            lim = tod + relativedelta(months=-6)
        case _:
            # default is 1 week
            lim = tod + relativedelta(weeks=-1)

    filtered_dates = [date for date in keys if datetime.strptime(date, "%Y-%m-%d").date() >= lim]
    return filtered_dates

def get_day_stats(db, email: str) -> dict:
    '''
    Return stats over last day
    '''
    global_stats = get_global_stats(db, email)
    dates = get_stats_dates(db, email, 'day')
    filtered = {key: global_stats[key] for key in dates if key in global_stats}
    return filtered

def get_week_stats(db, email: str) -> dict:
    '''
    Return stats over last week
    '''
    global_stats = get_global_stats(db, email)
    dates = get_stats_dates(db, email, 'week')
    filtered = {key: global_stats[key] for key in dates if key in global_stats}
    return filtered

def get_month_stats(db, email: str) -> dict:
    '''
    Return stats over last month
    '''
    global_stats = get_global_stats(db, email)
    dates = get_stats_dates(db, email, 'month')
    filtered = {key: global_stats[key] for key in dates if key in global_stats}
    return filtered

def get_3month_stats(db, email: str) -> dict:
    '''
    Return stats over last 3 months
    '''
    global_stats = get_global_stats(db, email)
    dates = get_stats_dates(db, email, '3month')
    filtered = {key: global_stats[key] for key in dates if key in global_stats}
    return filtered

def get_6month_stats(db, email: str) -> dict:
    '''
    Return stats over last 6 months
    '''
    global_stats = get_global_stats(db, email)
    dates = get_stats_dates(db, email, '6month')
    filtered = {key: global_stats[key] for key in dates if key in global_stats}
    return filtered

