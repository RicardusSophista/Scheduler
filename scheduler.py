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

class Schedule:
    def __init__(self, interval, increment, shortmonth="last", monthend="No",weekends="Keep",holidays=None):
        self.interval = interval
        self.imcrement = increment
        self.shortmonth = shortmonth
        self.monthend = monthend
        self.weekends = weekends
        self.holidays = holidays
        