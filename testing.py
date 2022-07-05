import re
import pandas as pd
import numpy as np

df = pd.read_csv('data/keycult.csv')

print(df.get('links').iloc[0])

#print(df.get('contents').iloc[79])
#print('\n\n\n\n\n\n\n')
#print(df.get('cleaned').iloc[79])

#st = 'https://imgur.com/a/0cRbhuD'

#out = re.findall(r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', st)
#print(out)

#print(re.findall(r'\[[a-zA-Z-]+\]', df.get('title').iloc[1]))

#works for getting location from title
#print(re.findall(r'\[(.*?)\]', df.get('title').iloc[1]))

#works for getting have content from title
#print(re.findall(r'W\](.*)', df.get('title').iloc[1])[0].strip())
