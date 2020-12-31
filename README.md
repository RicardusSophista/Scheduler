# Scheduler

An extension to the Python `dateutil` module to allow a regular sequence of dates to be generated with control over the treatment of short months, weekends, and holidays.

## Background

Payment schedules that are set up to repay on the 31st of the month are the bane of my life. Excel doesn't like them. `dateutil` does almost everything you could ever want with a date, but its `rrule` function is explicitly set up to skip over impossible dates. 

If you have a choice, please don't set up monthly schedules with a date later than the 28th. If you don't have a choice, then use `scheduler`. 

## Components

The `Schedule` object is a set of rules for setting up a schedule. It has two methods `nth_term` and `recite` for generating sequences based on those rules.

The `Schedule` object has the following attributes:
* `interval`: The basic unit of time that defines the schedule. Can be either 'week', 'month', or 'year'.
* `increment`: The number of `increment`s between each date. So if `interval` is 'week' and `increment` is '2', this is a fortnightly schedule.
* `short_to_next`: Determines what should happen to dates that aren't present in the month, e.g. 31st June. By default, this is set to `False`, meaning the schedule will jump back to the last day of the month, e.g. 30th June. If this is set to `True`, the schedule will jump to the first day of the *next* month, e.g. 1st July. 
* `skip_wkend`: If set to `True`, if a date in the sequence is a weekend, the sequence will jump to the next working day. Set to `False` by default.
* `holidays`: A list of `datetime` objects representing holidays to skip. By default this is empty. If you provide such a list, then any date in the sequence that falls within the holidays list will be moved to the next available day. 

The `nth_term` method will generate the nth iteration of the Schedule, given a start date. It has the following parameters:
* `start`: A `datetime` object representing the first date in the sequence (n=0).
* `count`: The value of n. 0 will return the start date.
* `incr_1`: Optional: this allows you to specify the first term if the zeroth term is for some reason irregular. This could happen for example:
  * A loan with monthly repayments starts with a 3-month repayment holiday: the zeroth term (representing the drawdown) could be 1st January, the first term (for the first payment) would be 1st April, and then subsequent terms would be 1st May, 1st June, etc;
  * A subscription is due annually at the end of the year, but subscribers who join halfway through the year are charged a pro-rata amount for the part-year. So the zeroth term (for the date when they joined) could be 1st July 2020, then the next term would be 31st December 2020, then 31st December 2021, etc
  Note that if `incr_1` is specified, it becomes the basis for every subsequent term - if `incr_1` is the 16th of the month in a monthly schedule, every subsequent date will be on the 16th (unless moved by weekend or holiday rules)
* `underlying`: Optional: This can be used if your `start` date (or `incr_1` date if you specified one) has been moved from its expected value due to a weekend, holiday, or short month. For example:
  * If you want to capture the last day of every month but your start date is 30th June, you would specify 31 as the underlying value. 
  * If your start date is 07/12/2020, but this has been moved from the 5th because the 5th was a Saturday, then you would specify 07/12/2020 as your start date with an `underlying` of '5'.
  * If your start date is 1st March because it has been bumped from the 30th February, you can specify 1st March as your start date and '30' as your `underlying`. Assuming a monthly sequence, n=0 will be 1st March and n=1 will be 30th March. Note: please do not set up sequences like this without a very good reason.

The `recite` method generates a list of dates based on similar parameters to `nth_term`. In effect, it simply applies `nth_term` with increasing values of `count` until a given endpoint. Its parameters are:
* `start`: A `datetime` object, as for `nth_term`
* `stop`: A `datetime` object - either this or `term` should be specified. `recite` will list all dates in the sequence from the `start` date up until the last date that is less than or equal to `stop`. (If `stop` is not itself a date in the sequence, the last date in the sequence will be the last date before `stop`.)
* `term`: An integer that can be used instead of `stop`: specifies how many dates after the start date should be included in the sequence - e.g. if `term` is '12', `recite` will return the start date plus the next 12 dates in the sequence.
* `incr_1` and `underlying`: Have the same purpose as in the `nth_term` method. 

## Dependencies

Requires `datetime` and `dateutil` modules.

## Copyright and licensing

Please, do what you like with it. (Legally, of course.)