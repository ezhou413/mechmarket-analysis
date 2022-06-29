import re
import pandas as pd
import numpy as np

df = pd.read_csv('data/keycult.csv')

print(df.get('contents').iloc[79])

#print(re.findall(r'\[[a-zA-Z-]+\]', df.get('title').iloc[1]))

#works for getting location from title
#print(re.findall(r'\[(.*?)\]', df.get('title').iloc[1]))

#works for getting have content from title
#print(re.findall(r'W\](.*)', df.get('title').iloc[1])[0].strip())
