import streamlit as st, google.generativeai as genai, json, re

st.set_page_config(page_title="AI 英文單字卡")
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", ""))

st.title("📚 AI 萬能單字卡產生器")
txt = st.text_area("請在此貼上英文：", height=200)

if st.button("✨ 開始產生單字卡") and txt:
    try:
        with st.spinner("正在與 AI 溝通中..."):
            # 這裡不寫名字，直接讓它抓第一個可用的模型
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model = genai.GenerativeModel(available_models[0])

            res = model.generate_content(f"將文字做成10個單字卡JSON格式(word,pos,cn,exp,eg): {txt[:3000]}")
            cards = json.loads(re.search(r'\[.*\]', res.text, re.DOTALL).group())

            st.success("終於搞定了！")
            for c in cards:
                with st.expander(f"📌 {c['word']} ({c['pos']})"):
                    st.write(f"**翻譯：** {c['cn']}")
                    st.write(f"**解釋：** {c['exp']}")
                    st.info(f"**例句：** {c['eg']}")
            st.balloons()
    except Exception as e:
        st.error(f"連線成功但 AI 鬧脾氣，請再按一次產生。錯誤碼：{str(e)}")
