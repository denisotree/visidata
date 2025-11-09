from visidata import vd, Column, Sheet, Progress, date


@Sheet.api
def addcol_percent_total(sheet, col):
    if not vd.isNumeric(col) or col.type is date:
        vd.fail('current column must be numeric (non-date)')

    total = 0.0
    for row in Progress(sheet.rows, 'summing'):
        v = col.getTypedValue(row)
        if isinstance(v, (int, float)):
            total += float(v)

    if not total:
        vd.fail('total is zero')

    def getter(newcol, row, _col=col, _total=total):
        v = _col.getTypedValue(row)
        return float(v) * 100.0 / _total if isinstance(v, (int, float)) else None

    return Column(f'{col.name}_pct', type=float, getter=getter)


Sheet.addCommand('gf', 'addcol-percent-total', 'addColumnAtCursor(addcol_percent_total(cursorCol))', 'add column with percent of total for current numeric column')

vd.addMenuItems('Column > Add column > percent of total > addcol-percent-total')
