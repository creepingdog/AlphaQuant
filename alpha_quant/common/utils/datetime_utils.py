import pandas as pd
from datetime import datetime, timedelta
import pytz


def datetime_to_did(date):
    """
    >>> import alpha_quant.common.utils.datetime_utils as dtu
    >>> dtu.datetime_to_did(datetime(2019, 9, 25))
    20190925
    >>> adt_utc = datetime(2020, 8, 7, 2, 0, 0, tzinfo=pytz.UTC)
    >>> adt_ny = adt_utc.astimezone(pytz.timezone('America/New_York'))
    >>> dtu.datetime_to_did(adt_utc)
    20200807
    >>> dtu.datetime_to_did(adt_ny)
    20200806
    """
    return int(date.strftime('%Y%m%d %Z')[:8])
#


def did_to_datetime(did, timezone=None):
    """
    >>> import alpha_quant.common.utils.datetime_utils as dtu
    >>> dtu.did_to_datetime(did=20190925)
    datetime.datetime(2019, 9, 25, 0, 0)
    """
    dt = datetime.strptime(str(did), '%Y%m%d')
    if timezone is not None:
        dt = dt.replace(tzinfo=pytz.timezone(timezone))
    #

    return dt
#


def did_to_datestr(did, sep='-'):
    """
    >>> import alpha_quant.common.utils.datetime_utils as dtu
    >>> dtu.did_to_datestr(did=20190925)
    '2019-09-25'
    >>> dtu.did_to_datestr(did=20191013, sep='/')
    '2019/10/13'
    """
    date = str(did)
    return f'{date[:4]}{sep}{date[4:6]}{sep}{date[6:]}'
#


def today(timezone=None):
    today = datetime.now() if timezone is None else datetime.now(pytz.timezone(timezone))
    return datetime_to_did(date=today)
#


def is_weekday(date):
    """
    >>> import alpha_quant.common.utils.datetime_utils as dtu
    >>> dtu.is_weekday(20200511)
    True
    """
    if isinstance(date, int):
        date = did_to_datetime(did=date)
    elif not isinstance(date, datetime):
        raise Exception(f'type(date)={type(date)} is not supported [int|datetime] !')
    #
    return date.weekday() not in [5, 6]
#


def get_biz_dids(start_did, end_did):
    """
    >>> import alpha_quant.common.utils.datetime_utils as dtu
    >>> dtu.get_biz_dids(start_did=20200910, end_did=20200917)
    [20200910, 20200911, 20200914, 20200915, 20200916, 20200917]
    """
    bdates = pd.bdate_range(did_to_datestr(did=start_did, sep='-'),
                            did_to_datestr(did=end_did, sep='-')).strftime('%Y%m%d')
    return [int(date) for date in bdates]
#


def next_biz_did(did):
    one_day = timedelta(days=1)
    next_day = did_to_datetime(did) + one_day
    while not is_weekday(date=next_day):
        next_day += one_day
    #
    return datetime_to_did(next_day)
#


def parse_datetime(dt, format=None, timezone=None, ret_as_timestamp=False):
    if isinstance(dt, int):
        dt = str(dt)
    #
    if (isinstance(dt, datetime) and not ret_as_timestamp) or \
            (isinstance(dt, pd.Timestamp) and ret_as_timestamp):
        return dt
    #

    try:
        dt = pd.Timestamp(dt)
        if timezone is not None:
            dt = dt.tz_localize(timezone)
        #
    except Exception:
        pass
    #

    if isinstance(dt, pd.Timestamp):
        return (dt if ret_as_timestamp else dt.to_pydatetime())
    #
    if isinstance(dt, str):
        dt = pd.to_datetime(dt, format=format)
        if timezone is not None:
            dt = dt.tz_localize(timezone)
        #
        return (dt if ret_as_timestamp else dt.to_pydatetime())
    #
    raise Exception(f'type(dt)={type(dt)} is not supported [did|str|datetime|pd.Timestamp|np.datetime64] !')
#
