from visidata import vd, Sheet, Column, VisiData, AttrDict, dispwidth

vd.option('disp_currency_fmt', '%.02f', 'default fmtstr to format for currency values', replay=True, help=vd.help_float_fmt)
vd.theme_option('color_currency_neg', 'red', 'color for negative values in currency displayer', replay=True)


floatchars='+-0123456789.'

CURRENCY_CHOICES = [
    AttrDict(key='USD', desc='US Dollar', symbol='$'),
    AttrDict(key='EUR', desc='Euro', symbol='€'),
    AttrDict(key='JPY', desc='Japanese Yen', symbol='¥'),
    AttrDict(key='GBP', desc='British Pound Sterling', symbol='£'),
    AttrDict(key='CNY', desc='Chinese Yuan Renminbi', symbol='CN¥'),
    AttrDict(key='AUD', desc='Australian Dollar', symbol='A$'),
    AttrDict(key='CAD', desc='Canadian Dollar', symbol='C$'),
    AttrDict(key='CHF', desc='Swiss Franc', symbol='CHF'),
    AttrDict(key='HKD', desc='Hong Kong Dollar', symbol='HK$'),
    AttrDict(key='SGD', desc='Singapore Dollar', symbol='S$'),
    AttrDict(key='NOK', desc='Norwegian Krone', symbol='Nkr'),
    AttrDict(key='KRW', desc='South Korean Won', symbol='₩'),
    AttrDict(key='SEK', desc='Swedish Krona', symbol='Skr'),
    AttrDict(key='NZD', desc='New Zealand Dollar', symbol='NZ$'),
    AttrDict(key='INR', desc='Indian Rupee', symbol='₹'),
    AttrDict(key='TWD', desc='New Taiwan Dollar', symbol='NT$'),
    AttrDict(key='ZAR', desc='South African Rand', symbol='R'),
    AttrDict(key='BRL', desc='Brazilian Real', symbol='R$'),
    AttrDict(key='MXN', desc='Mexican Peso', symbol='MX$'),
    AttrDict(key='TRY', desc='Turkish Lira', symbol='₺'),
    AttrDict(key='UAH', desc='Ukrainian Hryvnia', symbol='₴'),
    AttrDict(key='KZT', desc='Kazakhstani Tenge', symbol='₸'),
    AttrDict(key='GEL', desc='Georgian Lari', symbol='₾'),
    AttrDict(key='AMD', desc='Armenian Dram', symbol='֏'),
    AttrDict(key='RUB', desc='Russian Ruble', symbol='₽'),
]

_CURRENCY_LOOKUP = {choice.key: choice for choice in CURRENCY_CHOICES}

Column.init('currency_code', lambda: '', copy=True)


def _normalize_currency_code(code: str) -> str:
    return (code or '').strip().upper()


def _currency_symbol(code: str) -> str:
    choice = _CURRENCY_LOOKUP.get(code)
    return choice.symbol if choice else ''


@VisiData.property
def currency_choices(vd):
    return CURRENCY_CHOICES


@VisiData.api
def chooseCurrency(vd, prompt='choose currency: '):
    def _fmt_currency_summary(match, row, trigger_key):
        formatted_code = match.formatted.get('key', row.key) if match else row.key
        r = ' '*(dispwidth(prompt)-3)
        r += f'[:keystrokes]{trigger_key}[/]  '
        r += formatted_code
        if row.desc:
            r += ' - '
            r += match.formatted.get('desc', row.desc) if match else row.desc
        return r

    return vd.activeSheet.inputPalette(
        prompt,
        vd.currency_choices,
        value_key='key',
        formatter=_fmt_currency_summary,
        type='currency',
    )


@Column.api
def applyCurrencyType(col, currency_code):
    normalized = _normalize_currency_code(currency_code)
    if normalized not in _CURRENCY_LOOKUP:
        vd.warning(f'currency does not exist: {currency_code}')
        return

    col.type = currency
    col.displayer = 'currency'
    col.currency_code = normalized
    if not col._fmtstr:
        col.fmtstr = vd.options.disp_currency_fmt
    col.recalc()
    vd.status(f'{col.name} typed as currency ({normalized})')


@Column.api
def chooseCurrencyType(col):
    currency_code = vd.chooseCurrency()
    col.applyCurrencyType(currency_code)


@Column.api
def copyCurrencyMetadata(col, src_col):
    currency_code = getattr(src_col, 'currency_code', '')
    if not currency_code:
        return col

    col.currency_code = currency_code
    col.displayer = 'currency'

    if not getattr(col, '_fmtstr', None):
        src_fmt = getattr(src_col, '_fmtstr', None)
        if src_fmt:
            col.fmtstr = src_fmt
        else:
            col.fmtstr = vd.options.disp_currency_fmt

    return col


@vd.numericType('$')
def currency(*args):
    'dirty float (strip non-numeric characters)'
    if args and isinstance(args[0], str):
        args = [''.join(ch for ch in args[0] if ch in floatchars)]
    return float(*args)


@Column.api
def displayer_currency(col, dw, width=None):
    text = dw.text
    currency_code = getattr(col, 'currency_code', '')
    symbol = _currency_symbol(currency_code)

    if isinstance(dw.typedval, (int, float)):
        if dw.typedval < 0:
            digits = text[1:] if text.startswith('-') else text
            if symbol and not digits.startswith(symbol):
                digits = f'{symbol}{digits}'
            text = f'({digits})'
            if width:
                text = text.rjust(width-1)
            yield ('currency_neg', '')
        else:
            if symbol and not text.startswith(symbol):
                text = f'{symbol}{text}'
            if width:
                text = text.rjust(width-2)
    elif symbol and text and not text.startswith(symbol):
        text = f'{symbol}{text}'
    yield ('', text)

Sheet.addCommand('$', 'type-currency', 'cursorCol.chooseCurrencyType()', 'set type of current column to currency')

vd.addMenuItems('''
    Column > Type as > dirty float > type-currency
''')
