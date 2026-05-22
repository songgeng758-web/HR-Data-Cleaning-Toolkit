import pandas as pd

df = pd.read_excel('01人员信息主集.xlsx', skiprows=[1])
print('清洗前：', df.shape)

# axis=1 表示按"列"操作；how='all' 表示整列都为空才删
df = df.dropna(axis=1, how='all')

# 遍历所有文本列，去掉首尾空格
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].astype(str).str.strip().replace({'nan': None})

# 姓名特殊处理：把名字中间的空格也去掉
df['姓名'] = df['姓名'].str.replace(r'\s+', '', regex=True)

# 把无效值 '3' 和 '未知' 统一变成空值（None）
df['性别'] = df['性别'].replace({'3': None, '未知': None})

# errors='coerce' 表示转不了的（比如格式乱的）就变成空值，不会报错中断
for col in ['参加工作时间', '入职日期', '任职生效时间']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

df['数据问题'] = ''
df.loc[df['证件号'].isna(), '数据问题'] += '证件号缺失;'
df.loc[df['入职日期'].isna(), '数据问题'] += '入职日期缺失;'

# 找出证件号重复的行
dup = df['证件号'].notna() & df['证件号'].duplicated(keep=False)
df.loc[dup, '数据问题'] += '证件号重复;'

print('清洗后：', df.shape)
print('有问题的行数：', (df['数据问题'] != '').sum())

df.to_excel('人员信息_已清洗.xlsx', index=False)
print('已保存到 人员信息_已清洗.xlsx')