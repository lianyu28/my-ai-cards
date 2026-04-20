import streamlit as st, google.generativeai as genai, json, re

st.set_page_config(page_title="AI 英文單字卡")
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", ""))

st.title("📚 AI 萬能單字卡產生器")
txt = st.text_area("請在此貼上英文：", height=200)

if st.button("✨ 開始產生單字卡") and txt:
    try:
        with st.spinner("正在跟 AI 談判中..."):
            # 嘗試清單：從最強到最穩定
            for model_name in ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-pro']:
                try:
                    model = genai.GenerativeModel(model_name)
                    res = model.generate_content(f"將文字做成10個單字卡JSON格式(word,pos,cn,exp,eg): {txt[:3000]}")
                    cards = json.loads(re.search(r'\[.*\]', res.text, re.DOTALL).group())
                    st.success(f"終於成功了！(使用的 AI 是：{model_name})")
                    for c in cards:
                        with st.expander(f"📌 {c['word']} ({c['pos']})"):
                            st.write(f"**翻譯：** {c['cn']}")
                            st.write(f"**解釋：** {c['exp']}")
                            st.info(f"**例句：** {c['eg']}")
                    st.balloons() # 成功的話給妳點氣球慶祝！
                    break
                except:
                    continue 
            else:
                st.error("Google AI 暫時無法連線，可能是 API Key 權限問題或區域限制。")
    except Exception as e:
        st.error(f"發生意外：{str(e)}")
