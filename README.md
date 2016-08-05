# tbget

`tbget` is a tool for extracting tracebacks from garbled text.

Install with `pip install git+https://github.com/brownhead/tbget.git`, run it with `tbget -h`.

## Example Usage

Here's a JSON'd, `repr`'d, and shoved-through-a-word-doc'd traceback:

```
'{"test_data": "{\\"data\\": \\"$ tools/runtests.py \\\\nRUNNING ALL SORTS OF
TESTS\\\\nSTUFF IS PASSING!!\\\\n^CTraceback (most recent call last):\\\\n
File \\\\\\"tools/devshell.py\\\\\\", line 145, in <module>\\\\n    from
devshell_eval import *\\\\n  File
\\\\\\"/Users/johnsullivan/khan/webapp/tools/devshell_eval.py\\\\\\", line 4,
in <module>\\\\n    from assessment_items.models import *\\\\n  File \\\\\\"/U
sers/johnsullivan/.virtualenv/khan27/lib/python2.7/sre_parse.py\\\\\\", line
126, in __len__\\\\n    def
__len__(self):\\\\nKeyboardInterrupt\\\\n$\\\\n\\", \\"type\\":
\\"traceback\\"}", "test_result": "aborted"}'
```

After running it through `tbget`:

```pytb
Traceback (most recent call last):
  File "tools/devshell.py", line 145, in <module>
    from devshell_eval import *
  File "/Users/johnsullivan/khan/webapp/tools/devshell_eval.py", line 4, in <module>
    from assessment_items.models import *
  File "/Users/johnsullivan/.virtualenv/khan27/lib/python2.7/sre_parse.py", line 126, in __len__
    def __len__(self):
KeyboardInterrupt\\\\n$\\\\n\\", \\"type\\":
\\"traceback\\"}", "test_result": "aborted"}'
```

*(Because the traceback's end can't be accurately determined by my tool's general strategy, 100 characters after the last stack frame are printed)*
