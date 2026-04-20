import streamlit as st, youtube_transcript_api as yta, google.generativeai as genai, json, re
st.set_page_config(page_title="AI單字卡")
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", ""))
st.title("🎬 AI 影片單字卡產生器")
url = st.text_input("請貼上 YouTube 網址")
if st.button("✨ 開始產生") and url:
    try:
        vid = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url).group(1)
        with st.spinner("處理中..."):
            ts = yta.YouTubeTranscriptApi.get_transcript(vid, languages=['en', 'en-US'])
            txt = " ".join([t['text'] for t in ts])[:3500]
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(f"將字幕做成10個單字卡JSON格式(word,pos,cn,exp,eg): {txt}")
            cards = json.loads(re.search(r'\[.*\]', res.text, re.DOTALL).group())
            st.success("完成！")
            for c in cards:
                with st.expander(f"📌 {c['word']} ({c['pos']})"):
                    st.write(f"**翻譯：** {c['cn']}")
                    st.write(f"**解釋：** {c['exp']}")
                    st.info(f"**例句：** {c['eg']}")
    except Exception as e:
        st.error(f"錯誤：{str(e)}")
