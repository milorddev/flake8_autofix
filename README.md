## Flake8 AutoFix

This script automagically fixes simple flake8 linting errors and warnings

The script in action:

![flake8_autofix_in_action](https://media.discordapp.net/attachments/564872937455484928/605790338451243058/autolintfix.gif)


### How to use the script

All you have to do is run this script in the directory you want to lint/fix

If you drop the script in the same folder as your project

Example:
```
home/name/projectfolder > python3 flake8_autofix.py
```

Or if you have the script live somewhere else

Example:
```
home/name/projectfolder > python3 ../scripts/flake8_autofix.py
```


Whatever directory your terminal is on, is the one this script will autolint/fix

### What this script can Autofix

The plan is to have the simple stuff covered by this script. There is no intention to fully autofix everything.
Some of these codes simply require developer attention. Below are the codes this script does correct automatically.

If you would like to help make this list more complete, create a pull request! Your help is appreciated.


| Code | Message                                                              | Can AutoFix |
|------|----------------------------------------------------------------------|:-----------:|
| E101 | indentation contains mixed spaces and tabs                           |             |
| E111 | indentation is not a multiple of four                                |             |
| E112 | expected an indented block                                           |             |
| E113 | unexpected indentation                                               |             |
| E114 | indentation is not a multiple of four (comment)                      |             |
| E115 | expected an indented block (comment)                                 |             |
| E116 | unexpected indentation (comment)                                     |             |
| E117 | over-indented                                                        |             |
| E121 | continuation line under-indented for hanging indent                  |             |
| E122 | continuation line missing indentation or outdented                   |             |
| E123 | closing bracket does not match indentation of opening bracket’s line |             |
| E124 | closing bracket does not match visual indentation                    |             |
| E125 | continuation line with same indent as next logical line              |             |
| E126 | continuation line over-indented for hanging indent                   |             |
| E127 | continuation line over-indented for visual indent                    |             |
| E128 | continuation line under-indented for visual indent                   |             |
| E129 | visually indented line with same indent as next logical line         |             |
| E131 | continuation line unaligned for hanging indent                       |             |
| E133 | closing bracket is missing indentation                               |             |
| E201 | whitespace after ‘(‘                                                 |      X      |
| E202 | whitespace before ‘)’                                                |      X      |
| E203 | whitespace before ‘:’                                                |      X      |
| E211 | whitespace before ‘(‘                                                |      X      |
| E221 | multiple spaces before operator                                      |      X      |
| E222 | multiple spaces after operator                                       |      X      |
| E223 | tab before operator                                                  |             |
| E224 | tab after operator                                                   |             |
| E225 | missing whitespace around operator                                   |      X      |
| E226 | missing whitespace around arithmetic operator                        |             |
| E227 | missing whitespace around bitwise or shift operator                  |             |
| E228 | missing whitespace around modulo operator                            |             |
| E231 | missing whitespace after ‘,’, ‘;’, or ‘:’                            |      X      |
| E241 | multiple spaces after ‘,’                                            |             |
| E242 | tab after ‘,’                                                        |             |
| E251 | unexpected spaces around keyword / parameter equals                  |      X      |
| E252 | missing whitespace around parameter equals                           |      X      |
| E261 | at least two spaces before inline comment                            |      X      |
| E262 | inline comment should start with ‘# ‘                                |      X      |
| E265 | block comment should start with ‘# ‘                                 |      X      |
| E266 | too many leading ‘#’ for block comment                               |      X      |
| E271 | multiple spaces after keyword                                        |             |
| E272 | multiple spaces before keyword                                       |      X      |
| E273 | tab after keyword                                                    |             |
| E274 | tab before keyword                                                   |             |
| E275 | missing whitespace after keyword                                     |             |
| E301 | expected 1 blank line, found 0                                       |             |
| E302 | expected 2 blank lines, found 0                                      |      X      |
| E303 | too many blank lines (3)                                             |      X      |
| E304 | blank lines found after function decorator                           |             |
| E305 | expected 2 blank lines after end of function or class                |      X      |
| E306 | expected 1 blank line before a nested definition                     |             |
| E401 | multiple imports on one line                                         |             |
| E402 | module level import not at top of file                               |             |
| E501 | line too long (82 > 79 characters)                                   |             |
| E502 | the backslash is redundant between brackets                          |             |
| E701 | multiple statements on one line (colon)                              |             |
| E702 | multiple statements on one line (semicolon)                          |             |
| E703 | statement ends with a semicolon                                      |      X      |
| E704 | multiple statements on one line (def)                                |             |
| E711 | comparison to None should be ‘if cond is None:’                      |             |
| E712 | comparison to True should be ‘if cond is True:’ or ‘if cond:’        |             |
| E713 | test for membership should be ‘not in’                               |             |
| E714 | test for object identity should be ‘is not’                          |             |
| E721 | do not compare types, use ‘isinstance()’                             |             |
| E722 | do not use bare except, specify exception instead                    |             |
| E731 | do not assign a lambda expression, use a def                         |             |
| E741 | do not use variables named ‘l’, ‘O’, or ‘I’                          |             |
| E742 | do not define classes named ‘l’, ‘O’, or ‘I’                         |             |
| E743 | do not define functions named ‘l’, ‘O’, or ‘I’                       |             |
| E901 | SyntaxError or IndentationError                                      |             |
| E902 | IOError                                                              |             |
| W191 | indentation contains tabs                                            |      X      |
| W291 | trailing whitespace                                                  |      X      |
| W292 | no newline at end of file                                            |      X      |
| W293 | blank line contains whitespace                                       |      X      |
| W391 | blank line at end of file                                            |      X      |
| W503 | line break before binary operator                                    |             |
| W504 | line break after binary operator                                     |             |
| W505 | doc line too long (82 > 79 characters)                               |             |
| W601 | .has_key() is deprecated, use ‘in’                                   |             |
| W602 | deprecated form of raising exception                                 |             |
| W603 | ‘<>’ is deprecated, use ‘!=’                                         |             |
| W604 | backticks are deprecated, use ‘repr()’                               |             |
| W605 | invalid escape sequence ‘x’                                          |             |
| W606 | ‘async’ and ‘await’ are reserved keywords starting with Python 3.7   |             |
| F401 | module imported but unused                                           |      X      |
| F402 | import module from line N shadowed by loop variable                  |             |
| F403 | ‘from module import *’ used; unable to detect undefined names        |             |
| F404 | future import(s) name after other statements                         |             |
| F811 | redefinition of unused name from line N                              |             |
| F812 | list comprehension redefines name from line N                        |             |
| F821 | undefined name name                                                  |             |
| F822 | undefined name name in __all__                                       |             |
| F823 | local variable name ... referenced before assignment                 |             |
| F831 | duplicate argument name in function definition                       |             |
| F841 | local variable name is assigned to but never used                    |             |

