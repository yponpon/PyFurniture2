##讀取Json資料轉入Pandas
import pandas as pd
import numpy as np
import json

file_path = './Json_save/Json_save.json'

pd.set_option('display.max_columns', None) #顯示所有columns
pd.set_option('display.max_rows', None) #顯示所有rows

with open(file_path,'r') as f:
    dict_data = json.load(f)

#定義dataframe columns
dtypes = np.dtype([
          ('file', str),
          ('Style', str),
          ])
data = np.empty(0, dtype=dtypes)
df = pd.DataFrame(data)
# print(df.columns)

#loop at key
for key in sorted(dict_data):
    # print(key,dict_data[key]) #顯示key/value
    for i in dict_data[key]:
        if i in df.columns: #若column 存在dataframe
            continue
        else:
            df[i] = ''
        df = df.append(dict_data[key],ignore_index=True)

print(df.head())

df.to_csv('./output.csv',encoding='utf-8',index=True)