import StringIO

def format_traceback(frames, remainder, num_trailing=100):
    result = StringIO.StringIO()

    print >> result, u"Traceback (most recent call last):"
    for header, snippet in frames:
        print >> result, u" " * 2 + unicode(header)
        if snippet:
            print >> result, u" " * 4 + snippet

    print >> result, remainder[:num_trailing].strip(),

    if len(remainder) > num_trailing:
        print >> result, u"...",

    return result.getvalue()
