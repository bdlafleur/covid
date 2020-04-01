import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime


class County():
    def __init__(self, county, state, style):

        # Store name information.
        self.county = county
        self.state = state
        self.style = style

        # Parse all data and trim for just this county
        self.all_data = pd.read_csv('covid-19-data/us-counties.csv')
        self.data = \
            self.all_data[(self.all_data['county']==county) & \
                          (self.all_data['state']==state)]
        self.data['new_cases'] = self.data['cases'].diff()

        # Get rolling average columns.
        self.data['roll_new_cases'] = \
            self.data.new_cases.rolling(window=5).mean()
        self.data['roll_cases'] = \
            self.data.cases.rolling(window=5).mean()


def plot_time_series(filename, counties):

    fig, ax = plt.subplots(figsize=(10, 5), nrows=1, ncols=2)
    date_fmt = mdates.DateFormatter('%Y-%m-%d')
    locator= mdates.MonthLocator()

    # Plot the time series data.
    for county in counties:
        dates = county.data['date']
        xaxis = \
            [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
        ax[0].plot(xaxis, county.data['cases'], county.style,
                   label=county.county)
        ax[1].loglog(county.data['roll_cases'], county.data['roll_new_cases'],
                county.style, label=county.county)
    ax[0].set_xlabel('Date')
    ax[0].set_ylabel('Total Cases')
    ax[0].legend()
    ax[0].xaxis.set_major_formatter(date_fmt)
    ax[0].xaxis.set_major_locator(locator)

    ax[1].set_xlabel('Total Cases')
    ax[1].set_ylabel('New Cases')
    ax[1].legend()

    fig.autofmt_xdate()
    fig.savefig(f'{filename}')


def main():

    # Plot for regions I care about.
    kent = County('Kent', 'Michigan', 'r-')
    wash = County('Washtenaw', 'Michigan', 'b-')
    wayne = County('Wayne', 'Michigan', 'b--')
    kzoo = County('Kalamazoo', 'Michigan', 'm-')
    plot_time_series('Images/covid_michigan.png', [kent, wash, wayne])

    sch = County('Schenectady', 'New York', 'k-')
    alb = County('Albany', 'New York', 'k--')
    plot_time_series('Images/covid_newyork.png', [sch, alb])

    cath = County('Chatham', 'Georgia', 'g-')
    plot_time_series('Images/covid_georgia.png', [cath])

    ess = County('Essex', 'Massachusetts', 'c-')
    bost = County('Suffolk', 'Massachusetts', 'c--')
    plot_time_series('Images/covid_mass.png', [ess, bost])

    # Plot for New York.
    ny = County('New York City', 'New York', 'k')
    plot_time_series('Images/covid_ny.png', [ny])


if __name__ == '__main__':
    main()
