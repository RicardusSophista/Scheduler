#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 18:08:02 2020

@author: richard

TODO
monthly, weekly, annual payment schedules
FIRST = short month > first day of next month
LAST = short month > last day of month

YES = day1 is last day of month
    NO = day1 is regular day of month

WEEKENDS = if SKIP, do not use weekends
HOLIDAY = if populated, use list of holidays
"""

import datetime as dt
import dateutil as du


def last_day(start, underlying):
    i = 0
    while True:
        try:
            return dt.datetiume(start.year, start.month, underlying-i)
        except:
            i += 1
    

class Schedule:
    def __init__(self, interval, increment, short_to_next=False, skip_wkend=False, holidays=[]):
        self.interval = interval
        self.increment = increment
        self.short_to_next = short_to_next
        self.skip_wkend = skip_wkend
        self.holidays = holidays

    def nth_term(self, start, count, incr_1=None, underlying=None):
        if count == 0:
            return start.strftime('%d/%m/%Y')
        
        if incr_1:
            if count == 1:
                return incr_1.strftime('%d/%m/%Y')
            else:
                count -= 1
                start = incr_1
        
        """ If shortmonth is first and underlying is greater than start.day,
        use last day of previous month as basis of calculation
        raw will have wrong day but this will be overwritten by underlying rule 
        """
        if underlying == None:
            underlying = start.day
        else:
            if start.day < underlying:
                start = last_day(start + du.relativedelta.relativedelta(month=-1), underlying)
            
            
        delta = count * self.increment
        if self.interval == "week":
            raw = start + du.relatvedelta.relativedelta(weeks =+ delta)
        elif self.interval == "month":
            raw = start + du.relativedelta.relativedelta(months =+ delta)
        else:
            raw = start + du.relativedelta.relativedelta(years =+ delta)
        
        
        if raw.day < underlying:
            if self.short_to_next() == True:
                change = dt.datetime(raw.year, raw.month+1, 1)
                raw = change
            else:
                raw = last_day(raw, underlying)
        
        if self.skip_wkend == True:
            while raw.weekday() > 4 or raw in self.holidays:
                raw += du.relativedelta.relativedelta(days=1)
        elif len(self.holidays) > 0:
            while raw in self.holidays:
                raw += du.relativedelta.relativedelta(days=1)
        
        return raw.strftime('%d/%m/%Y')
        

    def recite(self, start, stop=None, term=None, incr_1=None, underlying=None):
        seq = []
        
        if term:
            for i in range(term + 1):
                seq.append(self.nth_term(start, i, incr_1, underlying))
        
        if stop:
            i = 0
            nxt = self.nth_term(start, i, incr_1, underlying)
            while nxt <= stop:
                seq.append(nxt)
                i += 1
                nxt = self.nth_term(start, i, incr_1, underlying)
        
        return seq
                
    
def test_methods():
    print('1. Create schedule rules')
    
    basis_input = input('\nInput the schedule basis W(eek) / M(onth) / Y(ear) >>> ').upper()
    b_keys = {'W': 'week', 'M': 'month', 'Y': 'year'}
    basis = b_keys[basis_input] 
    
    increment = int(input('Input the schedule increment (i.e., once every [increment] {}(s)) >>> ').format(basis))
    
    wkend_input = input('Should the schedule skip over weekends [Y/N]?').upper()
    y_to_true = {'Y': True, 'N': False}
    skip_wkend = y_to_true[wkend_input]
    
    short_input = input('If a date does not occur in the month, should the schedule move to the first day of next month [Y/N]?').upper()
    short_to_next = y_to_true[short_input]
    
    sched = Schedule(basis, increment, short_to_next=short_to_next, skip_wkend=skip_wkend)
    
    print('\n2. Create a sequence')
    start_input = input('Input start date >>> ')
    day, month, year = start_input.split('/')
    start = dt.datetime(int(year), int(month), int(day))
    
    q = input('Do you want to specify an incr_1 value Y/N?').upper()
    if q == 'Y':
        incr_1_input = input('Input first increment >>> ')
        day, month, year = incr_1_input.split('/')
        incr_1 = dt.datetime(int(year), int(month), int(day))
    else:
        incr_1 = None
    
    q = None
    if basis != 'week':
        q = input('Do you want to specify an underlying date value [Y/N]? >>> ').upper()
    if q == 'Y':
        underlying = int(input('Input the underlying day >>> '))
    else:
        underlying = None
        
    
    q = input('Do you want to specify an end date or a term E/T?').upper()
    if q == 'E':
        stop_input = input('Input end date >>>> ')
        day, month, year =  stop_input.split('/')
        stop = dt.datetime(year, month, day)
        term = None
    else:
        term = int(input('Input the term >>> '))
        stop = None
        

    print(sched.recite(start, stop=stop, term=term, incr_1=incr_1, underlying=underlying))

if __name__ == "__main__":
    test_methods()