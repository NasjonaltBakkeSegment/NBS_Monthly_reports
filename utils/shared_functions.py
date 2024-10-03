import pathlib
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import copy
import os
import yaml
import calendar

config_path = os.path.abspath('../config/params.yaml')
with open(config_path, 'r') as file:
    params = yaml.safe_load(file)

logsdir = pathlib.Path('../data')

hubs=['colhub_global', 'scihub', 'cdse', 'esahub_global', 'colhub_AOI']

plt.rcParams["figure.figsize"] = (params['fig_dims']['width'], params['fig_dims']['height'])
plt.rcParams.update({'font.size': params['font_size']['default']})

def plot_stats(df, plot_max=False, plot_BE=True):

    fig, ax = plt.subplots(figsize=(params['fig_dims']['width'], params['fig_dims']['height']))

    plt.plot(df.index, df['scihub'], linestyle='solid', color=params['color1'], label='scihub.copernicus.eu')
    plt.plot(df.index, df['cdse'], linestyle='solid', color=params['color2'], label='dataspace.copernicus.eu')
    plt.plot(df.index, df['colhub_global'], linestyle='solid', color=params['color3'], label='colhub.met.no')
    if not df['esahub_global'].isnull().all() and not (df['esahub_global'] == 0).all():
        plt.plot(df.index, df['esahub_global'], linestyle='solid', color=params['color4'], label='sentinelhub2.met.no')
    if not (df['colhub_AOI'] == 0).all():
        plt.plot(df.index, df['colhub_AOI'], linestyle='solid', color=params['color4'], label='colhub-archive.met.no')

    if plot_max:
        days = [1]
    else:
        days = [1, 10, 20]

    ax.set_ylabel('Number of products per sensing day', fontsize=params['font_size']['axis_labels'])
    ax.tick_params(axis='y', labelsize=params['font_size']['tick_labels'])

    # Set minor ticks for each day
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=7))

    # Determine the duration of the time series
    time_series_duration = df.index[-1] - df.index[0]

    if time_series_duration > pd.Timedelta(90, unit='d'):  # More than 3 months
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    else:  # Less than 3 months
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))

    # Rotate the x-axis tick labels to a 45-degree angle
    for label in ax.get_xticklabels():
        label.set_rotation(70)
        label.set_horizontalalignment('right')
        label.set_fontsize(params['font_size']['tick_labels'])

    plt.tight_layout()
    fig.autofmt_xdate()

    plt.legend(loc="best", fontsize=params['font_size']['legend'])
    plt.grid(True)

    plt.show()

def plot_missing(df, plot_max=False):

    fig = plt.figure(figsize=(params['fig_dims']['width'], params['fig_dims']['height']))

    # Number of missing products
    missing_all = int(sum(df['cdse'] - df['colhub_global']))
    missing_perc_all = ((df['cdse'] - df['colhub_global'])/df['cdse'])

    missing_30 = int(sum((df['cdse'] - df['colhub_global']).iloc[-30]))
    missing_perc_30 = ((df['cdse'] - df['colhub_global'])/df['cdse']).iloc[-30]

    plt.figtext(-0.4,0.3, 'Difference between \nCDSE and colhub \n (last day) \n\n {:d} products missing \n\n ~{:.1%} of the products'.format(missing, missing_perc, 1/3), color=params['color2'])
    plt.legend(loc="best", fontsize=params['font_size']['legend'])
    plt.grid(True)
    plt.show()

def read_dhus_logs(file):
    data = pd.read_csv(file, header=None, names=['day', 'product_type', 'action', 'size', 'number', 'timeliness'], parse_dates=['day'])
    out = {}
    for action_type in ['synchronized', 'deleted', 'fscanner']:
        d = data[data['action'] == action_type].drop('action', axis=1)
        stats_1 = d.groupby(['day']).sum()[['size', 'number']]
        stats_2 = d.groupby(['day']).median(numeric_only=True)['timeliness']
        stats = stats_1.join(stats_2)
        if len(stats) > 0:
            stats = stats.asfreq('1D', fill_value=0)
        out.update({action_type: stats})
    return out

def read_dhus_logs_details(file):
    data = pd.read_csv(file, header=None, names=['day', 'product_type', 'action', 'size', 'number', 'timeliness']\
                        , parse_dates=['day'], index_col=['day'])
    return data

