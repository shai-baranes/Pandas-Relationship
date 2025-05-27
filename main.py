#https://www.kaggle.com/code/robikscube/introduction-to-exploratory-data-analysis
# YT link: https://www.youtube.com/watch?v=xi0vhXFPegw&t=20s


# Function signature to check on agrs and  defaults
import inspect
import seaborn as sns
inspect.signature(sns.scatterplot)
# <Signature (data=None, *, x=None, y=None, hue=None, size=None, style=None, palette=None, hue_order=None, hue_norm=None, sizes=None, size_order=None, size_norm=None, markers=True, style_order=None, legend='auto', ax=None, **kwargs)>
# also doable by: sns.scatterplot.__text_signature__




inspect.signature(sns.pairplot)
# <Signature (data, *, hue=None, hue_order=None, palette=None, vars=None, x_vars=None, y_vars=None, kind='scatter', diag_kind='auto', markers=None, height=2.5, aspect=1, corner=False, dropna=False, plot_kws=None, diag_kws=None, grid_kws=None, size=None)>

inspect.signature(sns.heatmap)
# <Signature (data, *, vmin=None, vmax=None, cmap=None, center=None, robust=False, annot=None, fmt='.2g', annot_kws=None, linewidths=0, linecolor='white', cbar=True, cbar_kws=None, cbar_ax=None, square=False, xticklabels='auto', yticklabels='auto', mask=None, ax=None, **kwargs)>




import pandas as pd  # noqa: E402
import numpy as np  # noqa: E402
import matplotlib.pylab as plt  # noqa: E402
import seaborn as sns  # noqa: E402
plt.style.use('ggplot')
# pd.set_option('display.max_columns', 200)
# pd.set_option('display.max_rows', 0)
# import warnings
# warnings.filterwarnings('ignore')

df = pd.read_csv(r'input/coaster_db.csv')

# pd.to_datetime(df['Opening date']) # non-consistent format! sometimes years only and sometimes 'Easter 2022' etc...



# data cleaning and filtering: (header)
# same as: df.drop([columns_list], axis=1)
df = df[['coaster_name',
       # 'Length', 'Speed', 
       'Location', 'Status', 
       # 'Opening date', # 'Type',
        'Manufacturer',
       # 'Height restriction', 'Model', 'Height',
       # 'Inversions', 'Lift/launch system', 'Cost', 'Trains', 'Park section',
       # 'Duration', 'Capacity', 'G-force', 'Designer', 'Max vertical angle',
       # 'Drop', 'Soft opening date', 'Fast Lane available', 'Replaced',
       # 'Track layout', 'Fastrack available', 'Soft opening date.1',
       # 'Closing date', 
       'Opened',
       # 'Replaced by', 'Website',
       # 'Flash Pass Available', 'Must transfer from wheelchair', 'Theme',
       # 'Single rider line available', 'Restraint Style',
       # 'Flash Pass available', 'Acceleration', 'Restraints', 'Name',
       'year_introduced', 'latitude', 'longitude', 'Type_Main',
       'opening_date_clean',
       # 'speed1', 'speed2', 'speed1_value', 'speed1_unit',
       'speed_mph', 
       # 'height_value', 'height_unit', 
       'height_ft', 'Inversions_clean', 'Gforce_clean']]
       # 'height_ft', 'Inversions_clean', 'Gforce_clean']].copy() # in vid, he added the copy command to avoid linked/referenced df to old one


df.dtypes
# coaster_name           object
# Location               object
# Status                 object
# Manufacturer           object
# Opened                 object
# year_introduced         int64
# latitude              float64
# longitude             float64
# Type_Main              object
# opening_date_clean     object
# speed_mph             float64
# height_ft             float64
# Inversions_clean        int64
# Gforce_clean          float64


df['opening_date_clean'] = pd.to_datetime(df['opening_date_clean']) # results w/ dtype: datetime64[ns]
df['year_introduced'] = pd.to_numeric(df['year_introduced']) # somthing doable in case the field was not numeric (e.g. string)


df.columns
# Index(['coaster_name', 'Location', 'Status', 'Manufacturer', 'Opened',
#        'year_introduced', 'latitude', 'longitude', 'Type_Main',
#        'opening_date_clean', 'speed_mph', 'height_ft', 'Inversions_clean',
#        'Gforce_clean'],
#       dtype='object')


# rename our columns  (TBD check the other way as was done so far)
# provide dictionary with older as key and newer as value

df.rename(columns = {'coaster_name': 'Coaster_Name',
                     'year_introduced': 'Year_Introduced',
                     'opening_date_clean': 'Opening_Date',
                     'speed_mph': 'Speed_mph',
                     'height_ft': 'Height_ft',
                     'Inversions_clean': 'Inversions',
                     'Gforce_clean': 'Gforce'}, inplace=True)



# equivalent commands:
df.isna().sum() # sum (count) of NaN values per column
df.isnull().sum()
# Coaster_Name          0
# Location              0
# Status              213
# Manufacturer         59
# Opened             1060
# Year_Introduced       0
# latitude            275
# longitude           275
# Type_Main             0
# Opening_Date        250
# Speed_mph           150
# Height_ft           916
# Inversions            0
# Gforce              725
# dtype: int64

df.duplicated().sum() # no duplicates
# 0

  


# equivalent commands:
# finding all rows that have 'Coaster_Name' that is duplicated
df.loc[df.duplicated(subset=['Coaster_Name'])] # author
df[df.duplicated(['Coaster_Name'])] # mine


