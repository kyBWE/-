
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv('2024胡润百富榜.csv')

# 移除"亿"字并转换为数值
df['财富值(亿)'] = df['财富值'].str.replace('亿', '').astype(float)

# 分割多个行业
df['行业列表'] = df['行业'].str.split('、')

industry_counter = Counter()
for industries in df['行业列表'].dropna():
    industry_counter.update(industries)
# 转换为DataFrame
industry_df = pd.DataFrame.from_dict(industry_counter, orient='index', columns=['富豪数量']).reset_index()
industry_df = industry_df.rename(columns={'index': '行业'})
industry_df = industry_df.sort_values('富豪数量', ascending=False)
# 绘制前20行业富豪数量柱状图
plt.figure(figsize=(12, 8))
ax = sns.barplot(data=industry_df.head(20), x='富豪数量', y='行业')
plt.title('富豪数量最多的前20个行业', fontsize=15)
plt.xlabel('富豪数量', fontsize=12)
plt.ylabel('行业', fontsize=12)
# 添加数据标签
for p in ax.patches:
    width = p.get_width()
    plt.text(width + 1, p.get_y() + p.get_height()/2, 
             f'{int(width)}', 
             ha='left', va='center', fontsize=10)
plt.tight_layout()
plt.show()

# 计算各行业总财富
industry_wealth = {}
for idx, row in df.iterrows():
    if isinstance(row['行业列表'], list):
        for industry in row['行业列表']:
            if industry not in industry_wealth:
                industry_wealth[industry] = 0
            industry_wealth[industry] += row['财富值(亿)']
# 转换为DataFrame并排序
industry_wealth_df = pd.DataFrame.from_dict(industry_wealth, orient='index', columns=['总财富(亿)']).reset_index()
industry_wealth_df = industry_wealth_df.rename(columns={'index': '行业'})
industry_wealth_df = industry_wealth_df.sort_values('总财富(亿)', ascending=False)
# 绘制前20行业总财富柱状图
plt.figure(figsize=(12, 8))
ax = sns.barplot(data=industry_wealth_df.head(20), x='总财富(亿)', y='行业')
plt.title('总财富最高的前20个行业', fontsize=15)
plt.xlabel('总财富(亿)', fontsize=12)
plt.ylabel('行业', fontsize=12)
# 添加数据标签
for p in ax.patches:
    width = p.get_width()
    plt.text(width + 50, p.get_y() + p.get_height()/2, 
             f'{int(width)}亿', 
             ha='left', va='center', fontsize=10)
plt.tight_layout()
plt.show()

# 计算各行业总财富和平均年龄
# 确保列是数值类型
df['财富值(亿)'] = pd.to_numeric(df['财富值(亿)'], errors='coerce')  # 非数字转为NaN
df['年龄'] = pd.to_numeric(df['年龄'], errors='coerce')
df = df.dropna(subset=['财富值(亿)', '年龄'])
# 计算各行业总财富和平均年龄
industry_wealth = {}
industry_age_count = {}  # 存储年龄总和和人数
for idx, row in df.iterrows():
    if isinstance(row['行业列表'], list):
        for industry in row['行业列表']:
            # 初始化行业数据
            if industry not in industry_wealth:
                industry_wealth[industry] = 0
                industry_age_count[industry] = {'total_age': 0, 'count': 0}
            
            # 确保值是数字类型
            wealth = row['财富值(亿)']
            age = row['年龄']
            
            # 累加财富和年龄信息
            industry_wealth[industry] += float(wealth) if not pd.isna(wealth) else 0
            industry_age_count[industry]['total_age'] += float(age) if not pd.isna(age) else 0
            industry_age_count[industry]['count'] += 1 if not pd.isna(age) else 0
# 转换为DataFrame
industry_wealth_df = pd.DataFrame.from_dict(industry_wealth, orient='index', columns=['总财富(亿)']).reset_index()
industry_wealth_df = industry_wealth_df.rename(columns={'index': '行业'})
# 计算平均年龄
avg_age = {}
for industry, data in industry_age_count.items():
    if data['count'] > 0:  # 避免除以零
        avg_age[industry] = data['total_age'] / data['count']
    else:
        avg_age[industry] = 0
avg_age_df = pd.DataFrame.from_dict(avg_age, orient='index', columns=['平均年龄']).reset_index()
avg_age_df = avg_age_df.rename(columns={'index': '行业'})
# 合并数据
result_df = pd.merge(industry_wealth_df, avg_age_df, on='行业')
result_df = result_df.sort_values('总财富(亿)', ascending=False)
plt.figure(figsize=(14, 8))
ax = sns.barplot(data=result_df.head(20), x='总财富(亿)', y='行业')
# 添加标签
for i, p in enumerate(ax.patches):
    width = p.get_width()
    age = result_df.head(20).iloc[i]['平均年龄']
    plt.text(width + 50, p.get_y() + p.get_height()/2, 
             f'{int(width)}亿\n(平均年龄: {age:.1f}岁)', 
             ha='left', va='center', fontsize=10)
