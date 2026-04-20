import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi as yta
import google.generativeai as genai
import json
import re

# 頁面設定
st.set_page_config(page_title="AI 影片單字卡", layout="wide")

# 這裡隱藏你的 API Key，稍後會在 Streamlit 後台設定
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🎬 AI 影片單字卡產生器")
st.caption("輸入 YouTube 網址，自動抓取字幕並分析 10 個核心單字")

# 輸入框
video_url = st.text_input("請貼上 YouTube 網址 (例如: https://www.youtube.com/watch?v=xxxx)")

if st.button("✨ 開始產生"):
    if not video_url:
        st.error("請先貼上網址喔！")
    else:
        try:
            with st.spinner("正在提取影片字幕..."):
                # 提取 YouTube Video ID
                video_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", video_url).group(1)
                # 抓取字幕 (預設英文)
                transcript_list = yta.get_transcript(video_id, languages=['en'])
                full_text = " ".join([t['text'] for t in transcript_list])
            
            with st.spinner("AI 正在分析單字..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"""
                請從以下字幕中挑選 10 個核心單字。
                回傳格式必須是 JSON 陣列，每個物件包含：
                "word" (單字), "pos" (詞性), "cn" (中文翻譯), "exp" (中文解釋), "eg" (英文例句)。
                字幕內容：{full_text[:3000]}
                """
                response = model.generate_content(prompt)
                # 清理回傳格式
                raw_json = re.search(r'\[.*\]', response.text, re.DOTALL).group()
                cards = json.loads(raw_json)

            # 顯示結果 (使用 Streamlit 的欄位佈局)
            st.success("分析完成！")
            cols = st.columns(2)
            for i, card in enumerate(cards):
                with cols[i % 2]:
                    with st.expander(f"📌 {card['word']} ({card['pos']})"):
                        st.write(f"**中文翻譯：** {card['cn']}")
                        st.write(f"**詳細解釋：** {card['exp']}")
                        st.info(f"**例句：** {card['eg']}")

        except Exception as e:
            st.error(f"發生錯誤：{str(e)}")
            st.write("提示：請確認該影片是否有提供英文提供字幕（非自動產生有時會失敗）。")

# 建立一個 requirements.txt 檔案，貼上這三行：
# streamlit
# youtube-transcript-api
# google-generativeai
