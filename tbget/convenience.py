from .extraction import extract, extract_from_string
from .formatting import format_traceback


def extract_traceback(file_obj):
	extracted = extract(file_obj)
	if extracted is None:
		return None

	return format_traceback(*extracted)


def extract_traceback_from_string(text):
	extracted = extract_from_string(text)
	if extracted is None:
		return None

	return format_traceback(*extracted)
