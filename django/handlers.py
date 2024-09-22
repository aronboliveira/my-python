import re
from django.db import models

def clean_email(email: str) -> str:
		if "@" not in email:
				email = email[:email.rfind(".")] + "@" + email[email.rfind("."):]
		return email
def normalize_name(name: str) -> str:
  name = re.sub(r"[^\s\-'a-zA-Z\u00C0-\u017F\u0600-\u06FF]", "", name).replace("_", " ")
  if not name:
    name = 'undefined'
  return name
def undefine_falsish(value:str) -> str:
  if not value or value == '' or value == None:
    return 'undefined'
def null_falsish(value:str) -> str:
  if not value or value == '' or value == None:
    return 'null'
def none_falsish(value:str) -> None:
  if not value or value == '' or value.lower() == 'null' or value.lower() == 'undefined' or value.lower() == 'null':
    return None
def zero_falsish(value:str) -> str:
  if not value or value == '' or value == 0:
    return '0'
def zero_falsish_int(value:str) -> int:
  if not value or value == '' or value == '0':
    return 0
def false_falsish(value:str) -> bool:
  if not value or value == '' or value.lower() == 'false':
    return False
def extract_count_data(data) -> int:
  count = 0
  for k in data.keys():
    if k.startswith('trat_'):
      count += 1
  return count
def add_dynamic_fields(cls, field_prefix, count, field_type=models.CharField, **kwargs) -> None:
    for i in range(1, count + 1):
        field_name = f'{field_prefix}_{i}'
        if not hasattr(cls, field_name):
            cls.add_to_class(field_name, field_type(**kwargs))