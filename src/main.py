import json
import datetime
import logging
import pandas as pd
import re

list = ["Елена А.", "машина", "123 кот."]

pattern = r"\b[А-Я][а-я]+\s[А-Я]\."
t = [word for word in list if re.match(pattern, word)]

print(t)