def plot_stats_logs(synchronized, deleted=None, fscanner=None, plot_max=False):

    fig, ax = plt.subplots(figsize=(params['fig_dims']['width'], params['fig_dims']['height']))

    # Plot timeliness on the left y-axis
    l1, = ax.plot(synchronized.index, synchronized['timeliness'], linestyle='solid', color=params['color2'], label='timeliness')
    ax.set_ylim([0, None])
    ax.set_ylabel('Timeliness in hours', color=params['color2'])
    ax.tick_params('y', colors=params['color2'])
    plt.grid(True)

    # Plot number of products on the right y-axis
    ax2 = ax.twinx()
    l2, = ax2.plot(synchronized.index, synchronized['number'], color=params['color1'], label='synchronized')

    lines = [l1, l2]  # Initialize the list of line objects for the legend

    if fscanner is not None:
        l3, = ax2.plot(fscanner.index, fscanner['number'], linestyle='dashed', color=params['color1'], label='fscanned')
        lines.append(l3)

    if deleted is not None:
        l4, = ax2.plot(deleted.index, deleted['number'], color=params['color3'], label='deleted')
        lines.append(l4)

    ax2.set_xlabel('Ingestion date in colhub')
    ax2.set_ylabel('Number of products', color=params['color1'])
    ax2.tick_params('y', colors=params['color1'])

    # Combine legends for both axes
    labels = [line.get_label() for line in lines]
    ax2.legend(lines, labels, loc='best')

    # Time axis formatting
    if plot_max == True:
        days = [1]
    elif plot_max == False:
        days = [1,10,20]
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    #ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=days))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    fig.autofmt_xdate()

    plt.show()

def plot_stats_logs_daily(synchronized, deleted=None, fscanner=None, plot_max=False):

    # Simple stats that will be annotations on the plot
    median = int(synchronized['number'].iloc[0:-2].median())
    last = int(synchronized['number'].iloc[-1])
    t_median = synchronized['timeliness'].iloc[0:-2].median()
    t_last = synchronized['timeliness'].iloc[-1]
    if fscanner is not None:
        fmedian = int(fscanner['number'].iloc[0:-2].median())
        flast = int(fscanner['number'].iloc[-1])
        ft_median = fscanner['timeliness'].iloc[0:-2].median()
        ft_last = fscanner['timeliness'].iloc[-1]

    fig, ax = plt.subplots(figsize=(params['fig_dims']['width'], params['fig_dims']['height']))

    # Plot timeliness on the left y-axis
    l1, = ax.plot(synchronized.index, synchronized['timeliness'], linestyle='solid', color=params['color2'], label='timeliness')
    ax.set_ylim([0, None])
    ax.set_ylabel('Timeliness in hours', color=params['color2'])
    ax.tick_params('y', colors=params['color2'])
    plt.grid(True)

    # Plot number of products on the right y-axis
    ax2 = ax.twinx()
    l2, = ax2.plot(synchronized.index, synchronized['number'], color=params['color1'], label='synchronized')

    # Initialize list for legend handles
    lines = [l1, l2]

    # Add fscanner if present
    if fscanner is not None:
        l3, = ax2.plot(fscanner.index, fscanner['number'], linestyle='dashed', color=params['color1'], label='fscanned')
        lines.append(l3)

    # Add deleted if present
    if deleted is not None:
        l4, = ax2.plot(deleted.index, deleted['number'], color=params['color3'], label='deleted')
        lines.append(l4)

    # Set labels and ticks for right y-axis
    ax2.set_xlabel('Ingestion date in colhub')
    ax2.set_ylabel('Number of products', color=params['color1'])
    ax2.tick_params('y', colors=params['color1'])

    # Create a shared legend
    labels = [line.get_label() for line in lines]
    ax2.legend(lines, labels, loc='best')

    # Time axis formatting
    if plot_max == True:
        days = [1]
    elif plot_max == False:
        days = [1,10,20]
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=days))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    fig.autofmt_xdate()

    plt.show()

def plot_stats_simple(df, plot_max=False):

    fig, ax = plt.subplots(figsize=(params['fig_dims']['width'], params['fig_dims']['height']))

    # Plot nb of products
    plt.plot(df.index, df['nb_products'], linestyle='solid', color=params['color1'])
    ax.set_ylim([0, None])
    ax.set_ylabel('Number of products', color=params['color1'])
    ax.tick_params('y', colors=params['color1'])

    # Time axis formatting
    if plot_max == True:
        days = [1]
    elif plot_max == False:
        days = [1,10,20]
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=days))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    fig.autofmt_xdate()
    plt.grid(True)
    plt.show()

def get_year_and_month():
    config_path = os.path.abspath('../config/report_month.yaml')
    with open(config_path, 'r') as file:
        date = yaml.safe_load(file)
    year = int(date['year'])
    month = int(date['month'])
    return year, month

def get_month_name(month):
    if 1 <= month <= 12:
        return calendar.month_name[month]
    else:
        return "Invalid month number"
