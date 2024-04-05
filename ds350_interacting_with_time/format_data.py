
# %%
import polars as pl
import pandas as pd
import yfinance as yf
import lets_plot as lp

# %%


# %%
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

response = requests.get(url, verify=False)
html_content = response.content

table = pd.read_html(html_content)[0]

# Extract tickers
tickers_500 = table["Symbol"].tolist()

#print(tickers_500)

# %%


# %%

all_data = pd.DataFrame()

# Iterate through each ticker
for ticker in tickers_500:
    # Retrieve historical data for the ticker
    data = yf.download(ticker, period="5y", interval="1d")
    
    # Add a column for ticker symbol
    data['Ticker'] = ticker
    
    # Concatenate the data for each ticker
    all_data = pd.concat([all_data, data])

# Reset index
all_data = all_data.reset_index()
#print(all_data)

#%%



# %%

all_data_pl = pl.from_pandas(all_data) \
    .melt(id_vars="Date") \
    .with_columns(
        pl.col("variable").str.replace_many(["'", "(", ")"], "").str.split_exact(",", 1).alias("variable")) \
    .unnest("variable") \
    .rename({"Date": "date"}) \
    .pivot(
        values="value",
        index=["date", "field_1"],
        columns="field_0",
        aggregate_function="first") \
    .rename({"field_1": "ticker"})

# Convert back to pandas DataFrame if needed
#all_data_pl_df = all_data_pl.to_pandas()

# Print or further process the transformed DataFrame
#print(all_data_pl_df)

# %%


#EXTRACT NECESSARY COLUMNS AND CREATE VISUAL
# %%
import pandas as pd
from lets_plot import ggplot, aes, geom_line, ggtitle, xlab, ylab, scale_x_datetime, scale_color_discrete, LetsPlot

# Data Preparation
# Extract necessary columns: Date and Close price
stockdata = all_data[['Date', 'Close', 'Ticker']].copy()  # Make a copy to avoid SettingWithCopyWarning
stockdata['Date'] = pd.to_datetime(stockdata['Date'])

# Setup lets-plot to output HTML
LetsPlot.setup_html()

# Interactive Visualization with lets-plot
ggplot(stockdata, aes(x='Date', y='Close', color='Ticker')) + \
    geom_line(size=1) + \
    ggtitle("Stock Performances Over the Last 5 Years") + \
    xlab("Date") + \
    ylab("Close Price") + \
    scale_x_datetime(labels=["%b %Y"]) + \
    scale_color_discrete(name="Ticker")
# %%



# %%
price_plot = ggplot(all_data_pl) + \
    geom_line(aes(x='date', y='Close', color='ticker'), size=1) + \
    ggtitle("Stock Prices Over Time") + \
    xlab("Date") + \
    ylab("Close Price") + \
    scale_x_datetime(labels="%b %Y") + \
    scale_color_discrete(name="Ticker")

volume_plot = ggplot(all_data_pl) + \
    geom_bar(aes(x='date', y='Volume', fill='ticker'), stat='identity') + \
    ggtitle("Trading Volume Over Time") + \
    xlab("Date") + \
    ylab("Volume") + \
    scale_x_datetime(labels="%b %Y") + \
    scale_fill_manual(values=['blue'])  # Change color if necessary

# Combine both plots
combined_plot = price_plot + volume_plot

print(combined_plot)

# %%


#EXAMPLES PROVIDED
# %%
# example for one ticker
msft = yf.Ticker("MSFT")
msft.history(period="2y", interval="1h")

# %%
dat = yf.download(tickers_use, period="5y", interval="1d").reset_index()


# %%

#EXAMPLE PROVIDED
pl.from_pandas(dat) \
    .melt(id_vars="('Date','')") \
    .with_columns(
        pl.col("variable").str.replace_many(["'", "(", ")"], "").str.split_exact(",", 1).alias("variable")) \
    .unnest("variable") \
    .rename({"('Date','')": "date"}) \
    .pivot(
        values="value",
        index=["date", "field_1"],
        columns="field_0",
        aggregate_function="first") \
    .rename({"field_1": "ticker"})

  


# We want this.
# ┌────────┬──────────────┬───────────┬───────────┬───────────┬───────────┬───────────┬──────────┐
# │ ticker ┆ date         ┆ Adj Close ┆ Close     ┆ High      ┆ Low       ┆ Open      ┆ Volume   │
# │ ---    ┆ ---          ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---      │
# │ str    ┆ datetime[ns] ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64      │
# ╞════════╪══════════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╪══════════╡
# │ CXW    ┆ 2019-01-25   ┆ 16.794144 ┆ 19.17     ┆ 19.360001 ┆ 18.959999 ┆ 19.280001 ┆ 496300.0 │
# │        ┆ 00:00:00     ┆           ┆           ┆           ┆           ┆           ┆          │
# │ CXW    ┆ 2019-01-28   ┆ 16.855467 ┆ 19.24     ┆ 19.360001 ┆ 18.889999 ┆ 19.120001 ┆ 621000.0 │
# │        ┆ 00:00:00     ┆           ┆           ┆           ┆           ┆           ┆          │
# │ CXW    ┆ 2019-01-29   ┆ 17.197132 ┆ 19.629999 ┆ 19.690001 ┆ 19.139999 ┆ 19.290001 ┆ 457800.0 │
# │        ┆ 00:00:00     ┆           ┆           ┆           ┆           ┆           ┆          │
# │ CXW    ┆ 2019-01-30   ┆ 17.144569 ┆ 19.57     ┆ 19.790001 ┆ 19.4      ┆ 19.629999 ┆ 534000.0 │
# │        ┆ 00:00:00     ┆           ┆           ┆           ┆           ┆           ┆          │
# │ CXW    ┆ 2019-01-31   ┆ 17.407389 ┆ 19.870001 ┆ 19.870001 ┆ 19.33     ┆ 19.58     ┆ 526000.0 │
# │        ┆ 00:00:00     ┆           ┆           ┆           ┆           ┆           ┆          │
# └────────┴──────────────┴───────────┴───────────┴───────────┴───────────┴───────────┴──────────┘

# pdat = 



# pdat.write_parquet("stock.parquet")
# %%
