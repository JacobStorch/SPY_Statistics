--CAGR by Sector
WITH starting_prices as (SELECT DISTINCT ticker, open from stock_data WHERE date = '2016-01-04'),
ending_prices as (SELECT DISTINCT ticker, open from stock_data WHERE date = '2026-01-02'),
diffs AS (SELECT starting_prices.ticker,(ending_prices.open / starting_prices.open) AS growth_factor
	FROM starting_prices JOIN ending_prices ON starting_prices.ticker = ending_prices.ticker),
joined_tables AS (SELECT * FROM diffs JOIN company_info on diffs.ticker = company_info.ticker),
output AS (SELECT power(AVG(growth_factor),0.1)-1 as avg_CAGR, count(DISTINCT ticker) as sector_count, sector FROM joined_tables GROUP BY sector)
SELECT * FROM output ORDER BY avg_CAGR DESC;

--S&P Annual Volatility
WITH prev_close_table AS (SELECT ticker, date, close, LAG(close) OVER (ORDER BY date) AS prev_close FROM SPY_Data),
daily_return_table AS (SELECT *, (close / prev_close - 1) AS daily_return FROM prev_close_table ORDER BY date)
SELECT SQRT(AVG(daily_return*daily_return) - AVG(daily_return)*AVG(daily_return))*sqrt(252) AS annual_volatility FROM daily_return_table;

--Volatility by Sector
WITH prev_close_table AS (SELECT *, LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS prev_close FROM stock_data),
daily_return_table AS (SELECT *, (close / prev_close - 1) AS daily_return FROM prev_close_table ORDER BY ticker, date),
ticker_volatility AS (SELECT ticker,(SQRT(AVG(daily_return*daily_return) - AVG(daily_return)*AVG(daily_return))*sqrt(252)) AS annual_volatility FROM daily_return_table GROUP BY ticker),
output AS (SELECT * FROM ticker_volatility JOIN company_info on ticker_volatility.ticker = company_info.ticker)
SELECT sector, avg(annual_volatility) as average_annual_volatility FROM output GROUP BY sector ORDER BY average_annual_volatility DESC;