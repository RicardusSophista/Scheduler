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
    def __init__(self, interval, increment, shortmonth="last", weekends="Keep", holidays=[]):
        self.interval = interval
        self.increment = increment
        self.shortmonth = shortmonth
        self.weekends = weekends
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
            if self.shortmonth == "first":
                change = dt.datetime(raw.year, raw.month+1, 1)
                raw = change
            else:
                raw = last_day(raw, underlying)
        
        if self.weekends == "Skip":
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
                
    
    
sched = Schedule("month",1,weekends='Skip')
start_input = input('Input start date >>> ')
day, month, year = start_input.split('/')
start = dt.datetime(int(year), int(month), int(day))
incr_1_input = input('Input first increment >>> ')
day, month, year = incr_1_input.split('/')
incr_1 = dt.datetime(int(year), int(month), int(day))

term = int(input('Input term >>> '))

print(sched.recite(start, term=term, incr_1=incr_1))