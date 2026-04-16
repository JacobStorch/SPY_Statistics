import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_ohlcv(ticker, start_date="2010-01-01", end_date=None):
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')
    
    df = yf.download(ticker, start=start_date, end=end_date, progress=False)
    
    if df.empty:
        return None
    
    df.reset_index(inplace=True)
    df["ticker"] = ticker
    
    return df


def fetch_ticker_data(tickers, start_date="2010-01-01"):
    all_data = []
    
    for ticker in tickers:
        new_cols = []
        print(f"Fetching {ticker}...")
        df = fetch_ohlcv(ticker, start_date)
        for col in df.columns:
            if isinstance(col, tuple):
                col = col[0] 
            new_cols.append(col)
        print(ticker, new_cols)
        df.columns = new_cols
        
        if df is not None:
            all_data.append(df)
    
    if not all_data:
        return pd.DataFrame()
    
    for ticker in all_data:
        for col in ticker:
            print(col)

    combined = pd.concat(all_data, ignore_index=True)
    
    # Standardize column names
    combined.columns = [col.lower().replace(" ", "_") for col in combined.columns]
    
    return combined


def get_company_info(tickers):
    data = []
    
    for stock_ticker in tickers:
        tkr = yf.Ticker(stock_ticker)
        info = tkr.info
        print('info',info)
        
        sector = info.get('sector', '')
        industry = info.get('industry', '')
        city = info.get('city', '')
        state = info.get('state', '')
        
        data.append({
            'ticker': stock_ticker,
            'sector': sector,
            'industry': industry,
            'city': city,
            'state': state
        })
    
    df = pd.DataFrame(data)

    return df
    
    
