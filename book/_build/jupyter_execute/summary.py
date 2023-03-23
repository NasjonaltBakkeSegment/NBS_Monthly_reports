#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime
from IPython.display import Markdown as md
from IPython.display import display_markdown

todays_date = str(datetime.now().date())
month = datetime.now().strftime("%B")
year = str(datetime.now().year)

display_markdown('''# NBS mothly report for {month} {year}''')
md("# NBS mothly report for {} {}".format(month, year))


# # Quick summary
# 
# The table below shows a short overview of the NBS preformance operation during the last 30 days. The three different FEs and the BE are included. All columns represents the number of products in each portal excepting the last 3 columns. Those 3 columns represents the data flow from MET Norway to users through the portals where Volumes are measured in Tb. 
# 

# In[2]:


import pathlib
import datetime as dt
import pandas as pd
import copy
from myst_nb import glue

logsdir = pathlib.Path('../data')
hubs=['colhub_global', 'scihub', 'esahub_global', 'colhub_AOI']
products=['S1', 'S2L1C', 'S2L2A', 'S3', 'S5p']

data_FE = None
for h in hubs:
    csvfile = logsdir / f'products_in_{h}.csv'
    data_tmp = pd.read_csv(csvfile, header=None, names=['product', 'area', 'sensing_date', f'{h}'], parse_dates=['sensing_date'])
    # If several sensing date exist, keep the most recent one
    data_clean = copy.deepcopy(data_tmp.drop_duplicates(subset=['sensing_date', 'product', 'area'], keep='last'))
    if h == 'colhub_AOI':
        data_clean['area'] = 'colhub_aoi'
    if data_FE is None:
        data_FE = data_clean
    else:
        data_FE = data_FE.merge(data_clean, on=['sensing_date', 'product', 'area'], how='outer')
        
data_BE = None
areas = ['AOI']
for a in areas:
    for p in products:
        csvfile = logsdir / f'products_in_BE_{p}_{a}.csv'
        data_tmp = pd.read_csv(csvfile, header=None, names=['product', 'area', 'sensing_date', 'BE'], parse_dates=['sensing_date'])
        # If several sensing date exist, keep the most recent one
        data_clean = copy.deepcopy(data_tmp.drop_duplicates(subset=['sensing_date', 'product', 'area'], keep='last'))
        if a == 'AOI':
            data_clean['area'] = 'colhub_aoi'
        if data_BE is None:
            data_BE = data_clean
        else:
            data_BE = data_BE.append(data_clean)
            
data = data_FE.merge(data_BE, on=['sensing_date', 'product', 'area'], how='outer')
data.set_index('sensing_date', inplace=True)
data.sort_index(inplace=True)
data.fillna(0, inplace=True)

mask_s1 = (data['product'] == 'S1') & (data['area'] == 'colhub_aoi')
data_s1 = data.loc[mask_s1][-30:][['colhub_global', 'scihub', 'colhub_AOI', 'BE']].copy()
col_s1 = data_s1['colhub_global'].sum()
arc_s1 = data_s1['colhub_AOI'].sum()
sci_s1 = data_s1['scihub'].sum()
be_s1 = data_s1['BE'].sum()

mask_s2l1 = (data['product'] == 'S2L1C') & (data['area'] == 'colhub_aoi')
data_s2l1 = data.loc[mask_s2l1][-30:][['colhub_global', 'scihub', 'colhub_AOI', 'BE']].copy()
col_s2l1 = data_s2l1['colhub_global'].sum()
arc_s2l1 = data_s2l1['colhub_AOI'].sum()
sci_s2l1 = data_s2l1['scihub'].sum()
be_s2l1 = data_s2l1['BE'].sum()

mask_s2l2 = (data['product'] == 'S2L2A') & (data['area'] == 'colhub_aoi')
data_s2l2 = data.loc[mask_s2l2][-30:][['colhub_global', 'scihub', 'colhub_AOI', 'BE']].copy()
col_s2l2 = data_s2l2['colhub_global'].sum()
arc_s2l2 = data_s2l2['colhub_AOI'].sum()
sci_s2l2 = data_s2l2['scihub'].sum()
be_s2l2 = data_s2l2['BE'].sum()

