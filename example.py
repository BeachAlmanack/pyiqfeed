#! /usr/bin/env python3
# coding=utf-8

import time
import datetime
import pyiqfeed as iq
from pprint import pprint
import argparse

from passwords import dtn_product_id, dtn_login, dtn_password


def launch_service():
    """Check if IQFeed.exe is running and start if not"""

    svc = iq.FeedService(product=dtn_product_id,
                         version="Debugging",
                         login=dtn_login,
                         password=dtn_password)
    svc.launch()


def get_level_1_quotes_and_trades(ticker: str, seconds: int):
    """Get level 1 quotes and trades for ticker for seconds seconds."""

    quote_conn = iq.QuoteConn(name="pyiqfeed-Example-lvl1")
    quote_conn.start_runner()
    quote_listener = iq.VerboseQuoteListener("Level 1 Listener")
    quote_conn.add_listener(quote_listener)

    all_fields = sorted(list(iq.QuoteConn.quote_msg_map.keys()))
    quote_conn.select_update_fieldnames(all_fields)
    quote_conn.watch(ticker)
    time.sleep(seconds)
    quote_conn.unwatch(ticker)
    quote_conn.remove_listener(quote_listener)
    quote_conn.stop_runner()
    del quote_conn


def get_regional_quotes(ticker: str, seconds: int):
    """Get level 1 quotes and trades for ticker for seconds seconds."""

    quote_conn = iq.QuoteConn(name="pyiqfeed-Example-regional")
    quote_conn.start_runner()
    quote_listener = iq.VerboseQuoteListener("Regional Listener")
    quote_conn.add_listener(quote_listener)

    quote_conn.regional_watch(ticker)
    time.sleep(seconds)
    quote_conn.regional_unwatch(ticker)
    quote_conn.remove_listener(quote_listener)
    quote_conn.stop_runner()
    del quote_conn


def get_trades_only(ticker: str, seconds: int):
    """Get level 1 quotes and trades for ticker for seconds seconds."""

    quote_conn = iq.QuoteConn(name="pyiqfeed-Example-trades-only")
    quote_conn.start_runner()
    quote_listener = iq.VerboseQuoteListener("Trades Listener")
    quote_conn.add_listener(quote_listener)

    quote_conn.trades_watch(ticker)
    time.sleep(seconds)
    quote_conn.unwatch(ticker)
    quote_conn.remove_listener(quote_listener)
    quote_conn.stop_runner()
    del quote_conn


def get_live_interval_bars(ticker: str, bar_len: int, seconds: int):
    """Get real-time interval bars"""
    bar_conn = iq.BarConn(name='pyiqfeed-Example-interval-bars')
    bar_conn.start_runner()
    bar_listener = iq.VerboseBarListener("Bar Listener")
    bar_conn.add_listener(bar_listener)

    bar_conn.watch(symbol=ticker, interval_len=bar_len,
                   interval_type='s', update=1, lookback_bars=10)
    time.sleep(seconds)
    bar_conn.unwatch(ticker)
    bar_conn.remove_listener(bar_listener)
    bar_conn.stop_runner()
    del bar_conn


def get_administrative_messages(seconds: int):
    """Run and AdminConn and print connection stats to screen."""

    admin_conn = iq.AdminConn(name="pyiqfeed-Example-admin-messages")
    admin_conn.start_runner()
    admin_listener = iq.VerboseAdminListener("Admin Listener")
    admin_conn.add_listener(admin_listener)
    admin_conn.set_admin_variables(product=dtn_product_id,
                                   login=dtn_login,
                                   password=dtn_password,
                                   autoconnect=True)
    admin_conn.client_stats_on()
    time.sleep(seconds)


def get_tickdata(ticker: str, max_ticks: int, num_days: int):
    """Show how to read tick-data"""

    hist_conn = iq.HistoryConn(name="pyiqfeed-Example-tickdata")
    hist_conn.start_runner()
    hist_listener = iq.VerboseIQFeedListener("History Tick Listener")
    hist_conn.add_listener(hist_listener)

    # Look at docs for request_ticks, request_ticks_for_days and
    # request_ticks_in_period to see various ways to specify time periods
    # etc.

    # Get the last 10 trades
    tick_data = hist_conn.request_ticks(ticker=ticker, max_ticks=max_ticks)
    pprint(tick_data)

    # Get the last num_days days trades between 10AM and 12AM
    # Limit to max_ticks ticks otherwise too much will be printed on screen
    bgn_flt = datetime.time(hour=10, minute=0, second=0)
    end_flt = datetime.time(hour=12, minute=0, second=0)
    tick_data = hist_conn.request_ticks_for_days(ticker=ticker,
                                                 num_days=num_days,
                                                 bgn_flt=bgn_flt,
                                                 end_flt=end_flt,
                                                 max_ticks=max_ticks)
    pprint(tick_data)

    # Get all ticks between 9:30AM 5 days ago and 9:30AM today
    # Limit to max_ticks since otherwise too much will be printed on
    # screen
    today = datetime.date.today()
    sdt = today - datetime.timedelta(days=5)
    start_tm = datetime.datetime(year=sdt.year,
                                 month=sdt.month,
                                 day=sdt.day,
                                 hour=9,
                                 minute=30)
    edt = today
    end_tm = datetime.datetime(year=edt.year,
                               month=edt.month,
                               day=edt.day,
                               hour=9,
                               minute=30)

    tick_data = hist_conn.request_ticks_in_period(ticker=ticker,
                                                  bgn_prd=start_tm,
                                                  end_prd=end_tm,
                                                  max_ticks=max_ticks)
    pprint(tick_data)
    hist_conn.remove_listener(hist_listener)
    hist_conn.stop_runner()
    del hist_conn


