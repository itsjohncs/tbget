import collections
import logging
import re as regex

log = logging.getLogger()

class FrameHeaderToken(object):
    FRAME_HEADER_RE = regex.compile(ur"""
        F\s*i\s*\s*l\s*e\s+              # File
        (?P<path>.+?)\s*,\s+             # "/some/file.py",
        l\s*i\s*n\s*e\s+                 # line
        (?P<line_number>[\d\s]+)\s*,\s+  # 78,
        i\s*n\s+                         # in

        # foobar (lambdas use the angle brackets). We don't let function names
        # get split up by whitespace because it makes it too hard to separate the
        # function name from the code snippet. This fortunately ends up being
        # alright because the end of the funtion name will just be tacked onto the
        # beginning of the snippet in this case.
        (?P<function_name>[\w<>_]+)
    """, regex.DOTALL | regex.VERBOSE | regex.UNICODE | regex.IGNORECASE)

    QUOTES_RE_STRING = "(%s)" % "|".join(u"\"''\u201C\u201D\u2018\u201D")
    PATH_CLEAN_RE = regex.compile(ur"""
        ^\s*\\*\s*{quotes}|   # Quote at the beginning
        \\*\s*{quotes}\s*$|  # Quote at the end
        [\r\n]                  # Newlines
    """.format(quotes=QUOTES_RE_STRING), regex.VERBOSE | regex.UNICODE)

    LINE_NUMBER_CLEAN_RE = regex.compile(ur"\D", regex.UNICODE)

    def __init__(self, start, end, path, line_number, function_name):
        self.start = start
        self.end = end
        self.path = path
        self.line_number = line_number
        self.function_name = function_name

    @classmethod
    def clean_path(cls, path):
        """Cleans a path found by the frame header regex.

        We can end up with a variety of pretty funky paths (strange quotation
        marks because of a visit into a word processor, newlines, etc.) so we
        clean the path here.

        We could try to do this in the top-level regex, but no thank you.
        """
        return cls.PATH_CLEAN_RE.sub("", path)

    @classmethod
    def clean_line_number(cls, line_number):
        """Cleans a line number found by the frame header regex.

        I don't expect very many issues to happen with line numbers (besides
        the occaisional hard breaking newline), but we clean them thoroughly
        because it's trivial to do so (we only want decimal numbers).
        """
        return cls.LINE_NUMBER_CLEAN_RE.sub("", line_number)

    @classmethod
    def _from_match(cls, match):
        """Creates a token from a regex match object."""
        return cls(
            start=match.start(),
            end=match.end(),
            path=cls.clean_path(match.group("path")),
            line_number=cls.clean_line_number(match.group("line_number")),
            function_name=match.group("function_name"))

    @classmethod
    def find_all(cls, text):
        """Find all frame headers in some text.

        NOTE(brownhead): I plan for this to return overlapping matches
            eventually, but we'll see how often those occur in practice first.
        """
        return [cls._from_match(i) for i in cls.FRAME_HEADER_RE.finditer(text)]

    def __repr__(self):
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join("%s=%r" % kv for kv in
                      sorted(self.__dict__.iteritems())))

    def __str__(self):
        return u'File "{path}", line {line_number}, in {function_name}'.format(
            **self.__dict__)


def consecutive_pairs(iterable):
    """Yields all consecutive pairs in an iterable.

    >>> list(consecutive_pairs([1, 2, 3, 4, 5]))
    [(1, 2), (2, 3), (3, 4), (4, 5)]
    """
    iterator = iter(iterable)
    a, b = next(iterator), next(iterator)
    while True:
        yield a, b
        a = b
        b = next(iterator)


WRAPPING_RE_RAW = ur"(\s|\\+n|\\+r)"
SNIPPET_CLEAN_RE = regex.compile(ur"""
    ^{wrapping}+ |
    {wrapping}+$
""".format(wrapping=WRAPPING_RE_RAW), regex.VERBOSE | regex.UNICODE)


def clean_snippet(snippet):
    return regex.sub(ur"\s+", " ", SNIPPET_CLEAN_RE.sub("", snippet))


def extract_snippets(frame_headers, text):
    for before, after in consecutive_pairs(frame_headers):
        assert before.end <= after.start
        yield clean_snippet(text[before.end:after.start])


LAST_LINE_RE = regex.compile(ur"""
    (\\n|\\r|\s)+.*\s.*    # Tries to find a snippet

    # This should hopefully be the start of the last line
    (\\n|\\r|\s)+(?P<exception_name>\w+:|KeyboardInterrupt)
""", regex.VERBOSE | regex.UNICODE | regex.DOTALL)

def extract_last_snippet(start_pos, text):
    last_line_match = LAST_LINE_RE.search(text, pos=start_pos)
    if not last_line_match:
        return start_pos, None

    last_line_start = last_line_match.start("exception_name")
    return last_line_start, clean_snippet(text[start_pos:last_line_start])


def extract_from_string(text):
    frame_headers = FrameHeaderToken.find_all(text)
    if not frame_headers:
        return None

    snippets = extract_snippets(frame_headers, text)

    # Create a list of all the stack frames (tuples of the headers, and the
    # snippet text).
    frames = list(zip(frame_headers, snippets))

    # Create the last stack frame (getting the last snippet is a special case,
    # and a tricky one at that).
    remainder_start, last_snippet = (
        extract_last_snippet(frame_headers[-1].end, text))
    frames.append((frame_headers[-1], last_snippet))

    return frames, text[remainder_start:]

def extract(file_obj):
    return extract_from_string(file_obj.read().decode("utf-8"))
