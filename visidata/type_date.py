import datetime
import re

from visidata import VisiData, vd, Sheet, Column, AttrDict, dispwidth


_BRACKET_TRAIL_RE = re.compile(r'\[[^\]]*\]\s*$')
_BRACKET_ANY_RE = re.compile(r'\[[^\]]*\]')

@VisiData.lazy_property
def date_parse(vd):
    try:
        from dateutil.parser import parse
        return parse
    except ImportError:
        vd.warning('install python-dateutil for date type')
        return str


def _normalize_datestr(val: str, allow_wild: bool = False) -> str:
    """Return *val* normalized for python-dateutil parsing.

    Removes bracketed timezone annotations (e.g. ``[UTC]``) and converts a
    trailing ``Z`` into ``+00:00`` so that dateutil consistently recognizes it.
    When *allow_wild* is True, bracketed annotations anywhere in the string are
    stripped instead of just the trailing suffix.
    """
    s = (val or '').strip()
    if not s:
        return s

    # Normalize explicit "Z[UTC]" suffixes first.
    s = s.replace('Z[UTC]', 'Z')

    if allow_wild:
        s = _BRACKET_ANY_RE.sub('', s)
    else:
        s = _BRACKET_TRAIL_RE.sub('', s)

    if s.endswith('Z'):
        s = s[:-1] + '+00:00'

    return s

vd.help_date = '''
- RFC3339: `%Y-%m-%d %H:%M:%S.%f %z`
- `%A`  Weekday as locale’s full name.
- `%w`  Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.
- `%d`  Day of the month as a zero-padded decimal number.
- `%b`  Month as locale’s abbreviated name.
- `%B`  Month as locale’s full name.
- `%p`  Locale’s equivalent of either AM or PM.
- `%c`  Locale’s appropriate date and time representation.
- `%x`  Locale’s appropriate date representation.
- `%X`  Locale’s appropriate time representation.
- `%Z`  Time zone name (empty string if the object is naive).

See [:onclick https://strftime.org]Python strftime()[/] for a full list of format codes.
'''

vd.option('disp_date_fmt','%Y-%m-%d', 'default fmtstr passed to strftime for date values', replay=True, help=vd.help_date)


@vd.numericType('@', '', formatter=lambda fmtstr,val: val.strftime(fmtstr or vd.options.disp_date_fmt))
class date(datetime.datetime):
    'datetime wrapper, constructed from time_t or from str with dateutil.parse'

    def __new__(cls, *args, **kwargs):
        'datetime is immutable so needs __new__ instead of __init__'
        if not args:
            return datetime.datetime.now()
        elif len(args) > 1:
            return super().__new__(cls, *args, **kwargs)

        s = args[0]
        if isinstance(s, int) or isinstance(s, float):
            r = datetime.datetime.fromtimestamp(s)
        elif isinstance(s, str):
            cleaned = _normalize_datestr(s)
            try:
                r = vd.date_parse(cleaned)
            except ValueError:
                r = vd.date_parse(_normalize_datestr(cleaned, allow_wild=True))
        elif isinstance(s, (datetime.datetime, datetime.date)):
            r = s
        else:
            raise Exception('invalid type for date %s' % type(s).__name__)

        t = r.timetuple()
        ms = getattr(r, 'microsecond', 0)
        tzinfo = getattr(r, 'tzinfo', None)
        return super().__new__(cls, *t[:6], microsecond=ms, tzinfo=tzinfo, **kwargs)

    def __lt__(self, b):
        if isinstance(b, datetime.datetime): return datetime.datetime.__lt__(self, b)
        elif isinstance(b, datetime.date):   return not self.date().__eq__(b) and self.date().__lt__(b)
        return NotImplemented

    def __gt__(self, b):
        if isinstance(b, datetime.datetime): return datetime.datetime.__gt__(self, b)
        elif isinstance(b, datetime.date):   return not self.date().__eq__(b) and self.date().__gt__(b)
        return NotImplemented

    def __le__(self, b):
        if isinstance(b, datetime.datetime): return datetime.datetime.__le__(self, b)
        elif isinstance(b, datetime.date):   return self.date().__le__(b)
        return NotImplemented

    def __ge__(self, b):
        if isinstance(b, datetime.datetime): return datetime.datetime.__ge__(self, b)
        elif isinstance(b, datetime.date):   return self.date().__ge__(b)
        return NotImplemented

    def __eq__(self, b):
        if isinstance(b, datetime.datetime): return datetime.datetime.__eq__(self, b)
        elif isinstance(b, datetime.date): return self.date().__eq__(b)
        return NotImplemented

    def __str__(self):
        return self.strftime(vd.options.disp_date_fmt)

    def __hash__(self):
        return super().__hash__()

    def __float__(self):
        return self.timestamp()

    def __radd__(self, n):
        return self.__add__(n)

    def __add__(self, n):
        'add n days (int or float) to the date'
        if isinstance(n, (int, float)):
            n = datetime.timedelta(days=n)
        return date(super().__add__(n))

    def __sub__(self, n):
        'subtract n days (int or float) from the date.  or subtract another date for a timedelta'
        if isinstance(n, (int, float)):
            n = datetime.timedelta(days=n)
        elif isinstance(n, (date, datetime.datetime)):
            return datedelta(super().__sub__(n).total_seconds()/(24*60*60))
        return super().__sub__(n)


