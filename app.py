import streamlit as st, google.generativeai as genai, json, re
st.set_page_config(page_title="AI 英文單字卡")
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", ""))

st.title("📚 AI 萬能單字卡產生器")
st.info("直接貼上任何你想學的英文文章或影片字幕文字吧！")

txt = st.text_area("請在這裡貼上英文文字：", height=200)

if st.button("✨ 開始產生單字卡") and txt:
    try:
        with st.spinner("AI 分析中..."):
            model = genai.GenerativeModel('gemini-pro')
            res = model.generate_content(f"請從以下文字挑選10個核心單字，做成JSON格式(包含 word, pos, cn, exp, eg): {txt[:3500]}")
            cards = json.loads(re.search(r'\[.*\]', res.text, re.DOTALL).group())
            st.success("分析完成！")
            for c in cards:
                with st.expander(f"📌 {c['word']} ({c['pos']})"):
                    st.write(f"**翻譯：** {c['cn']}")
                    st.write(f"**解釋：** {c['exp']}")
                    st.info(f"**例句：** {c['eg']}")
    except Exception as e:
        st.error(f"錯誤：{str(e)}")
