import streamlit as st
import youtube_transcript_api
import google.generativeai as genai
import json, re

st.set_page_config(page_title="AI單字卡")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🎬 AI 影片單字卡產生器")
url = st.text_input("請貼上 YouTube 網址")

if st.button("✨ 開始產生"):
    if url:
        try:
            v_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url).group(1)
            with st.spinner("處理中..."):
                ts = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(v_id, languages=['en', 'en-US'])
                txt = " ".join([t['text'] for t in ts])[:3500]
                model = genai.GenerativeModel('gemini-1.5-flash')
                pmt = f"請將字幕做成10個單字卡JSON格式(word,pos,cn,exp,eg): {txt}"
                res = model.generate_content(pmt)
                cards = json.loads(re.search(r'\[.*\]', res.text, re.DOTALL).group())
                st.success("分析完成！")
                for c in cards:
                    with st.expander(f"📌 {c['word']} ({c['pos']})"):
                        st.write(f"**翻譯：** {c['cn']}")
                        st.write(f"**解釋：** {c['exp']}")
                        st.info(f"**例句：** {c['eg']}")
        except Exception as e:
            st.error(f"錯誤：{str(e)}")
