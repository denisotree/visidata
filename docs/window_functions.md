# Window Functions in VisiData-NG

The Window Functions feature allows you to perform calculations across a set of rows related to the current row.

## Syntax

Expressions are entered using a dot-notation DSL:

`column.function(args).partition_by(columns).order_by(columns, desc=False)`

## Available Functions

| Function | Description |
| :--- | :--- |
| `lag(n=1)` | Returns the value of `column` from `n` rows *before* the current row. |
| `lead(n=1)` | Returns the value of `column` from `n` rows *after* the current row. |
| `moving_average(n=3)` | Returns the trailing average of the last `n` values (including current). |

## Modifiers

- `partition_by('col1', 'col2', ...)`: Resets calculations at the boundaries of the specified columns.
- `order_by('col1', desc=True)`: Sets the sort order within each partition.

## Examples

- **Previous day's price**:
  `price.lag(1).order_by('date')`
- **7-day moving average per store**:
  `sales.moving_average(7).partition_by('store_id').order_by('date')`
- **Next rank (descending)**:
  `score.lead(1).order_by('score', desc=True)`

## Usage Notes

- Calculations are performed on a snapshot of the current sheet.
- The resulting column is a static column with pre-calculated values.
- If no partition/order is specified, the current sheet's row order is used.
