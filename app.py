import streamlit as st, google.generativeai as genai, json, re

st.set_page_config(page_title="AI 英文單字卡")
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", ""))

st.title("📚 AI 萬能單字卡產生器")
txt = st.text_area("請在這裡貼上英文文字：", height=200)

if st.button("✨ 開始產生單字卡") and txt:
    try:
        with st.spinner("正在連線至 AI 伺服器..."):
            # 使用最穩定且支援 beta 版通道的名稱
            model = genai.GenerativeModel('models/gemini-pro')
            
            prompt = f"請挑選10個核心單字，回傳JSON陣列(word, pos, cn, exp, eg): {txt[:3000]}"
            response = model.generate_content(prompt)
            
            clean_json = re.search(r'\[.*\]', response.text, re.DOTALL).group()
            cards = json.loads(clean_json)
            
            st.success("成功！")
            for c in cards:
                with st.expander(f"📌 {c['word']} ({c['pos']})"):
                    st.write(f"**翻譯：** {c['cn']}")
                    st.write(f"**解釋：** {c['exp']}")
                    st.info(f"**例句：** {c['eg']}")
    except Exception as e:
        st.error(f"連線成功但 AI 拒絕請求，訊息：{str(e)}")
