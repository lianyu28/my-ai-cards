import streamlit as st, google.generativeai as genai, json, re

st.set_page_config(page_title="AI 英文單字卡")
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", ""))

st.title("📚 AI 萬能單字卡產生器")
txt = st.text_area("請在這裡貼上英文文字：", height=200)

if st.button("✨ 開始產生單字卡") and txt:
    try:
        with st.spinner("AI 正在尋找最適合的模型..."):
            # 【大招】自動搜尋帳號內可用的模型
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # 優先找 1.5-flash，找不到就找 pro，再找不到就用第一個
            target = next((m for m in models if "1.5-flash" in m), models[0])
            model = genai.GenerativeModel(target)
            
        with st.spinner(f"正在使用 {target} 分析中..."):
            prompt = f"請挑選10個核心單字，回傳JSON陣列(word, pos, cn, exp, eg): {txt[:3000]}"
            response = model.generate_content(prompt)
            clean_json = re.search(r'\[.*\]', response.text, re.DOTALL).group()
            cards = json.loads(clean_json)
            
            st.success(f"完成！(模型: {target})")
            for c in cards:
                with st.expander(f"📌 {c['word']} ({c['pos']})"):
                    st.write(f"**翻譯：** {c['cn']}")
                    st.write(f"**解釋：** {c['exp']}")
                    st.info(f"**例句：** {c['eg']}")
    except Exception as e:
        st.error(f"連線失敗，請檢查 API Key 是否正確。錯誤訊息：{str(e)}")