DATE_TYPE_CHOICES = [
    AttrDict(key='datetime', desc='Date & time', fmtstr='%Y-%m-%d %H:%M:%S'),
    AttrDict(key='date', desc='Date', fmtstr=''),
    AttrDict(key='month', desc='Month', fmtstr='%Y-%m'),
    AttrDict(key='year', desc='Year', fmtstr='%Y'),
]

DATE_TYPE_LOOKUP = {choice.key: choice for choice in DATE_TYPE_CHOICES}

Column.init('date_type_key', lambda: '', copy=True)


@VisiData.property
def date_type_choices(vd):
    return DATE_TYPE_CHOICES


@VisiData.api
def chooseDateType(vd, prompt='choose date type: '):
    pad = ' ' * max(dispwidth(prompt)-3, 0)

    def _fmt_summary(match, row, trigger_key):
        code = match.formatted.get('key', row.key) if match else row.key
        label = match.formatted.get('desc', row.desc) if match else row.desc
        return f"{pad}[:keystrokes]{trigger_key}[/]  {code} - {label}"

    # Only pass string fields to the palette to avoid None in fuzzymatch
    items = [AttrDict(key=c.key, desc=c.desc) for c in vd.date_type_choices]

    return vd.activeSheet.inputPalette(
        prompt,
        items,
        value_key='key',
        formatter=_fmt_summary,
        type='date',
    )


@Column.api
def applyDateType(col, date_type_key, *, recalc=True, quiet=False):
    choice = DATE_TYPE_LOOKUP.get(date_type_key)
    if not choice:
        vd.warning(f'date type does not exist: {date_type_key}')
        return col

    col.type = date
    col.date_type_key = choice.key
    col.displayer = 'generic'

    fmtstr = choice.fmtstr or vd.options.disp_date_fmt
    col.fmtstr = fmtstr
    if recalc:
        col.recalc()

    if not quiet:
        desc = getattr(choice, 'desc', None)
        text = desc if isinstance(desc, str) else choice.key
        text_str = str(text)
        vd.status(f'{col.name} typed as {text_str.lower()}')
    return col


@Column.api
def chooseDateType(col):
    selected = vd.chooseDateType()
    if selected:
        col.applyDateType(selected)


@Column.api
def copyDateMetadata(col, src_col):
    src_key = getattr(src_col, 'date_type_key', '')
    if not src_key:
        return col

    # Preserve formatting without triggering a full recalc or status update.
    col.applyDateType(src_key, recalc=False, quiet=True)
    col.fmtstr = getattr(src_col, '_fmtstr', None) or col.fmtstr
    return col


class datedelta(datetime.timedelta):
    def __float__(self):
        return self.total_seconds()


# simple constants, for expressions like 'timestamp+15*minutes'
vd.addGlobals(
    years=365.25,
    months=30.0,
    weeks=7.0,
    days=1.0,
    hours=1.0/24,
    minutes=1.0/(24*60),
    seconds=1.0/(24*60*60),
    datedelta=datedelta,
    datetime=date,
    date=date)


Sheet.addCommand('@', 'choose-date-type', 'cursorCol.chooseDateType()', 'choose date type for the current column')
Sheet.addCommand('', 'type-date', 'cursorCol.applyDateType("date")', 'set type of current column to date')
Sheet.addCommand('', 'type-datedelta', 'cursorCol.type = datedelta', 'set type of current column to datedelta')
Sheet.addCommand('', 'type-datetime', 'cursorCol.applyDateType("datetime")', 'set type of current column to datetime')
Sheet.addCommand('', 'type-month', 'cursorCol.applyDateType("month")', 'set type of current column to month')
Sheet.addCommand('', 'type-year', 'cursorCol.applyDateType("year")', 'set type of current column to year')

vd.addMenuItems('''
    Column > Type as > date > type-date
    Column > Type as > datetime > type-datetime
    Column > Type as > month > type-month
    Column > Type as > year > type-year
    Column > Type as > datedelta > type-datedelta
''')
