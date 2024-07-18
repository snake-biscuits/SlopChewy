from typing import Any, Dict, List, Tuple, Union


JsonSheet = Dict[str, Union[List[str], Tuple[Any]]]
# ^ {"columns": ["A", "B"], "values": [("A value", b_value)]}


JsonSpreadSheet = Dict[str, JsonSheet]
# ^ {"sheet name": ...}
