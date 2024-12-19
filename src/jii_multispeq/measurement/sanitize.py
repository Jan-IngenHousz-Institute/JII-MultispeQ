import re

from jii_multispeq.constants import REGEX_NIL_NAN

def sanitize( data ):
  """
  Sanitize a string from the MultispeQ instrument
  so it can be parsed by the json encoder.

  :param input: Input String
  :type input: str

  :return: Sanitized String 
  :rtype: str
  """

  ## Replace single quotes with double quotes
  data = re.sub(r"(?<!\\)'", '"', data)

  # TODO: check if there are cases with single quotes inside a value


  ## Replace nil and NAN
  def replace_value(match):
    if match.group(1).lower() == 'nil':
        return 'null'
    else:  # NAN or -NAN
        return 'NaN'

  prog = re.compile( REGEX_NIL_NAN, re.I | re.M)

  data = prog.sub( replace_value, data)

  return data
