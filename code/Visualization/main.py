import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_excel('./billboard_result1.xlsx')
@st.cache_data
def raw_data():
    return pd.read_excel('./billboard_merge.xlsx')



data = load_data()
#df는 장르빈도수가 20개 이상있는 데이터만 추출한다(빈도수가 너무 적은 장르는 제거)
df = data.groupby('장르').filter(lambda x: len(x) >= 20)
#분석하기 전에 있는 크롤링 데이터
raw=raw_data()

#글꼴을 지정한다.
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False



# Plot 1: 월별 장르 시각화
@st.cache_data
def Genre(data):
    data['년도'] = data['년도'].astype(str)
    data['월'] = data['월'].astype(str).str.zfill(2)  

    data['년도-월'] = data['년도'] + '-' + data['월']
    genre_trends = data.pivot_table(index='년도-월', columns='장르', aggfunc='size', fill_value=0)
    st.line_chart(genre_trends)
    
# Plot 2: 월별 가사 감정 시각화
@st.cache_data
def Sentiment(data):
    data['년도'] = data['년도'].astype(str)
    data['월'] = data['월'].astype(str).str.zfill(2) 
    data['년도-월'] = data['년도'] + '-' + data['월']
    sentiment_trends = data.pivot_table(index='년도-월', columns='가사 감정', aggfunc='size', fill_value=0)
    st.line_chart(sentiment_trends)

#가장 인기있는 노래주제 시각화
def title(data):
    theme_trends = data['노래주제'].value_counts().head(10)
    st.bar_chart(theme_trends)
    
#월별 인기있는 가사 주제 평균 순위 시각화
@st.cache_data
def plot_title_trends_heatmap(data):
    monthly_topic_popularity = data.groupby(['월', '노래주제'])['순위'].mean().reset_index()
    monthly_topic_popularity = monthly_topic_popularity.sort_values('순위', ascending=True).drop_duplicates(['월'])
    monthly_heatmap_data = monthly_topic_popularity.pivot(index='노래주제', columns='월', values='순위')
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(monthly_heatmap_data, cmap='coolwarm', annot=True, fmt='.0f', ax=ax)
    ax.set_title('인기있는 가사주제 월 평균 순위')
    ax.set_xlabel('월')
    ax.set_ylabel('노래 주제')
    st.pyplot(fig)