mask_s3 = (data['product'] == 'S3') & (data['area'] == 'colhub_aoi')
data_s3 = data.loc[mask_s3][-30:][['colhub_global', 'scihub', 'colhub_AOI', 'BE']].copy()
col_s3 = data_s3['colhub_global'].sum()
arc_s3 = data_s3['colhub_AOI'].sum()
sci_s3 = data_s3['scihub'].sum()
be_s3 = data_s3['BE'].sum()

mask_s5 = (data['product'] == 'S5p') & (data['area'] == 'colhub_aoi')
data_s5 = data.loc[mask_s5][-30:][['colhub_global', 'scihub', 'colhub_AOI', 'BE']].copy()
col_s5 = data_s5['colhub_global'].sum()
arc_s5 = data_s5['colhub_AOI'].sum()
sci_s5 = data_s5['scihub'].sum()
be_s5 = data_s5['BE'].sum()


# In[3]:


def get_product_type(product):
    if product[0:2] == 'S1':
        type = product.split('_')[2]
    elif product[0:2] == 'S2':
        type = product.split('_')[1]
        if not type.startswith('M'):
            type = 'Unknown'
    elif product[0:2] == 'S3':
        tmp = product.split('_')
        if tmp[1] == 'SL':
            type = 'SLSTR_L' + tmp[2]
        elif tmp[1] == 'SR':
            type = 'SRAL_L' + tmp[2]
        elif tmp[1] == 'OL':
            type = 'OLCI_L' + tmp[2]
        else:
            type = 'Unknown'
    else:
        type = 'Unknown'
    if 'DTERRENG' in product:
        type = type + '_DTERRENG'
    return type

def get_data(file):
    data = pd.read_csv(file, header=None, names=['download_time', 'user', 'product', 'size', 'download_duration']                        , parse_dates=['download_time'], index_col='download_time')
    data['satellite'] = data['product'].apply(lambda x: x[0:2])
    data['product_type'] = data['product'].apply(get_product_type)
    return data[data['product_type'] != 'Unknown']

csvfile = logsdir / 'NBS_frontend-global_outputs.csv'
nbs_global = get_data(csvfile)
#nbs_global.set_index('download_time', inplace=True)
nbs_global.sort_index(inplace=True)
nbs_global.fillna(0, inplace=True)
nbs_30 = nbs_global.loc[nbs_global.index >= dt.datetime.today() - dt.timedelta(days=30)].copy()

col_use = len(nbs_30['user'].unique())
col_nb = nbs_30.count()['product_type']
col_vol = nbs_30.sum()['size']/1024/1024/1024/1024 #in Tb


csvfile = logsdir / 'NBS_frontend-AOI_outputs.csv'
nbs_AOI = get_data(csvfile)
#nbs_AOI.set_index('download_time', inplace=True)
nbs_AOI.sort_index(inplace=True)
nbs_AOI.fillna(0, inplace=True)
aoi_30 = nbs_AOI.loc[nbs_AOI.index >= dt.datetime.today() - dt.timedelta(days=30)].copy()

arc_use = len(aoi_30['user'].unique())
arc_nb = aoi_30.count()['product_type']
arc_vol = aoi_30.sum()['size']/1024/1024/1024/1024 #in Tb


# In[4]:


def read_dhus_logs_details(file):
    data = pd.read_csv(file, header=None, names=['day', 'product_type', 'action', 'volume', 'number', 'timeliness']                        , parse_dates=['day'], index_col=['day'])
    return data

def read_csv(file):
    data_tmp = pd.read_csv(file, header=None, names=['product_type', 'day', 'number', 'volume'], parse_dates=['day'], sep=';')
    # If several sensing date exist, keep the numbers only for the most recent script run (ie highest day index)
    data_clean = copy.deepcopy(data_tmp.drop_duplicates(subset=['product_type', 'day'], keep='last')).set_index('day').sort_index()
    data_clean['volume'] = data_clean['volume']/1024./1024
    return data_clean

data_s1 = read_dhus_logs_details(logsdir / 'S1-backend-AOI_inputs.csv')
data_s2l1c = read_dhus_logs_details(logsdir / 'S2L1C-backend-AOI_inputs.csv')
data_s2l2a = read_dhus_logs_details(logsdir / 'S2L2A-backend-AOI_inputs.csv')
data_s3 = read_dhus_logs_details(logsdir / 'S3-backend-AOI_inputs.csv')
data_s5 = read_dhus_logs_details(logsdir / 'S5p-backend-AOI_inputs.csv')
all_colhub = data_s1.append(data_s2l1c).append(data_s2l2a).append(data_s3).append(data_s5)

