import streamlit as st
import youtube_transcript_api
import google.generativeai as genai
import json
import re

st.set_page_config(page_title="AI 影片單字卡", layout="wide")

# 安全讀取 API Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("後台 Secrets 沒設定 GEMINI_API_KEY！")

st.title("🎬 AI 影片單字卡產生器")
video_url = st.text_input("請貼上 YouTube 網址")

if st.button("✨ 開始產生"):
    if video_url:
        try:
            # 1. 提取 Video ID
            video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", video_url)
            if not video_id_match:
                st.error("網址格式好像不對喔！")
                st.stop()
            video_id = video_id_match.group(1)

            # 2. 抓取字幕 (改用最原始的呼叫方式避免名稱衝突)
            with st.spinner("正在提取影片字幕..."):
                try:
                    # 強制指定用小寫的函式庫名稱呼叫
                    transcript_list = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
                    full_text = " ".join([t['text'] for t in transcript_list])
                except Exception as yt_err:
                    st.error(f"無法抓取字幕：{str(yt_err)}")
                    st.info("提示：請確認影片是否有『英文』字幕（非自動產生有時更準）。")
                    st.stop()
            
            # 3. AI 分析
            with st.spinner("AI 正在分析單字..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                # 確保下面這一行 prompt 前面的空格跟上面的 model 對齊，且中間不要換行
                prompt = f"請從以下字幕挑選 10 個核心單字。格式為 JSON 陣列，包含 word, pos, cn, exp, eg。字幕：{full_text[:3000]}"
                response = model.generate_content(prompt)

                
                # 清理回傳結果，只取 JSON 部分
                clean_text = re.search(r'\[.*\]', response.text, re.DOTALL).group()
                cards = json.loads(clean_text)

            # 4. 顯示結果
            st.success("分析完成！")
            cols = st.columns(2)
            for i, card in enumerate(cards):
                with cols[i % 2]:
                    with st.expander(f"📌 {card['word']} ({card['pos']})"):
                        st.write(f"**中文翻譯：** {card['cn']}")
                        st.write(f"**詳細解釋：** {card['exp']}")
                        st.info(f"**例句：** {card['eg']}")

        except Exception as e:
            st.error(f"發生非預期錯誤：{str(e)}")
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
