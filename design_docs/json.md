# `.json` spreadsheet form

would make a nice basis for a generic python object form
> maybe a `Selection` object?


## Example

```json
[
  {
    "sheet name": {
      "columns": ["A", "B"],
      "values": [
        ["some text", 123.45],
        ["more text", 678.90]]
  }
]
```

> NOTE: column names should occupy the top row.
> unless "columns" is None, in which case "values" begin at row 0


### Design Flaws

 * storing each row as a list of cells could get messy for large gaps
   - it might be better to identify discrete blocks for better packing

```json
"sheet name": {
  "A1:C3": {
    "columns": [...],
    "values": [
        [...]]
  }
}
```

 * cells with both text and numerical data
   - type encoding in general seems difficult
 * formulae
   - freeze results? (could be an option when converting)
