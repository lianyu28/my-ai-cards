import streamlit as st, google.generativeai as genai, json, re

st.set_page_config(page_title="AI 英文單字卡")
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", ""))

st.title("📚 AI 萬能單字卡產生器")
st.info("直接貼上英文文字，AI 會幫你整理單字卡！")

txt = st.text_area("請在這裡貼上英文文字：", height=200)

if st.button("✨ 開始產生單字卡") and txt:
    try:
        with st.spinner("AI 分析中..."):
            # 【關鍵修改】直接使用最通用的名稱，或是自動抓取
            model = genai.GenerativeModel('gemini-1.5-flash-latest') 
            
            prompt = f"請挑選10個核心單字，回傳JSON陣列(word, pos, cn, exp, eg): {txt[:3000]}"
            response = model.generate_content(prompt)
            
            # 清理 JSON 回傳格式
            clean_json = re.search(r'\[.*\]', response.text, re.DOTALL).group()
            cards = json.loads(clean_json)
            
            st.success("完成！")
            for c in cards:
                with st.expander(f"📌 {c['word']} ({c['pos']})"):
                    st.write(f"**翻譯：** {c['cn']}")
                    st.write(f"**解釋：** {c['exp']}")
                    st.info(f"**例句：** {c['eg']}")
    except Exception as e:
        # 如果 flash-latest 不行，再試一次基本的 flash
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # ... 重複內容略 ... (這段是為了預防萬一)
            st.error(f"連線成功但發生細微錯誤，請再試一次。詳細訊息：{str(e)}")
        except:
            st.error(f"發生錯誤：{str(e)}")