def get_sp500_tickers():
    tickers = [
    "NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "AVGO", "META", "TSLA", "BRK-B", "WMT", "LLY", "JPM", 
    "XOM", "V", "JNJ", "COST", "MA", "MU", "NFLX", "ORCL", "CVX", "ABBV", "AMD", "BAC", "PLTR", "CAT", "PG", 
    "KO", "CSCO", "HD", "GE", "MRK", "AMAT", "LRCX", "UNH", "MS", "RTX", "INTC", "GS", "WFC", "PM", "GEV", 
    "IBM", "LIN", "TMUS", "MCD", "AXP", "PEP", "C", "VZ", "KLAC", "T", "NEE", "AMGN", "TMO", "TXN", "ABT", 
    "TJX", "GILD", "DIS", "CRM", "ANET", "BA", "SCHW", "ISRG", "COP", "ADI", "APH", "DE", "PFE", "BLK", "UBER", 
    "LMT", "UNP", "HON", "ETN", "WELL", "APP", "PANW", "DHR", "QCOM", "SPGI", "LOW", "SYK", "GLW", "CB", "NEM", 
    "PLD", "ACN", "BMY", "PGR", "DELL", "PH", "INTU", "COF", "CME", "MDT", "MO", "HCA", "VRTX", "SBUX", "SO", 
    "CRWD", "WDC", "NOW", "STX", "SNDK", "MCK", "DUK", "CMCSA", "VRT", "CVS", "EQIX", "CEG", "NOC", "ADBE", 
    "TT", "HWM", "GD", "WM", "ICE", "BSX", "WMB", "MAR", "BX", "FCX", "PNC", "BK", "MRSH", "FDX", "USB", "PWR", 
    "UPS", "ADP", "JCI", "AMT", "KKR", "REGN", "SHW", "MCO", "CDNS", "CMI", "CSX", "EOG", "ORLY", "SNPS", "EMR", 
    "SLB", "MMM", "VLO", "ABNB", "ITW", "ECL", "MDLZ", "KMI", "MSI", "RCL", "CI", "MPC", "MNST", "AEP", "CRH", 
    "PSX", "ROST", "ELV", "WBD", "AON", "CTAS", "RSG", "HLT", "DASH", "CL", "TDG", "LHX", "GM", "APD", "NSC", 
    "SRE", "TRV", "CIEN", "NKE", "HOOD", "DLR", "COR", "TEL", "PCAR", "OXY", "SPG", "FTNT", "BKR", "APO", 
    "TFC", "MPWR", "LITE", "O", "CTVA", "AFL", "AJG", "OKE", "AZO", "D", "ALL", "TGT", "FANG", "TRGP", "VST", 
    "FAST", "ETR", "GWW", "KEYS", "EA", "EXC", "FIX", "CAH", "AME", "ADSK", "XEL", "TER", "ZTS", "NXPI", "NDAQ", 
    "PSA", "COHR", "MET", "EW", "COIN", "GRMN", "F", "URI", "CVNA", "CARR", "IDXX", "KR", "BDX", "WAB", "FITB", 
    "DAL", "CMG", "EBAY", "YUM", "HSY", "ODFL", "DDOG", "PYPL", "ED", "AIG", "ROK", "CBRE", "PEG", "MSCI", 
    "DHI", "VTR", "NUE", "AMP", "PCG", "WEC", "EQT", "HIG", "CCI", "ROP", "TTWO", "LYV", "LVS", "VMC", "SATS", 
    "XYZ", "MCHP", "STT", "CCL", "SYY", "ADM", "KDP", "ACGL", "PRU", "MLM", "PAYX", "EME", "RMD", "WDAY", "HPE", 
    "A", "KVUE", "HBAN", "HAL", "CPRT", "NRG", "GEHC", "ATO", "IRM", "IR", "CBOE", "TPL", "KMB", "DTE", "DVN", 
    "AEE", "MTB", "XYL", "IBKR", "OTIS", "AXON", "CTSH", "DOW", "VICI", "WAT", "FISV", "FE", "TDY", "PPL", "UAL", 
    "JBL", "IQV", "CNP", "TPR", "RJF", "EXR", "DOV", "EIX", "CHTR", "EXPE", "KHC", "NTRS", "WTW", "DG", "STZ", 
    "AWK", "HUBB", "CFG", "CTRA", "ES", "STLD", "MTD", "FICO", "LYB", "ROL", "BIIB", "VRSN", "EL", "WRB", "ON", 
    "VRSK", "CINF", "Q", "BG", "EXE", "DXCM", "FIS", "SYF", "CMS", "HUM", "ARES", "AVB", "ULTA", "TSCO", "PPG", 
    "NI", "TSN", "EQR", "BRO", "RF", "DRI", "L", "PHM", "LH", "KEY", "EFX", "DGX", "VLTO", "SBAC", "CHD", "OMC", 
    "STE", "WSM", "LEN", "DLTR", "RL", "FSLR", "JBHT", "SW", "CF", "ALB", "LDOS", "CPAY", "MRNA", "PFG", "GIS", 
    "TROW", "CHRW", "NTAP", "EXPD", "SNA", "EVRG", "LNT", "WST", "LUV", "BR", "INCY", "DD", "IP", "AMCR", "PKG", 
    "NVR", "ZBH", "IFF", "LULU", "CNC", "FTV", "FFIV", "GPN", "WY", "CSGP", "PTC", "HPQ", "HOLX", "AKAM", "ESS", 
    "HII", "BALL", "LII", "CDW", "INVH", "KIM", "VTRS", "TRMB", "TXT", "APA", "TKO", "J", "PODD", "NDSN", "MAA", 
    "GPC", "IEX", "TYL", "DECK", "REG", "PNR", "MKC", "SMCI", "COO", "BBY", "EG", "HST", "ERIE", "AVY", "HAS", 
    "CLX", "DPZ", "BEN", "PNW", "APTV", "BF-B", "PSKY", "FOX", "MAS", "ALLE", "FOXA", "ALGN", "HRL", "DOC", 
    "GEN", "JKHY", "UDR", "GL", "GNRC", "GDDY", "UHS", "AIZ", "SOLV", "CPT", "SWK", "IT", "WYNN", "ZBRA", "AES", 
    "SJM", "DVA", "TTD", "MGM", "RVTY", "IVZ", "FRT", "NWSA", "AOS", "BLDR", "BAX", "NCLH", "TAP", "HSIC", "FDS", 
    "TECH", "MOS", "CRL", "SWKS", "BXP", "ARE", "CAG", "POOL", "EPAM", "CPB", "BKNG", "NWS"
    ]

    return tickers

if __name__ == "__main__":
    # Example: start small, then scale up
    tickers = get_sp500_tickers()
    
    ticker_data = fetch_ticker_data(tickers, start_date="2015-01-01")
    company_info = get_company_info(tickers)
    SPY_data = fetch_ticker_data(["SPY"], start_date="2015-01-01")
    
    ticker_data.to_csv("stock_data.csv", index=False)
    company_info.to_csv("company_info.csv", index=False)
    SPY_data.to_csv("SPY_data.csv", index=False)