plt.title('总财富最高的前20个行业及平均年龄', fontsize=15)
plt.xlabel('总财富(亿)', fontsize=12)
plt.ylabel('行业', fontsize=12)
plt.tight_layout()
plt.show()

# 计算行业平均财富
industry_avg_wealth = industry_wealth_df.merge(industry_df, on='行业')
industry_avg_wealth['平均财富(亿)'] = industry_avg_wealth['总财富(亿)'] / industry_avg_wealth['富豪数量']
industry_avg_wealth = industry_avg_wealth.sort_values('平均财富(亿)', ascending=False)
# 绘制前20行业平均财富柱状图
plt.figure(figsize=(12, 8))
ax = sns.barplot(data=industry_avg_wealth.head(20), x='平均财富(亿)', y='行业')
plt.title('平均财富最高的前20个行业', fontsize=15)
plt.xlabel('平均财富(亿)', fontsize=12)
plt.ylabel('行业', fontsize=12)
# 添加数据标签
for p in ax.patches:
    width = p.get_width()
    plt.text(width + 2, p.get_y() + p.get_height()/2, 
             f'{width:.1f}亿', 
             ha='left', va='center', fontsize=10)
plt.tight_layout()
plt.show()

# 计算行业平均财富和富豪平均年龄
industry_avg_wealth = industry_wealth_df.merge(industry_df, on='行业')
industry_avg_wealth['平均财富(亿)'] = industry_avg_wealth['总财富(亿)'] / industry_avg_wealth['富豪数量']
# 合并平均年龄数据
industry_avg_wealth = industry_avg_wealth.merge(avg_age_df, on='行业')
# 按平均财富排序
industry_avg_wealth = industry_avg_wealth.sort_values('平均财富(亿)', ascending=False)
# 绘制前20行业平均财富柱状图（带平均年龄）
plt.figure(figsize=(14, 8))
ax = sns.barplot(data=industry_avg_wealth.head(20), x='平均财富(亿)', y='行业')
# 添加数据标签（同时显示平均财富和平均年龄）
for i, p in enumerate(ax.patches):
    width = p.get_width()
    age = industry_avg_wealth.head(20).iloc[i]['平均年龄']
    plt.text(width + 2, p.get_y() + p.get_height()/2, 
             f'{width:.1f}亿\n(平均年龄: {age:.1f}岁)', 
             ha='left', va='center', fontsize=10)
plt.title('平均财富最高的前20个行业及平均年龄', fontsize=15)
plt.xlabel('平均财富(亿)', fontsize=12)
plt.ylabel('行业', fontsize=12)
plt.tight_layout()
plt.show()

# 年龄分布
df['年龄'] = pd.to_numeric(df['年龄'], errors='coerce')
# 创建年龄分组
bins = [0, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ['30岁以下', '30-39岁', '40-49岁', '50-59岁', '60-69岁', '70-79岁', '80-89岁', '90岁以上']
df['年龄分组'] = pd.cut(df['年龄'], bins=bins, labels=labels)
# 绘制年龄分布图
plt.figure(figsize=(12, 6))
age_dist = df['年龄分组'].value_counts().sort_index()
ax = age_dist.plot(kind='bar')
# 添加数据标签
for i, v in enumerate(age_dist):
    ax.text(i, v + 5, f'{v}人', ha='center', fontsize=10)
plt.title('富豪年龄分布', fontsize=15)
plt.xlabel('年龄段', fontsize=12)
plt.ylabel('人数', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 性别分布
gender_dist = df['性别'].value_counts()
gender_pct = df['性别'].value_counts(normalize=True) * 100
plt.figure(figsize=(8, 8))
patches, texts, autotexts = plt.pie(
    gender_dist, 
    labels=[f'{label} ({count}人, {pct:.1f}%)' 
           for label, count, pct in zip(gender_dist.index, gender_dist, gender_pct)],
    autopct='%1.1f%%',
    startangle=90
)
plt.title('富豪性别分布', fontsize=15)
plt.show()

# 出生地分布
birthplace_dist = df['出生地'].value_counts().head(20)
plt.figure(figsize=(12, 6))
ax = birthplace_dist.plot(kind='bar')
plt.title('富豪出生地分布(前20)', fontsize=15)
plt.xlabel('出生地', fontsize=12)
plt.ylabel('人数', fontsize=12)
plt.xticks(rotation=45)
# 添加数据标签
for i, v in enumerate(birthplace_dist):
    ax.text(i, v + 2, str(v), ha='center')
plt.tight_layout()
plt.show()

