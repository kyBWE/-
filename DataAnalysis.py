import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取并预处理数据
df=pd.read_csv('2024胡润百富榜.csv')
df['财富值(亿)']=df['财富值'].str.replace('亿', '').astype(float)
df['行业列表']=df['行业'].str.split('、')
df['年龄']=pd.to_numeric(df['年龄'],errors='coerce')

# 通用绘图函数
def draw(data,x,y,title,xlabel,ylabel,fmt='{:.0f}'):
    plt.figure(figsize=(15,8))
    ax=sns.barplot(data=data,x=x,y=y)
    plt.title(title,fontsize=15)
    plt.xlabel(xlabel,fontsize=12)
    plt.ylabel(ylabel,fontsize=12)
    for p in ax.patches:
        width=p.get_width()
        plt.text(width,p.get_y()+p.get_height()/2, 
                 fmt.format(width),ha='left',va='center',fontsize=10)
    plt.tight_layout()
    plt.show()

# 1.富豪数量最多的行业
cnt=Counter()
for i in df['行业列表']:
    cnt.update(i)
df1=pd.DataFrame(cnt.items(),columns=['行业','富豪数量']).sort_values('富豪数量',ascending=False)
draw(df1.head(20),'富豪数量','行业','富豪数量最多的前20个行业','富豪数量','行业')

# 2.总财富值最高的行业
df2=df.explode('行业列表').groupby('行业列表')['财富值(亿)'].sum().reset_index().sort_values('财富值(亿)',ascending=False)
draw(df2.head(20),'财富值(亿)','行业列表','总财富值最高的前20个行业','总财富(亿)','行业','{:.0f}亿')

# 3.总财富值最高的行业及平均年龄
df3=df.explode('行业列表').groupby('行业列表').agg(
    总财富=('财富值(亿)','sum'),
    平均年龄=('年龄','mean'),
    富豪数量=('姓名（中文）','count')
).reset_index().sort_values('总财富',ascending=False)
df3['平均财富']=df3['总财富']/df3['富豪数量']
plt.figure(figsize=(15,8))
ax=sns.barplot(data=df3.head(20),x='总财富',y='行业列表')
for i,p in enumerate(ax.patches):
    width=p.get_width()
    age=df3.head(20).iloc[i]['平均年龄']
    plt.text(width,p.get_y()+p.get_height()/2, 
             f'{int(width)}亿\n(平均年龄:{age:.1f}岁)',ha='left',va='center',fontsize=10)
plt.title('总财富最高的前20个行业及平均年龄',fontsize=15)
plt.xlabel('总财富(亿)',fontsize=12)
plt.ylabel('行业',fontsize=12)
plt.tight_layout()
plt.show()

# 4.平均财富最高的行业
df4=df3.sort_values('平均财富',ascending=False)
draw(df4.head(20),'平均财富','行业列表','平均财富最高的前20个行业','平均财富(亿)','行业','{:.1f}亿')

# 5.平均财富最高的行业及平均年龄
plt.figure(figsize=(15, 8))
ax=sns.barplot(data=df4.head(20),x='平均财富',y='行业列表')
for i,p in enumerate(ax.patches):
    width=p.get_width()
    age=df4.head(20).iloc[i]['平均年龄']
    plt.text(width,p.get_y()+p.get_height()/2, 
             f'{int(width)}亿\n(平均年龄:{age:.1f}岁)',ha='left',va='center',fontsize=10)
plt.title('平均财富最高的前20个行业及平均年龄',fontsize=15)
plt.xlabel('平均财富(亿)',fontsize=12)
plt.ylabel('行业',fontsize=12)
plt.tight_layout()
plt.show()

# 6.富豪的年龄分布
df['年龄分组'] = pd.cut(df['年龄'], bins=[0,30,40,50,60,70,80,90,100],
                    labels=['30岁以下','30-39岁','40-49岁','50-59岁','60-69岁','70-79岁','80-89岁','90岁以上'])
Ages=df['年龄分组'].value_counts().sort_index()
plt.figure(figsize=(12,6))
ax=Ages.plot(kind='bar')
for i,v in enumerate(Ages):
    ax.text(i,v,f'{v}人',ha='center',fontsize=10)
plt.title('富豪年龄分布',fontsize=15)
plt.xlabel('年龄段',fontsize=12)
plt.ylabel('人数',fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 6.富豪的性别分布
Sex=df['性别'].value_counts()
plt.figure(figsize=(8,8))
plt.pie(Sex,labels=[f'{k}({v}人,{v/Sex.sum()*100:.1f}%)' for k,v in Sex.items()],autopct='%1.1f%%')
plt.title('富豪性别分布',fontsize=15)
plt.show()

# 7.富豪的出生地分布
Birthplace=df['出生地'].value_counts().head(20)
plt.figure(figsize=(15,6))
ax=Birthplace.plot(kind='bar')
for i,v in enumerate(Birthplace):
    ax.text(i,v,str(v),ha='center')
plt.title('富豪出生地分布(前20)',fontsize=15)
plt.xlabel('出生地',fontsize=12)
plt.ylabel('人数',fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