csvfile = pathlib.Path('../data/nb_products_volume_per_sensing_date.csv')
all_netcdf = read_csv(csvfile)

alle = pd.concat([all_colhub, all_netcdf])

all_vol_be = alle['volume'].sum()/1024 #in Tb

lately = alle[alle.index >= dt.datetime.today() - dt.timedelta(days=30)]
vol_be = lately['volume'].sum()/1024 #in Tb
nb_be = be_s1 + be_s2l1 + be_s2l2 + be_s3 + be_s5


# In[5]:


glue("col_s1", col_s1)
glue("col_s2l1", col_s2l1)
glue("col_s2l2", col_s2l2)
glue("col_s3", col_s3)
glue("col_s5", col_s5)
glue("arc_s1", arc_s1)
glue("arc_s2l1", arc_s2l1)
glue("arc_s2l2", arc_s2l2)
glue("arc_s3", arc_s3)
glue("arc_s5", arc_s5)
glue("sci_s1", sci_s1)
glue("sci_s2l1", sci_s2l1)
glue("sci_s2l2", sci_s2l2)
glue("sci_s3", sci_s3)
glue("sci_s5", sci_s5)
glue("be_s1", be_s1)
glue("be_s2l1", be_s2l1)
glue("be_s2l2", be_s2l2)
glue("be_s3", be_s3)
glue("be_s5", be_s5)
glue("col_use", col_use)
glue("col_nb", col_nb)
glue("col_vol", col_vol)
glue("arc_use", arc_use)
glue("arc_nb", arc_nb)
glue("arc_vol", arc_vol)
glue("nb_be", nb_be)
glue("vol_be", vol_be)


# | Portals | S1 | S2L1C | S2L2A | S3 | S5p | Nb of users | Nb of products | Volume |
# |:---------:|:---------:|:--------:|:---------:|:----------:|:----------:|:-------------:|:---------:|:----------:|
# | colhub.met.no | {glue:text}`col_s1:.0f` | {glue:text}`col_s2l1:.0f` | {glue:text}`col_s2l2:.0f` | {glue:text}`col_s3:.0f` | {glue:text}`col_s5:.0f` | {glue:text}`col_use` | {glue:text}`col_nb` | {glue:text}`col_vol:.3f` |
# | colhub-archive.met.no | {glue:text}`arc_s1:.0f` | {glue:text}`arc_s2l1:.0f` | {glue:text}`arc_s2l2:.0f` | {glue:text}`arc_s3:.0f` | {glue:text}`arc_s5:.0f` | {glue:text}`arc_use` | {glue:text}`arc_nb` | {glue:text}`arc_vol:.3f` |
# | scihub.copernicus.eu | {glue:text}`sci_s1:.0f` | {glue:text}`sci_s2l1:.0f` | {glue:text}`sci_s2l2:.0f` | {glue:text}`sci_s3:.0f` | {glue:text}`sci_s5:.0f` | - | - | - |
# | MET Norway BE | {glue:text}`be_s1:.0f` | {glue:text}`be_s2l1:.0f` | {glue:text}`be_s2l2:.0f` | {glue:text}`be_s3:.0f` | {glue:text}`be_s5:.0f` | - | - | - |
# 

# In[6]:


md("Finally, the total amount of disk space dedicated to the NBS project, including either products in SAFE and NetCDF formats, represents {} Tb.".format(int(all_vol_be)))


# In[7]:


# Monthly volumes (in Tb)
lately = alle[alle.index >= dt.datetime.today() - dt.timedelta(days=365)]
year = (lately['volume'].sum()/1024.)
after_year = year + all_vol_be
short = lately[lately.index <= dt.datetime.today() - dt.timedelta(days=123)]
m6 = (short['volume'].sum()/1024.)
after_6m = m6 + all_vol_be


# In[8]:


md("Due to tracking the data ingested and produced for the NBS project in the last year it is possible to forcast the upcoming need for disk space. As long as data flows follows the same pattern than last year, in 6 months the total disk space will grow until {} Tb; while in 12 months it is forecasted to become {} Tb.".format(int(after_6m), int(after_year)))