#월별 인기 있는 주제와 해당 장르와 감정 시각화
@st.cache_data
def plot_title_genre_emotion_trends_bar(data):
    #월별 인기 주제 찾는다.
    monthly_topic_popularity = data.groupby(['월', '노래주제'])['순위'].mean().reset_index()
    popular_topics = monthly_topic_popularity.sort_values(['월', '순위'], ascending=[True, True]).drop_duplicates(['월'])
    popular_topics.columns=['월','노래주제','평균순위']
    
    #월별 인기 주제의 장그와 감정을 찾는다
    popular_topics_with_genre_emotion = popular_topics.merge(data[['노래주제', '장르', '순위', '가사 감정']], on='노래주제', how='left').drop_duplicates(['월', '노래주제'])

    
    fig, ax = plt.subplots(figsize=(15, 8))
    for _, row in popular_topics_with_genre_emotion.iterrows():
        plt.bar(row['월'], row['순위'], label=f"{row['노래주제']} ({row['장르']}, {row['가사 감정']})")

    plt.xlabel('월')
    plt.ylabel('평균 순위')
    plt.title('월별 인기 있는 주제, 장르 및 감정의 평균 순위')
    plt.legend(title='노래주제, 장르 및 감정', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    st.pyplot(fig)
    
#월별 인기 있는 주제와 해당 장르와 감정 시각화
@st.cache_data
def plot_title_genre_emotion_trends_bar1(data):
    #월별 인기 주제 찾는다.
    monthly_topic_popularity = data.groupby(['월', '노래주제'])['차트인한 기간'].mean().reset_index()
    popular_topics = monthly_topic_popularity.sort_values(['월', '차트인한 기간'], ascending=[True, True]).drop_duplicates(['월'])
    popular_topics.columns=['월','노래주제','평균순위']
    
    #월별 인기 주제의 장그와 감정을 찾는다
    popular_topics_with_genre_emotion = popular_topics.merge(data[['노래주제', '장르', '차트인한 기간', '가사 감정']], on='노래주제', how='left').drop_duplicates(['월', '차트인한 기간'])

    
    fig, ax = plt.subplots(figsize=(15, 8))
    for _, row in popular_topics_with_genre_emotion.iterrows():
        plt.bar(row['월'], row['차트인한 기간'], label=f"{row['노래주제']} ({row['장르']}, {row['가사 감정']})")

    plt.xlabel('월')
    plt.ylabel('평균 차트인한 기간')
    plt.title('월별 인기 있는 주제, 장르 및 감정의 평균 순위')
    plt.legend(title='노래주제, 장르 및 감정', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    st.pyplot(fig)


    



# Streamlit 앱 시작

data = load_data()
# 사이드바에 분석 선택 옵션 추가
analysis_type = st.sidebar.selectbox(
    '분석 타입을 선택하세요:',
    [ '프로젝트','데이터 소개및 분석' ,'노래 트랜드','인기있는 가사주제 월 평균 순위',
        '월별 인기 있는 주제와 해당 장르와 감정','오랫동안 사랑받는 노래 시각화','결과']
)

# 선택한 분석 유형에 따라 시각화 표시
if analysis_type=='프로젝트':
    st.title('프로젝트 소개')
    st.subheader("주제")
    st.write('''대중음악 트렌드 분석을 통한 전략적 음악 제작 및 마케팅 전략''')
    st.subheader("회사")
    st.write('''음악 제작및 마케팅 회사(하이브)''')
    st.subheader("데이터 수집")
    st.write('''빌보드사이트에서 순위, 아티스트, 노래에 대한 정보를 크롤링 하였습니다.''')
    st.write('''빌보드에서 크롤링한 정보를 활용해서 지니뮤직에서 장르, 가사, 재생시간 정보를 크롤링 하였습니다.''')
    with st.expander("크롤링 데이터 보기"):
        #전체 데이터
        st.dataframe(raw)#표 형태의 데이터를 화면에 보여줘

elif analysis_type =='데이터 소개및 분석':
    st.title('데이터 소개및 분석')
    with st.expander("Raw데이터 보기"):
        #전체 데이터
        st.dataframe(raw)#표 형태의 데이터를 화면에 보여줘
    st.header("분석 방법론")
    st.subheader("감정분석")
    st.write('''감정 분석을 통해 가사의 내용을 긍정적, 부정적, 중립적 감정을 구별하였습니다.''')
    st.subheader("topic 모델링")    
    st.write('''topic 모델링을 통해 가사 내용으로 주제를 나누었습니다.''')
    st.subheader("최종 데이터")
    with st.expander("최종 데이터 보기"):
        #전체 데이터
        st.dataframe(data)#표 형태의 데이터를 화면에 보여줘



elif analysis_type=='노래 트랜드':
    st.header("분석 결과")
    st.subheader("년도 월에따른 장르 트랜드")
    Genre(df)
    st.subheader("년도 월에따른 가사 감정 트랜드")
    Sentiment(df)    
    st.subheader("Top music title")
    title(df)
    
         
elif analysis_type == '인기있는 가사주제 월 평균 순위':
    st.header("분석 결과")
    st.subheader("월별로 가장 인기있는 가사주제")
    plot_title_trends_heatmap(df)
    st.write('''### 결과''')
    st.write('''히트맵에서 월별로 가장 인기있는 주제를 표현한 것입니다(숫자는 평균 순위)''')
    df1=df[df['순위']<11]
    genres_to_keep = df1['노래주제'].value_counts() > 4
    filtered_df = df1[df1['노래주제'].isin(genres_to_keep[genres_to_keep].index)]    
    plot_title_trends_heatmap(filtered_df)
    st.write('''### TOP 10 결과''')
    st.write('''다음과 같은 가사 주제가 월별로 가장 인기가 있다는 사실을 알 수 있습니다.''')


    
elif analysis_type=='월별 인기 있는 주제와 해당 장르와 감정':
    st.header("분석 결과")
    st.subheader("월별 인기 있는 주제와 해당 장르")
    plot_title_genre_emotion_trends_bar(df)
    st.write('''### 결과''')
    st.write('''월별로 가장 인기있는 주제별 장르와 감정을 나타낸 결과입니다''')
    df1=df[df['순위']<11]
    genres_to_keep = df1['노래주제'].value_counts() > 4
    filtered_df = df1[df1['노래주제'].isin(genres_to_keep[genres_to_keep].index)]    
    plot_title_genre_emotion_trends_bar(filtered_df)
    st.write('''### TOP 10 결과''')
    st.write('''다음과 같은 가사 주제별 장르와 감정이 월별로 가장 인기가 있다는 사실을 알수 있습니다.''')

elif analysis_type == '오랫동안 사랑받는 노래 시각화':
    st.header("분석 결과")
    st.subheader("차트인을 오랫동안 유지한 주제와 해당 장르와 감정")
    plot_title_genre_emotion_trends_bar1(df)
    st.write('''### 결과''')
    st.write('''차트인을 오랫동안 한 주제별 장르와 감정이 영향을 많이 준다는 사실을 알 수 있습니다.''')
    df1=df[df['차트인한 기간']>10]
    genres_to_keep = df1['노래주제'].value_counts() > 4
    filtered_df = df1[df1['노래주제'].isin(genres_to_keep[genres_to_keep].index)]    
    plot_title_genre_emotion_trends_bar1(filtered_df)
    st.write('''### 차트인 기간이 기간이 10개월 보다 높은 결과''')
    st.write('''다음과 같은 가사 주제별 장르와 감정이 대중에게 오랫동안 사랑받는 것을 알 수 있습니다.''')

elif analysis_type == '결과':
    st.header("하이브회사에서의 프로젝트 활용방안")
    st.subheader("전략적 의사 결정")
    st.write('''인사이트를 통해 회사는 빌보드에서 살아남을 수 있는 음악이 어떤 종류의 음악인지 알 수 있습니다. ''')
    st.subheader("시장 동향에 따른 마케팅 전략")
    st.write(''' 특정 달에 인기가 있는 노래를 출시하여 대중에게
             공감을 불러일으키는 효과적인 마케팅 전략을 세울 수 있습니다.''')
    st.subheader("시장 예측기반 아티스트 확보")
    st.write(''' 특정 달에 인기가 있는 음악을 만들기 위해서 특정 노래 주제와 감정, 특정 장르에 특화된 아티스트를 미리 선점할수 있습니다.''')
    st.subheader("프로모션 및 광고 계획")
    st.write('''차트에서 오래 머물수 있게 인사이트를 통해 얻은 노래 주제와 장르 및 감정을 기반으로하는 음악을 홍보하여 
             차트에서 롱런할수 있는 계획을 세울수 있습니다.''')
    st.subheader("시장 이해")
    st.write('''인사이트를 통해서 소비자 선호도의 패턴과 변화를 빠르게 알 수 있습니다.''')