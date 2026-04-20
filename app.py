import streamlit as st
import youtube_transcript_api
import google.generativeai as genai
import json, re

st.set_page_config(page_title="AI影片單字卡", layout="wide")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🎬 AI 影片單字卡產生器")
url = st.text_input("請貼上 YouTube 網址")

if st.button("✨ 開始產生"):
    if url:
        try:
            # 1. 抓取 ID
            v_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url).group(1)
            
            # 2. 抓取字幕
            with st.spinner("抓取字幕中..."):
                ts = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(v_id, languages=['en', 'en-US'])
                txt = " ".join([t['text'] for t in ts])[:3500]
            
            # 3. AI 分析
            with st.spinner("AI 分析中..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                pmt = f"請將以下字幕做成10個英文單字卡 JSON 格式(word, pos, cn, exp, eg): {txt}"
                res = model.generate_content(pmt)
                cards = json.loads(re.search(r'\[.*\]', res.text, re.DOTALL).group())

            # 4. 顯示
            st.success("分析完成！")
            cols = st.columns(2)
            for i, c in enumerate(cards):
                with cols[i % 2]:
                    with st.expander(f"📌 {c['word']} ({c['pos']})"):
                        st.write(f"**翻譯：** {c['cn']}")
                        st.write(f"**解釋：** {c['exp']}")
                        st.info(f"**例句：** {c['eg']}")
        except Exception as e:
            st.error(f"錯誤：{str(e)}")
