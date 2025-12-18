import collections
import itertools
from visidata import vd, Column, Sheet, SettableColumn, Progress, asyncthread, anytype

class ReverseCompare:
    def __init__(self, obj):
        self.obj = obj
    def __lt__(self, other):
        try:
            return other.obj < self.obj
        except TypeError:
            return str(other.obj) < str(self.obj)
    def __eq__(self, other):
        return self.obj == other.obj

class WindowSpec:
    def __init__(self, colname, funcname, args):
        self.colname = colname
        self.funcname = funcname
        self.args = args
        self.partitions = []
        self.orderings = []  # list of (colname, desc)

    def partition_by(self, *colnames):
        self.partitions.extend(colnames)
        return self

    def order_by(self, *colnames, desc=False):
        for colname in colnames:
            self.orderings.append((colname, desc))
        return self

class WindowDSL:
    def __init__(self, colname):
        self.colname = colname

    def lag(self, n=1):
        return WindowSpec(self.colname, 'lag', (n,))

    def lead(self, n=1):
        return WindowSpec(self.colname, 'lead', (n,))

    def moving_average(self, n=3):
        return WindowSpec(self.colname, 'moving_average', (n,))

def calculate_window_function(sheet, spec):
    # 1. Resolve columns
    source_col = sheet.column(spec.colname)
    if not source_col:
        vd.fail(f"column '{spec.colname}' not found")

    partition_cols = [sheet.column(c) for c in spec.partitions]
    for c, name in zip(partition_cols, spec.partitions):
        if not c:
            vd.fail(f"partition column '{name}' not found")

    order_cols = [(sheet.column(c), desc) for c, desc in spec.orderings]
    for c, (col, desc) in zip(spec.orderings, order_cols):
        if not col:
            vd.fail(f"order column '{c[0]}' not found")

    # 2. Type validation
    if spec.funcname == 'moving_average':
        if source_col.type not in (int, float):
            vd.fail(f"moving_average requires numeric column, but '{source_col.name}' is {source_col.typestr}")

    # 3. Preparation: extract data and keep original row indices
    # row_data: (partition_key, order_key, source_value, original_index)
    row_data = []
    for i, row in enumerate(sheet.rows):
        part_key = tuple(c.getTypedValue(row) for c in partition_cols)
        # order_key needs to handle desc
        sort_key = []
        for c, desc in order_cols:
            val = c.getTypedValue(row)
            sort_key.append(val)
        
        row_data.append({
            'part_key': part_key,
            'sort_key': tuple(sort_key),
            'val': source_col.getTypedValue(row),
            'idx': i
        })

    # 4. Sort
    # We sort by part_key first, then by sort_key
    # Since Python's sort is stable, we can sort by order keys in reverse if needed,
    # but it's easier to just define a key function.

    # Custom sort for handling desc
    # First sort by partition key
    # Then within each partition, sort by order columns
    # Actually, let's just use the partition_key as the primary sort key
    # and then the order keys.
    
    def get_full_sort_key(item):
        key = [item['part_key']]
        for (col, desc), val in zip(order_cols, item['sort_key']):
            # We wrap values to invert comparison for desc
            if desc:
                key.append(ReverseCompare(val))
            else:
                key.append(val)
        return tuple(key)


    row_data.sort(key=get_full_sort_key)

    # 5. Apply function within partitions
    results = [None] * len(sheet.rows)
    
    for part_key, group in itertools.groupby(row_data, key=lambda x: x['part_key']):
        group = list(group)
        n_group = len(group)
        
        if spec.funcname == 'lag':
            offset = spec.args[0]
            for i in range(n_group):
                if i >= offset:
                    results[group[i]['idx']] = group[i-offset]['val']
                else:
                    results[group[i]['idx']] = None
                    
        elif spec.funcname == 'lead':
            offset = spec.args[0]
            for i in range(n_group):
                if i + offset < n_group:
                    results[group[i]['idx']] = group[i+offset]['val']
                else:
                    results[group[i]['idx']] = None
                    
        elif spec.funcname == 'moving_average':
            n = spec.args[0]
            # Trailing average
            for i in range(n_group):
                start = max(0, i - n + 1)
                window = [group[j]['val'] for j in range(start, i + 1) if group[j]['val'] is not None]
                if window:
                    results[group[i]['idx']] = sum(window) / len(window)
                else:
                    results[group[i]['idx']] = None

    return results

@Sheet.api
def addcol_window_func(sheet):
    expr = sheet.inputExpr("window expr (e.g. col.lag(1).partition_by('p')): ")
    if not expr:
        return
    sheet._addcol_window_func_heavy(expr)

@Sheet.api
@asyncthread
def _addcol_window_func_heavy(sheet, expr):
    # Create evaluation context
    # We want to allow: colname.lag(1)...
    # So we'refill globals with proxies for all columns
    ctx = {col.name: WindowDSL(col.name) for col in sheet.columns}
    # Add other globals for safety
    ctx.update(vd.getGlobals())
    
    try:
        spec = eval(expr, ctx)
    except Exception as e:
        vd.error(f"invalid window expression: {e}")
        return

    if not isinstance(spec, WindowSpec):
        vd.error("expression must result in a window function (e.g. .lag(), .lead(), .moving_average())")
        return

    # Pre-calculate values
    with Progress(gerund='calculating window function', total=sheet.nRows) as prog:
        vals = calculate_window_function(sheet, spec)
        
    # Add column
    colname = f"{spec.colname}_{spec.funcname}"
    res_type = anytype
    if spec.funcname == 'moving_average':
        res_type = float
    else:
        # try to inherit type from source col
        source_col = sheet.column(spec.colname)
        if source_col:
            res_type = source_col.type

    newcol = SettableColumn(colname, type=res_type)
    sheet.addColumnAtCursor(newcol)
    newcol.setValues(sheet.rows, *vals)
    vd.status(f"added window column '{colname}'")


Sheet.addCommand('', 'addcol-window-func', 'addcol_window_func()', 'add column based on window function expression')

vd.addMenuItems('''
    Column > Add column > Window function column > addcol-window-func
''')

vd.addGlobals(calculate_window_function=calculate_window_function)
