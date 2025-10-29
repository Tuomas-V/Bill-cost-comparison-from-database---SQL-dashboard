import pandas as pd
from sqlalchemy import create_engine
import datetime

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D



engine = create_engine("mariadb://user:password@localhost:port/database")

# SQL queries into dataframe
query1 = r"SELECT tositepv, tili, summa FROM laskut;"
query2 = r"SELECT * FROM tilit;"

df1 = pd.read_sql(query1, engine)
df2 = pd.read_sql(query2, engine)

data = df1.merge(df2[['tili', 'tilin_nimi']], on='tili')

# formatting dates to datetime & renaming needed columns to match display language
data['tositepv'] = pd.to_datetime(data['tositepv'], format='%Y-%m-%d')
data.rename(columns={'tositepv':'date', 'summa':'sum', 'tilin_nimi':'account_name'}, inplace=True)

# grouping by bill costs & dates, and selecting electricity & gas and heating bills
spendings = data.groupby(['date', 'account_name'])['sum'].sum()
df = spendings.to_frame()
df = df.reset_index()

electricity = df.loc[(df['account_name'] =='Sähkö ja kaasu')]
heating = df.loc[(df['account_name'] =='Lämmitys')]



# Visualization
#===============

background_color = "#292832"
title_color = "#FFFFFF"
text_color = "#DDDDDD"
box_color = "#313131"

line1_color = "#097CDA"
line2_color = "#D7650D"
cutoff1_color = "#0B9520"
cutoff2_color = "#A708CA"
line_width = 1
cutoff_line_width = 1.5

# automatically corrects for differences in sample size of bills when comparing means
diff1 = diff2 = 1
if electricity.value_counts('sum').sum() > heating.value_counts('sum').sum():
    diff1 = (electricity['sum'].value_counts().sum())/(heating['sum'].value_counts().sum())
elif electricity.value_counts('sum').sum() < heating.value_counts('sum').sum():
    diff2 = (heating['sum'].value_counts().sum())/(electricity['sum'].value_counts().sum())

# sets the cutoff lines to relative mean of bills
line_cutoff1 = int(electricity['sum'].mean()*diff1)
line_cutoff2 = int(heating['sum'].mean()*diff2)

# figure
fig, ax = plt.subplots(figsize=(9,7))
plt.xlim([datetime.date(2024, 1, 1), datetime.date(2024, 12, 31)])
plt.ylim(0, 500000)
fig.subplots_adjust(bottom=0.2)

# plots
plt.plot(electricity['date'], electricity['sum'], color=line1_color, linewidth=line_width, label='Electricity & Gas')
plt.plot(heating['date'], heating['sum'], color=line2_color, linewidth=line_width, label='Heating')

data_year = df['date'].loc[0].year
plt.title('Raahe city electricity & gas bills relative to heating in %i' %data_year, color=title_color, pad=5)

# legends
line_legend = plt.legend(loc="upper left", edgecolor=text_color, facecolor=box_color, labelcolor=text_color)
ax.add_artist(line_legend)

custom_lines = [Line2D([0], [0], color=cutoff1_color, lw=cutoff_line_width, ls='--'),
                Line2D([0], [0], color=cutoff2_color, lw=cutoff_line_width, ls='--')]

cutoff_legend = ax.legend(custom_lines, ['Electricity & Gas: %i€' %line_cutoff1, 'Heating:               %i€' %line_cutoff2], loc='upper right',
          edgecolor=text_color, facecolor=box_color, labelcolor=text_color, title='Average cost relative to bill count')
plt.setp(cutoff_legend.get_title(), color=title_color)

# spines and ticks
ax.spines[['right', 'top']].set_visible(False)
ax.spines[['left', 'right', 'top', 'bottom']].set_color(text_color)

ax.tick_params(axis='y', colors=text_color)
ax.tick_params(axis='x', colors=text_color)
ax.yaxis.set_major_formatter('{x:1.0f}€')

ticks_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ax.set_xticklabels(ticks_labels)

# cutoff lines
ax.hlines(y=line_cutoff1, xmin=0, xmax=210000, zorder=0, ls='--', lw=cutoff_line_width, color=cutoff1_color)
ax.hlines(y=line_cutoff2, xmin=0, xmax=210000, zorder=0, ls='--', lw=cutoff_line_width, color=cutoff2_color)

# background
ax.set_facecolor(background_color)
fig.patch.set_facecolor(background_color)

plt.show()