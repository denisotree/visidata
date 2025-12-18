import pytest
from unittest.mock import MagicMock
from visidata.features.window_func import WindowSpec, calculate_window_function

def test_lag_no_partition():
    sheet = MagicMock()
    # Mock columns
    col_a = MagicMock()
    col_a.name = 'a'
    col_a.getTypedValue.side_effect = [1, 2, 3]
    
    sheet.columns = [col_a]
    sheet.column.side_effect = lambda name: col_a if name == 'a' else None
    sheet.rows = [object(), object(), object()]
    sheet.nRows = 3

    spec = WindowSpec('a', 'lag', (1,))
    results = calculate_window_function(sheet, spec)
    assert results == [None, 1, 2]

def test_lead_no_partition():
    sheet = MagicMock()
    col_a = MagicMock()
    col_a.name = 'a'
    col_a.getTypedValue.side_effect = [1, 2, 3]
    
    sheet.columns = [col_a]
    sheet.column.side_effect = lambda name: col_a if name == 'a' else None
    sheet.rows = [object(), object(), object()]
    sheet.nRows = 3

    spec = WindowSpec('a', 'lead', (1,))
    results = calculate_window_function(sheet, spec)
    assert results == [2, 3, None]

def test_moving_average_no_partition():
    sheet = MagicMock()
    col_a = MagicMock()
    col_a.name = 'a'
    col_a.type = int
    col_a.getTypedValue.side_effect = [1, 2, 3, 4]
    
    sheet.columns = [col_a]
    sheet.column.side_effect = lambda name: col_a if name == 'a' else None
    sheet.rows = [object(), object(), object(), object()]
    sheet.nRows = 4

    spec = WindowSpec('a', 'moving_average', (3,))
    results = calculate_window_function(sheet, spec)
    # i=0: [1] -> 1.0
    # i=1: [1, 2] -> 1.5
    # i=2: [1, 2, 3] -> 2.0
    # i=3: [2, 3, 4] -> 3.0
    assert results == [1.0, 1.5, 2.0, 3.0]

def test_partitioning_and_ordering():
    sheet = MagicMock()
    col_v = MagicMock(); col_v.name = 'v'
    col_p = MagicMock(); col_p.name = 'p'
    col_o = MagicMock(); col_o.name = 'o'
    
    # Rows:
    # row0: p='x', o=1, v=10
    # row1: p='x', o=2, v=20
    # row2: p='y', o=1, v=100
    
    rows = [object(), object(), object()]
    def get_typed_val(row, col):
        if col == col_p:
            return 'x' if row in (rows[0], rows[1]) else 'y'
        if col == col_o:
            if row == rows[0]: return 1
            if row == rows[1]: return 2
            if row == rows[2]: return 1
        if col == col_v:
            if row == rows[0]: return 10
            if row == rows[1]: return 20
            if row == rows[2]: return 100
        return None

    col_p.getTypedValue.side_effect = lambda r: get_typed_val(r, col_p)
    col_o.getTypedValue.side_effect = lambda r: get_typed_val(r, col_o)
    col_v.getTypedValue.side_effect = lambda r: get_typed_val(r, col_v)

    sheet.columns = [col_v, col_p, col_o]
    sheet.column.side_effect = lambda name: {'v': col_v, 'p': col_p, 'o': col_o}.get(name)
    sheet.rows = rows
    sheet.nRows = 3

    # Lag(1) with partition by 'p' order by 'o'
    spec = WindowSpec('v', 'lag', (1,)).partition_by('p').order_by('o')
    results = calculate_window_function(sheet, spec)
    # Partition 'x': (o=1, v=10), (o=2, v=20) -> lag: None, 10
    # Partition 'y': (o=1, v=100) -> lag: None
    assert results[0] == None  # row0

def test_descending_ordering():
    sheet = MagicMock()
    col_v = MagicMock(); col_v.name = 'v'
    col_o = MagicMock(); col_o.name = 'o'
    
    rows = [object(), object()]
    # row0: o=1, v=10
    # row1: o=2, v=20
    
    def get_typed_val(row, col):
        if col == col_o:
            return 1 if row == rows[0] else 2
        if col == col_v:
            return 10 if row == rows[0] else 20
        return None

    col_o.getTypedValue.side_effect = lambda r: get_typed_val(r, col_o)
    col_v.getTypedValue.side_effect = lambda r: get_typed_val(r, col_v)

    sheet.columns = [col_v, col_o]
    sheet.column.side_effect = lambda name: {'v': col_v, 'o': col_o}.get(name)
    sheet.rows = rows
    sheet.nRows = 2

    # Lag(1) with order by 'o' desc=True
    # Ordered should be (o=2, v=20), (o=1, v=10)
    # lag(1) for (o=2, v=20) is None
    # lag(1) for (o=1, v=10) is 20
    spec = WindowSpec('v', 'lag', (1,)).order_by('o', desc=True)
    results = calculate_window_function(sheet, spec)
    assert results[0] == 20  # row0 (o=1)
    assert results[1] == None # row1 (o=2)
