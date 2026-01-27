import streamlit as st
import pandas as pd
import os

# =========================================================
# [설정] 읽어올 파일 (today_predictor_v2.py가 만든 파일)
DATA_FILE = "prediction_result_today.xlsx"
# =========================================================

st.set_page_config(page_title="AI Sports Picks", layout="wide", page_icon="⚽")

# --- 1. 사이드바 & 로그인 ---
st.sidebar.title("💎 VIP 멤버십")
st.sidebar.info("상위 1% 고승률 픽은 VIP 전용입니다.")

user_id = st.sidebar.text_input("아이디")
user_pw = st.sidebar.text_input("비밀번호", type="password")
is_vip = False

if st.sidebar.button("로그인"):
    if user_id == "admin" and user_pw == "1234":
        is_vip = True
        st.session_state['vip_access'] = True
        st.sidebar.success("관리자 로그인 성공! 🔓")
    else:
        st.sidebar.error("정보가 일치하지 않습니다.")

if st.session_state.get('vip_access'):
    is_vip = True

# --- 2. 데이터 로딩 ---
current_folder = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_folder, DATA_FILE)

if os.path.exists(file_path):
    df = pd.read_excel(file_path)
    
    # 메인 헤더
    st.title("⚽ 오늘의 AI 승부 예측")
    st.markdown(f"#### 📅 분석 완료: 총 **{len(df)}**경기 | 🎯 적중률 80% 이상: **{len(df[df['적중확률'] >= 80])}**경기")
    st.divider()

    # --- 3. 경기 리스트 출력 ---
    
    # 컬럼 헤더 디자인
    col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 3, 1.5, 2, 2])
    col1.markdown("**시간**")
    col2.markdown("**홈팀**")
    col3.markdown("**원정팀**")
    col4.markdown("**홈팀 배당**")
    col5.markdown("**AI 추천**")
    col6.markdown("**데이터 확률**")
    st.markdown("---")

    for index, row in df.iterrows():
        # 데이터 추출
        time_str = str(row['시간'])
        home = row['홈팀']
        away = row['원정팀']
        odds = row['홈배당']
        pick = row['AI추천']
        prob = row['적중확률']
        sample = row['표본수']

        # [비즈니스 로직] 승률 80% 이상은 VIP 전용
        is_premium = prob >= 80

        c1, c2, c3, c4, c5, c6 = st.columns([1, 3, 3, 1.5, 2, 2])
        
        # 1. 시간 표시
        c1.write(time_str)

        # 2. 팀 이름 & 배당 & 픽 (VIP 여부에 따라 가림)
        if is_premium and not is_vip:
            # [잠금 모드]
            c2.markdown("🔒 **VIP 전용**")
            c3.markdown("🔒 **VIP 전용**")
            c4.write("-")
            c5.markdown("🔒 **Hidden**")
            # 핵심: 확률은 보여줘서 호기심 자극!
            c6.markdown(f"🔥 **{prob}%** (표본 {sample})")
            
            # 스타일링: 잠긴 행은 회색 배경 느낌 (Streamlit에선 구분선으로 처리)
        else:
            # [공개 모드] or [VIP 로그인 상태]
            c2.write(home)
            c3.write(away)
            c4.write(f"{odds}")
            
            # 픽 색상 강조
            if "홈승" in pick: color = "green"
            elif "원정승" in pick: color = "orange"
            elif "오버" in pick: color = "blue"
            else: color = "gray"
            
            c5.markdown(f":{color}[**{pick}**]")
            
            # 고승률인 경우 불꽃 아이콘 추가
            if prob >= 80:
                c6.markdown(f"🔥 **{prob}%** (표본 {sample})")
            else:
                c6.write(f"{prob}% (표본 {sample})")

        st.markdown("---") # 구분선

else:
    st.error("⚠️ 데이터 파일이 없습니다. 'today_predictor_v2.py'를 먼저 실행해서 엑셀을 만드세요.")