# equivalent commands:
df.query('Coaster_Name == "Crystal Beach Cyclone"') # author
df[df['Coaster_Name'] == "Crystal Beach Cyclone"] # mine
#              Coaster_Name            Location  ... Inversions Gforce
# 39  Crystal Beach Cyclone  Crystal Beach Park  ...          0    4.0
# 43  Crystal Beach Cyclone  Crystal Beach Park  ...          0    4.0

# [2 rows x 14 columns]


# one was mistaken on the year introduced
df[df['Coaster_Name'] == "Crystal Beach Cyclone"]['Year_Introduced']
df[df['Coaster_Name'] == "Crystal Beach Cyclone"].Year_Introduced
# 39    1926
# 43    1927



# disposing on duplicates

# the subset that is not (~) duplicated on the set of columns (we also have to reset the index since some rows are lost)
df = df[~df.duplicated(['Coaster_Name', 'Location', 'Opening_Date'])].reset_index(drop=True) # Mine
# df = df[~df.duplicated(subset=['Coaster_Name', 'Location', 'Opening_Date'])].reset_index(drop=True) #Author (the drop is to avoid double index columns)



df['Year_Introduced'].value_counts() # counting the unique values

# 1999    46
# 2000    45
# 1998    30
# 2001    29
# 2002    28
#         ..
# 1956     1
# 1959     1
# 1961     1
# 1895     1
# 1884     1


# -----------start plot------------------------
ax = df['Year_Introduced'].value_counts().head(10).plot(kind='bar', title='Top Years Coasters Introduced') 

ax.set_xlabel('Year Introduced')
ax.set_ylabel('Count')
plt.show()  # Figure_1.png
# ------------end plot--------------------------


# TBD combine plots in a single frame

# -----------start plot------------------------
df['Speed_mph'].plot(kind='hist', bins=20, title='Coaster Speed (mph)')
plt.show()  # Figure_2.png
# ------------end plot--------------------------



# -----------start plot------------------------
df['Speed_mph'].plot(kind='kde', title='Coaster Speed (mph)')
plt.show()  # Figure_3.png
# ------------end plot--------------------------



# -----------start plot------------------------
df.plot(kind='scatter', x='Speed_mph', y='Height_ft', title='Coaster Speed vs. Height')
plt.show()  # Figure_4.png
# ------------end plot--------------------------




# -----------start plot------------------------
sns.scatterplot(y='Speed_mph', x='Year_Introduced', data=df) # TBD PNG
# OR sns.scatterplot(x='Speed_mph', y='Height_ft', data=df, hue='Year_Introduced') # TBD PNG
plt.show()  # Figure_5.png / Figure_5_hue.png
# ------------end plot--------------------------





# -----------start plot------------------------
# feature relationship (correlation), ability to compare multiple features against each-other (vars: for multiples variables)
sns.pairplot(df, vars=['Year_Introduced', 'Speed_mph', 'Height_ft', 'Inversions', 'Gforce'], hue='Type_Main') # it might take some time (hue = type of material)
plt.show() # Figure_6.png, to see all potential correlation by charts (TBD add the corr table as well)
# ------------end plot--------------------------




numeric_columns = df.select_dtypes(include='number') # correlation table works only on the numeric valeus
numeric_columns.corr()

#                  Year_Introduced  latitude  ...  Inversions    Gforce
# Year_Introduced         1.000000 -0.069354  ...    0.233701 -0.073403
# latitude               -0.069354  1.000000  ...   -0.000506  0.055499
# longitude               0.178767 -0.297532  ...    0.080824  0.017657
# Speed_mph               0.225991 -0.056193  ...    0.246593  0.503828
# Height_ft               0.249487  0.020147  ...    0.138286  0.480465
# Inversions              0.233701 -0.000506  ...    1.000000  0.339137
# Gforce                 -0.073403  0.055499  ...    0.339137  1.000000



numeric_columns = df.drop(['latitude', 'longitude'], axis=1).select_dtypes(include='number')
df_corr = numeric_columns.corr()

#                  Year_Introduced  Speed_mph  Height_ft  Inversions    Gforce
# Year_Introduced         1.000000   0.225991   0.249487    0.233701 -0.073403
# Speed_mph               0.225991   1.000000   0.823216    0.246593  0.503828
# Height_ft               0.249487   0.823216   1.000000    0.138286  0.480465
# Inversions              0.233701   0.246593   0.138286    1.000000  0.339137
# Gforce                 -0.073403   0.503828   0.480465    0.339137  1.000000



# -----------start plot------------------------
sns.heatmap(df_corr, annot=True)
plt.show() # # Figure_7.png
# ------------end plot--------------------------




# Question: What are the locations with the fastest rollercoasters (minimum of 10)? 
# group by locations

df.value_counts('Location') # we se that we have 'Other', so we'd like to ignore it
# Location
# Other                            181
# Kings Island                      19
# Cedar Point                       18
# Six Flags Magic Mountain          17
# Hersheypark                       16
#                                 ... 
# Nürburgring                        1
# OCT East                           1
# Family Kingdom Amusement Park      1
# Expoland                           1
# Đại Nam Văn Hiến                   1





# df.groupby('Location')['Speed_mph'].mean().dropna()



# equivalents:
df.query('Location != "Other"').groupby('Location')['Speed_mph'].mean().dropna()
df[df.Location != "Other"].groupby('Location')['Speed_mph'].mean().dropna()




       # .groupby('Location')['Speed_mph'].mean()
ax = df.query('Location != "Other"')    \
       .groupby('Location')['Speed_mph'].agg(['mean', 'count']) \
       .query('count >= 10')    \
       .sort_values('mean', ascending=True)['mean'] \
       .plot(kind='barh', figsize=(12,5), title='Average Coast Speed by Location')  \


ax.set_xlabel('Average Acoaster Speed')
plt.show()  # Figure_8.png

 