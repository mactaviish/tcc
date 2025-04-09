import unicodedata
import re

def clean_string(s: str) -> str:
  s = unicodedata.normalize('NFKD', s)
  s = s.encode('ASCII', 'ignore').decode('utf-8')
  s = re.sub(r'[^a-zA-Z0-9_ ]', '', s)
  return s.strip().lower().replace(" ", "_")
