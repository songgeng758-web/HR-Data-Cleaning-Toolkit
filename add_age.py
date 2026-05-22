import pandas as pd

# 1. 读入已清洗的表
df = pd.read_excel('人员信息_已清洗.xlsx')

# 2. 筛出合法的 18 位身份证
s = df['证件号'].astype(str).str.strip()
is_id = (df['证件类型'].astype(str).str.strip() == '身份证') & \
        s.str.match(r'^\d{17}[\dXx]$')

# 3. 反推出生日期（第 7~14 位）
birth_raw = s.where(is_id).str[6:14]
df['出生日期'] = pd.to_datetime(birth_raw, format='%Y%m%d', errors='coerce')

# 4. 计算年龄
today = pd.Timestamp('today').normalize()
df['年龄'] = ((today - df['出生日期']).dt.days / 365.25).round().astype('Int64')

# 5. 用第 17 位校验性别
digit17 = s.where(is_id).str[16]
id_gender = digit17.dropna().astype(int).map(lambda x: '男' if x % 2 == 1 else '女')
id_gender = id_gender.reindex(df.index)
cur_gender = df['性别'].astype(str).str.strip()
df['性别校验'] = ''
mismatch = id_gender.notna() & cur_gender.isin(['男', '女']) & (id_gender != cur_gender)
df.loc[mismatch, '性别校验'] = '与身份证不符'

# 6. 把出生日期、年龄移到"性别"后面
b, a = df.pop('出生日期'), df.pop('年龄')
idx = df.columns.get_loc('性别') + 1
df.insert(idx, '出生日期', b)
df.insert(idx + 1, '年龄', a)

# 7. 保存
df.to_excel('人员信息_已清洗_含年龄.xlsx', index=False)
print('完成')
print('  总行数:', len(df))
print('  成功反推年龄:', df['年龄'].notna().sum(), '条')
print('  性别与身份证不符:', mismatch.sum(), '条')