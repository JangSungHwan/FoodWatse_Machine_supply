import numpy as np
import pandas as pd


df1 = pd.read_csv('음식물쓰레기_발생량_추정_정보(2023년_수정).csv', sep = ',')
df2 = pd.read_csv('음식물_쓰레기_처리장비_정보_목록(2021.09).csv', sep = ',')


#총계소각, 총계매립, 총계 기타를 모두 합한 열을 새로 만든다.
#재활용은 제외하는 것으로 한다.
df1['Food Waste Sum']=df1['tot_sum_incnr']+df1['tot_sum_bryng']+df1['tot_sum_etc']

#지역별 총 음식물 쓰레기 합계량을 나타내는 새로운 데이터세트
data_s = df1.groupby(by='signgu_nm')['Food Waste Sum' ].sum().reset_index()


data_s['count'] = 0
'''
#지역이름 부분일치시 카운트   
for i, a in enumerate(data_s['signgu_nm']):
    for j, b in enumerate(df2['city_gn_gu_nm']):
        if a in b:
            data_s['count'][i] += 1   '''      
            
data_s['count'] = data_s['signgu_nm'].apply(lambda x: sum(df2['city_gn_gu_nm'].str.contains(x)))

#음식물 처리를 모두 재활용으로 처리하는 지역 행 제거하기
data_s = data_s[data_s['Food Waste Sum'] != 0]

#0인 count 값 1로 대체
data_s = data_s.replace({'count' : 0}, 1)

#count/Food Waste Sum 열 생성
data_s['처리율'] = data_s['count']/data_s['Food Waste Sum']

print(data_s)

#처리율이 적은 순으로 정렬된 데이터 세트 
data_s_sorted= data_s.sort_values(by='처리율' ,ascending=True)

print(data_s_sorted)

#20구역 선정
data_s_sorted_20 = data_s_sorted.head(n=20)

import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'#한글 깨짐문제 해결
plt.rcParams['axes.unicode_minus'] =False

print(data_s_sorted_20)

data_s_sorted_20.plot.bar(x='signgu_nm',y='처리율')