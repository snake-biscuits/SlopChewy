## Commandable base class

### command decorator

```python
@command(regex: str)
def command_name(self, *args: List[str]):
    ...
```

 * add regex & `command_name` method to **class'** `_commands` dict
  - `{re.compile(pattern): method}`


### run method 

```python
run(self, command: str):
    for regex in self._commands:
        match = regex.match(command)
        if match is not None:
            # run the method that implements this command
            method_name = self._commands[regex]
            method = getattr(self, method_name)
            args = match.groups()
            method(*args)
```
