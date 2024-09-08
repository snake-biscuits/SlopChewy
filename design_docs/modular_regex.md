# Modular Regex

Common (simple) patterns will occur in many complex patterns
e.g. `[A-Z]+[0-9]+` Cell, `<Cell>:<Cell>` CellRange
`=@avg(A1:C3)/C4`

It'd be nice to have some abstract base class for parsing the complex patterns


## Previous Design

I came up with an idea for tackling this when I made `bsp_tool.extensions.editor`
However, that approach has a lot of ugly subclass systems & wierd wrappers

A class-based appoach is nice for bundling methods
 * `str -> object`
 * `object -> str`
 * validate `str`
 * validate `object`

But calling `__init__` every time we parse create a huge amount of overhead
The worst offender is likely re-compiling the regex every time

Doing regex compiles up-front would be far nicer
Though not every regex


### Improvements

 * cache each regex pattern after it's first compile
   + "only pay for what you use"
   - would require the use of a singleton



## Design Goals

 * readability
   - `"keyword ARG_1 ARG_2"` abstract form
   - `{"ARG_1": [TypeA, TypeB], "ARG_2": [TypeC]}` sub-member types
 * performance
   - parse fast
   - low memory footprint (use generators / list comprehension)


## Realisation

we're essentially just trying to make [YACC](https://en.wikipedia.org/wiki/Yacc)
but it only parses one line at a time
and updates an object's state w/ each line
or creates a child object

baby's first assembly language / turing machine
iirc there was a dr brain minigame like this
wrote a routine + 2 subroutines to move a little guy around
kinda line that one zactronics game (TIS-100? never played it)
