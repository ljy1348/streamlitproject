import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta



st.set_page_config(layout="wide")
st.title('챗봇 실시간 대시보드')

auth = False



st.markdown("""
<style>
[data-testid="stHorizontalBlock"]:nth-last-child(1) > [data-testid="column"]:nth-child(1) {
    border-right: 1px solid #000000; /* 빨간색 선 */
}
</style>
""", unsafe_allow_html=True)

# 기간 설정
time_range_col1, time_range_col2 = st.columns(2)

# 현재 날짜와 시간을 얻습니다.
today = datetime.today().date()

# 이번 달의 첫째 날을 계산합니다.
first_day_of_current_month = today.replace(day=1)

with time_range_col1:
    start_date = st.date_input("시작 날짜", value=first_day_of_current_month, key='start_date')

with time_range_col2:
    end_date = st.date_input("종료 날짜", value=today, key='end_date')


start_date_minus_one_month = start_date - relativedelta(months=1)
end_date_minus_one_month = end_date - relativedelta(months=1)
start_date_minus_one_month_str = start_date_minus_one_month.strftime('%Y-%m-%d')
end_date_minus_one_month_str = end_date_minus_one_month.strftime('%Y-%m-%d')
count_col1 , count_col2 = st.columns(2)

# 카운트 db 가져오기
# data = (start_date_minus_one_month_str, end_date_minus_one_month_str, start_date_minus_one_month_str, end_date_minus_one_month_str,)
# df_count = mysqlutil.save_to_db(sql.get_question_count, data)
# count_list = df_count['ALL_COUNT']
# persantage_list = df_count['PERCENTAGE']

if end_date == today :
    df_count = pd.read_csv('testdata/line_data2.csv')
    count = 19852
    pers = 75
else :
    df_count = pd.read_csv('testdata/line_data1.csv')
    count = 8825
    pers = 72
with count_col1:
    st.markdown(f"""
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 140px; border: 2px solid gray; border-radius: 10px;">
                <div style="font-size: 15px; color: gray; margin-top: 8px; margin-bottom: 10px;">전체 질문 수</div>
                <div style="font-size: 50px; font-weight: bold;">{count}</div>
            </div>
        """, unsafe_allow_html=True)
with count_col2:
    st.markdown(f"""
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 140px; border: 2px solid gray; border-radius: 10px;">
                <div style="font-size: 15px; color: gray; margin-top: 8px; margin-bottom: 10px;">챗봇 답변율</div>
                <div style="font-size: 50px; font-weight: bold;">{pers}%</div>
            </div>
            """, unsafe_allow_html=True)


# 선 그래프
graph_yn = st.checkbox("그래프 보이기")
if graph_yn == False :


    # data = (start_date_minus_one_month_str, end_date_minus_one_month_str)
    # get_data = mysqlutil.save_to_db(sql.select_line_graph_data,data)
    # print(get_data)

    get_data = df_count


    # df = px.data.stocks()
    # print(df.head())

    fig = px.line(get_data, x="Date", y=get_data.columns,
                  hover_data={"Date": "|%Y년 %m월 %d일"},
                  title='카테고리 답변 기록"')

    fig.update_xaxes(
        tickformat="%Y년 %m월 %d일",
        tickformatstops=[
            dict(dtickrange=[None, 'M1'], value="%Y년 %m월 %d일"),  # Less than a month
            dict(dtickrange=['M1', None], value="%Y년 %m월")  # More than a month
        ]
    )
    st.plotly_chart(fig, use_container_width=True)

# 구분선
st.markdown('<hr>', unsafe_allow_html=True)


# 실시간 조회 시간 설정
time_option = st.selectbox('실시간 조회 시간',['1시간','6시간','12시간'])
col1,col2 = st.columns(2)

# 실시간 바 그래프

if time_option == '1시간' :
    read_time = '1'
    category_count_df = pd.read_csv('testdata/category_1hour.csv')
    answer_list_df = pd.read_csv('testdata/count_1hour.csv')
if time_option == '6시간' :
    read_time = '6'
    category_count_df = pd.read_csv('testdata/category_6hour.csv')
    answer_list_df = pd.read_csv('testdata/count_6hour.csv')
if time_option == '12시간' :
    read_time = '12'
    category_count_df = pd.read_csv('testdata/category_12hour.csv')
    answer_list_df = pd.read_csv('testdata/count_12hour.csv')

# temp_data = (read_time,)
# category_count_df = mysqlutil.save_to_db(sql.select_get_category_count, temp_data)
# answer_list_df =  mysqlutil.save_to_db(sql.get_answer_category_list, temp_data)

# category_count_df.sort_values(by=['COUNT'], inplace=True)



연동_카테고리_카운트_fig = px.bar(category_count_df, x='COUNT', y='CATEGORY_NAME', text='COUNT', orientation='h', color_discrete_sequence=['orange'])
연동_카테고리_카운트_fig.update_layout(width=800, height=400)

미연동_카테고리_카운트_fig = px.bar(category_count_df, x='COUNT', y='CATEGORY_NAME', text='COUNT', orientation='h', color_discrete_sequence=['blue'])
미연동_카테고리_카운트_fig.update_layout(width=800, height=400)
with col1:
    st.write("연동")
    st.plotly_chart(연동_카테고리_카운트_fig, use_container_width=True)
    linked_data_show = st.checkbox("연동 질문 보기")
    if linked_data_show == False:
        st.table(answer_list_df)
with col2:
    st.write("미연동")
    st.plotly_chart(미연동_카테고리_카운트_fig, use_container_width=True)
    unlinked_data_show = st.checkbox("미연동 질문 보기")
    if unlinked_data_show == False:
        st.table(answer_list_df)
