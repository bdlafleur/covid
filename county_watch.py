from math import log
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import SU
import datetime


class County():
    def __init__(self, county, state, style):

        window = 7

        # Store name information.
        self.county = county
        self.state = state
        self.style = style

        # Parse all data and trim for just this county
        self.all_data = pd.read_csv('covid-19-data/us-counties.csv')
        self.data = \
            self.all_data[(self.all_data['county'] == county) &
                          (self.all_data['state'] == state)]
        self.data['new_cases'] = self.data['cases'].diff()

        # Get rolling average columns.
        self.data['roll_new_cases'] = \
            self.data.new_cases.rolling(window=window).mean()
        self.data['roll_cases'] = \
            self.data.cases.rolling(window=window).mean()

        # Get doubling rate.
        ln2 = [log(i, 2) for i in self.data['roll_cases']]
        slope_list = [0]*window
        last = ln2[window-1]
        for ele in ln2[window:]:
            try:
                slope_list.append(1/(ele - last))
                last = ele
            except ZeroDivisionError:
                slope_list.append(0)

        slope_list = np.array(slope_list)
        slope_list[slope_list == 0] = 100
        self.data['doubling_rate'] = slope_list


def plot_time_series(filename, counties):

    fig, ax = plt.subplots(figsize=(14, 5), nrows=1, ncols=3)
    date_fmt = mdates.DateFormatter('%Y-%m-%d')
    locator = mdates.WeekdayLocator(byweekday=SU, interval=1)

    # Plot the time series data.
    for county in counties:
        dates = county.data['date']
        xaxis = \
            [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
        ax[0].plot(xaxis, county.data['cases'], county.style,
                   label=county.county)
        ax[1].loglog(county.data['roll_cases'], county.data['roll_new_cases'],
                     county.style, label=county.county)
        ax[2].plot(xaxis, county.data['doubling_rate'],
                   county.style, label=county.county)

    ax[0].set_xlabel('Date')
    ax[0].set_ylabel('Total Cases')
    ax[0].legend()
    ax[0].xaxis.set_major_formatter(date_fmt)
    ax[0].xaxis.set_major_locator(locator)

    ax[1].set_xlabel('Total Cases')
    ax[1].set_ylabel('New Cases')
    ax[1].legend()

    ax[2].set_xlabel('Date')
    ax[2].set_ylabel('Doubling Rate (doubles every X days)')
    ax[2].set_ylim((0, 14))
    ax[2].xaxis.set_major_locator(locator)
    ax[2].invert_yaxis()
    ax[2].legend()

    fig.autofmt_xdate()
    fig.savefig(f'{filename}')


def main():

    # Plot for regions I care about.
    kent = County('Kent', 'Michigan', 'r-')
    wash = County('Washtenaw', 'Michigan', 'b-')
    wayne = County('Wayne', 'Michigan', 'b--')
    kzoo = County('Kalamazoo', 'Michigan', 'm-')
    plot_time_series('Images/covid_michigan.png', [kent, wash, wayne, kzoo])

    sch = County('Schenectady', 'New York', 'k-')
    alb = County('Albany', 'New York', 'k--')
    plot_time_series('Images/covid_newyork.png', [sch, alb])

    cath = County('Chatham', 'Georgia', 'g-')
    plot_time_series('Images/covid_georgia.png', [cath])

    ess = County('Essex', 'Massachusetts', 'c-')
    bost = County('Suffolk', 'Massachusetts', 'c--')
    plot_time_series('Images/covid_mass.png', [ess, bost])

    dek = County('DeKalb', 'Illinois', 'c-')
    chi = County('Cook', 'Illinois', 'c--')
    plot_time_series('Images/covid_illinois.png', [dek, chi])

    # Plot for New York.
    ny = County('New York City', 'New York', 'k')
    plot_time_series('Images/covid_ny.png', [ny])


if __name__ == '__main__':
    main()
