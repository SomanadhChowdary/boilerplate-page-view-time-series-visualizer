import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',parse_dates=['date'],index_col='date')


# Clean data
df = df[(df['value']>=df['value'].quantile(0.025))&(df['value']<=df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(14,5))
    ax=fig.add_subplot(1,1,1)
    ax.plot(df.index,df['value'],color='red')
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year']=df_bar.index.year
    df_bar['month']=df_bar.index.month_name()
    # Draw bar plot
    months_ordered=[
        'January','February','March','April','May','June','July','August','September','October','November','December'
    ]
    df_bar['month']=pd.Categorical(df_bar['month'],categories=months_ordered,ordered=True)
    df_grouped = df_bar.groupby(['year','month'])['value'].mean().unstack()
    fig = df_grouped.plot(kind='bar',figsize=(14,7)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box['month_num']= df_box['date'].dt.month
    # Draw box plots (using Seaborn)
    df_box=df_box.sort_values('month_num')
    fig , axes = plt.subplots(ncols=2,figsize=(16,6))
    sns.boxplot(x='year',y='value',data=df_box,ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    sns.boxplot(x='month',y='value',data=df_box,ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
