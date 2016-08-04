# tbget

`tbget` is a simple tool for extracting tracebacks from any text.

Here's an example traceback that has been encoded and word wrapped in a few ways before it got to me (I've actually cut most of the stack frames to keep it short).

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

If I run that through `tbget`, I get this:

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

Much more readable!!

For those curious about the extra nonsense at the end... Unfortunately figuring out when the exception's message ends is seemingly impossible, so the tool just prints out 100 characters after the last stack frame.