def get_historical_bar_data(ticker: str, bar_len: int, bar_unit: str,
                            num_bars: int):
    """Shows how to get interval bars."""
    hist_conn = iq.HistoryConn(name="pyiqfeed-Example-historical-bars")
    hist_conn.start_runner()
    hist_listener = iq.VerboseIQFeedListener("History Bar Listener")
    hist_conn.add_listener(hist_listener)

    # look at docs for request_bars, request_bars_for_days and
    # request_bars_in_period for other ways to specify time periods etc
    bars = hist_conn.request_bars(ticker=ticker,
                                  interval_len=bar_len,
                                  interval_type=bar_unit,
                                  max_bars=num_bars)
    pprint(bars)
    hist_conn.remove_listener(hist_listener)
    hist_conn.stop_runner()
    del hist_conn


def get_daily_data(ticker: str, num_days: int):
    """Historical Daily Data"""
    hist_conn = iq.HistoryConn(name="pyiqfeed-Example-daily-data")
    hist_conn.start_runner()
    hist_listener = iq.VerboseIQFeedListener("History Bar Listener")
    hist_conn.add_listener(hist_listener)

    daily_data = hist_conn.request_daily_data(ticker, num_days)
    hist_conn.remove_listener(hist_listener)
    pprint(daily_data)
    hist_conn.stop_runner()
    del hist_conn


def get_reference_data():
    """Markets, SecTypes, Trade Conditions etc"""
    table_conn = iq.TableConn(name="pyiqfeed-Example-reference-data")
    table_listener = iq.VerboseIQFeedListener("Reference Data Listener")
    table_conn.add_listener(table_listener)
    table_conn.update_tables()
    print("Markets:")
    pprint(table_conn.get_markets())
    print("")

    print("Security Types:")
    pprint(table_conn.get_security_types())
    print("")

    print("Trade Conditions:")
    pprint(table_conn.get_trade_conditions())
    print("")

    print("SIC Codes:")
    pprint(table_conn.get_sic_codes())
    print("")

    print("NAIC Codes:")
    pprint(table_conn.get_naic_codes())
    print("")
    table_conn.remove_listener(table_listener)
    table_conn.stop_runner()
    del table_conn


def get_ticker_lookups(ticker: str):
    """Lookup tickers."""
    lookup_conn = iq.LookupConn(name="pyiqfeed-Example-Ticker-Lookups")
    lookup_listener = iq.VerboseIQFeedListener("TickerLookupListener")
    lookup_conn.add_listener(lookup_listener)
    lookup_conn.start_runner()

    syms = lookup_conn.request_symbols_by_filter(
        search_term=ticker, search_field='s')
    print("Symbols with %s in them" % ticker)
    pprint(syms)
    print("")

    sic_symbols = lookup_conn.request_symbols_by_sic(83)
    print("Symbols in SIC 83:")
    pprint(sic_symbols)
    print("")

    naic_symbols = lookup_conn.request_symbols_by_naic(10)
    print("Symbols in NAIC 10:")
    pprint(naic_symbols)
    print("")
    lookup_conn.remove_listener(lookup_listener)
    lookup_conn.stop_runner()
    del lookup_conn


def get_equity_option_chain(ticker: str):
    """Equity Option Chains"""
    lookup_conn = iq.LookupConn(name="pyiqfeed-Example-Eq-Option-Chain")
    lookup_listener = iq.VerboseIQFeedListener("EqOptionListener")
    lookup_conn.add_listener(lookup_listener)
    lookup_conn.start_runner()
    e_opt = lookup_conn.request_equity_option_chain(
        symbol=ticker,
        opt_type='pc',
        month_codes="".join(iq.LookupConn.equity_call_month_letters +
                            iq.LookupConn.equity_put_month_letters),
        near_months=None,
        include_binary=True,
        filt_type=0, filt_val_1=None, filt_val_2=None)
    print("Currently trading options for %s" % ticker)
    pprint(e_opt)
    lookup_conn.remove_listener(lookup_listener)
    lookup_conn.stop_runner()
    del lookup_conn


