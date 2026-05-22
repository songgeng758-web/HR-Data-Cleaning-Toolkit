import pandas as pd

# skiprows=[1] 表示跳过第 2 行（那行是填表说明，不是数据）
df = pd.read_excel('01人员信息主集.xlsx', skiprows=[1])

print('行数和列数：', df.shape)        # 看规模
print(df.head())                       # 看前 5 行长啥样
print(df.isna().sum())                 # 看每列缺多少值