def get_futures_chain(ticker: str):
    """Futures chain"""
    lookup_conn = iq.LookupConn(name="pyiqfeed-Example-Futures-Chain")
    lookup_listener = iq.VerboseIQFeedListener("FuturesChainLookupListener")
    lookup_conn.add_listener(lookup_listener)
    lookup_conn.start_runner()

    f_syms = lookup_conn.request_futures_chain(
        symbol=ticker,
        month_codes="".join(iq.LookupConn.futures_month_letters),
        years="67",
        near_months=None,
        timeout=None)
    print("Futures symbols with underlying %s" % ticker)
    print(f_syms)
    lookup_conn.remove_listener(lookup_listener)
    lookup_conn.stop_runner()
    del lookup_conn


def get_futures_spread_chain(ticker: str):
    """Futures spread chain"""
    lookup_conn = iq.LookupConn(name="pyiqfeed-Example-Futures-Spread-Lookup")
    lookup_listener = iq.VerboseIQFeedListener("FuturesSpreadLookupListener")
    lookup_conn.add_listener(lookup_listener)
    lookup_conn.start_runner()

    f_syms = lookup_conn.request_futures_spread_chain(
        symbol=ticker,
        month_codes="".join(iq.LookupConn.futures_month_letters),
        years="67",
        near_months=None,
        timeout=None)
    print("Futures Spread symbols with underlying %s" % ticker)
    print(f_syms)
    lookup_conn.remove_listener(lookup_listener)
    lookup_conn.stop_runner()
    del lookup_conn


def get_futures_options_chain(ticker: str):
    """Futures Option Chain"""
    lookup_conn = iq.LookupConn(name="pyiqfeed-Example-Futures-Options-Chain")
    lookup_listener = iq.VerboseIQFeedListener("FuturesOptionLookupListener")
    lookup_conn.add_listener(lookup_listener)
    lookup_conn.start_runner()

    f_syms = lookup_conn.request_futures_option_chain(
        symbol=ticker,
        month_codes="".join(iq.LookupConn.futures_month_letters),
        years="67",
        near_months=None,
        timeout=None)
    print("Futures Option symbols with underlying %s" % ticker)
    print(f_syms)
    lookup_conn.remove_listener(lookup_listener)
    lookup_conn.stop_runner()
    del lookup_conn


def get_news():
    news_conn = iq.NewsConn("pyiqfeed-example-News-Conn")
    news_listener = iq.VerboseIQFeedListener("NewsListener")
    news_conn.add_listener(news_listener)
    news_conn.start_runner()

    cfg = news_conn.request_news_config()
    pprint(cfg)

    headlines = news_conn.request_news_headlines(
        sources=[], symbols=[], date=None, limit=10)
    pprint(headlines)

    story_id = headlines[0].story_id
    story = news_conn.request_news_story(story_id)
    pprint(story.story)

    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=5)

    counts = news_conn.request_story_counts(
        symbols=["AAPL", "IBM", "TSLA"],
        bgn_dt=week_ago, end_dt=today)
    pprint(counts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pyiqfeed example code")
    parser.add_argument('-l', action="store_true", dest='level_1',
                        help="Run Level 1 Quotes")
    parser.add_argument('-r', action="store_true", dest='regional_quotes',
                        help="Run Regional Quotes")
    parser.add_argument('-t', action="store_true", dest='trade_updates',
                        help="Run Trades Only Quotes")
    parser.add_argument('-i', action="store_true", dest='interval_data',
                        help="Run interval data")
    parser.add_argument("-a", action='store_true', dest='admin_socket',
                        help="Run Administrative Connection")
    parser.add_argument("-k", action='store_true', dest='historical_tickdata',
                        help="Get historical tickdata")
    parser.add_argument("-b", action='store_true', dest='historical_bars',
                        help="Get historical bar-data")
    parser.add_argument("-d", action='store_true', dest='historical_daily_data',
                        help="Get historical daily data")
    parser.add_argument("-f", action='store_true', dest='reference_data',
                        help="Get reference data")
    parser.add_argument("-c", action='store_true', dest='lookups_and_chains',
                        help="Lookups and Chains")
    parser.add_argument("-n", action='store_true', dest='news',
                        help="News related stuff")
    results = parser.parse_args()

    launch_service()

    if results.level_1:
        get_level_1_quotes_and_trades(ticker="SPY", seconds=10)
    if results.regional_quotes:
        get_regional_quotes(ticker="SPY", seconds=10)
    if results.trade_updates:
        get_trades_only(ticker="SPY", seconds=10)
    if results.interval_data:
        get_live_interval_bars(ticker="SPY", bar_len=15, seconds=20)
    if results.admin_socket:
        get_administrative_messages(seconds=5)
    if results.historical_tickdata:
        get_tickdata(ticker="SPY", max_ticks=100, num_days=2)
    if results.historical_bars:
        get_historical_bar_data(ticker="SPY",
                                bar_len=60,
                                bar_unit='s',
                                num_bars=100)
    if results.historical_daily_data:
        get_daily_data(ticker="SPY", num_days=10)
    if results.reference_data:
        get_reference_data()
    if results.lookups_and_chains:
        get_ticker_lookups("SPH9GBM1")
        get_equity_option_chain("SPY")
        get_futures_chain("@VX")
        get_futures_spread_chain("@VX")
        get_futures_options_chain("CL")
    if results.news:
        get_news()
