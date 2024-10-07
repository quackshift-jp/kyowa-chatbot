import os
import time
import pathlib
import sys
import streamlit as st
from datetime import datetime, timedelta

def render():
    sys.path.append(str(pathlib.Path().absolute()))

    st.title("chatbot")

    st.markdown(
        """
        <style>
        .custom-card {
            position: relative;
            display: flex;
            flex-direction: column;
            gap: 8px;
            border-radius: 16px;
            border: 1px solid #ccc;
            padding: 12px 12px 16px;
            text-align: left;
            font-size: 15px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
            width: 320px;
            margin-right: 10px;
            cursor: pointer;
        }
        .custom-card:hover {
            background-color: #f5f5f5;
        }
        .custom-card:disabled {
            cursor: not-allowed;
        }
        .icon-md {
            width: 24px;
            height: 24px;
            color: rgb(118, 208, 235);
        }
        .card-text {
            color: #606060;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            white-space: normal;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    card_template = """
        <div class="custom-card" onClick="document.querySelector('input[type=text]').value='{}'; document.querySelector('button').click();">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-md">
                <path fill="currentColor" fill-rule="evenodd" d="M13.997 3.39A2.5 2.5 0 0 1 17.2 2.103l2.203.882a2.5 2.5 0 0 1 1.342 3.369L19.063 10H20a1 1 0 0 1 1 1v8a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3v-8a1 1 0 0 1 .992-1l-.149-.101-.03-.022c-1.254-.924-1.016-2.864.425-3.458l2.12-.874.724-2.176c.492-1.479 2.41-1.851 3.42-.665L11.99 4.45l1.521.01zm1.513 1.506a2 2 0 0 1 .461 2.618l-1.144 1.861v.045a1.3 1.3 0 0 0 .044.278 1 1 0 0 1 .047.302h1.942l2.07-4.485a.5.5 0 0 0-.268-.673l-2.203-.882a.5.5 0 0 0-.641.258zM12.889 10a3.3 3.3 0 0 1-.06-.499c-.01-.236-.004-.69.237-1.081l1.202-1.954-2.293-.016a2 2 0 0 1-1.51-.704L8.98 4l-.725 2.176A2 2 0 0 1 7.12 7.394L5 8.267l2.063 1.407c.129.087.23.2.303.326zM5 12v7a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-7zm4.5 2.5a1 1 0 0 1 1-1h3a1 1 0 1 1 0 2h-3a1 1 0 0 1-1-1" clip-rule="evenodd"></path>
            </svg>
            <div class="card-text">{}</div>
        </div>
    """


    if "messages" not in st.session_state:
        st.session_state.messages = []



    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    if prompt := st.chat_input("ここに入力してください"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        st.session_state.show_samples = False

        with st.chat_message("assistant"):
            with st.spinner("回答生成中..."):
                time.sleep(2)
                # TODO: rag_main.pyを呼び出す
                #result=rag_main(prompt)
                result = "hogehogeに関する情報は現在利用できません。"
            # TODO: rag_main.pyから呼び出す 
            source_details = [
                {"id":"12345","title": "AIの未来", "published_at": "2023-10-01T12:00:00"},
                {"id":"12345","title": "Pythonの進化", "published_at": "2023-09-15T08:30:00"}
            ]

            if source_details:
                details_message = f'<span style="color: grey; font-size: small;">参考記事は以下の通りです。</span>  \n'
                for detail in source_details:
                    news_url = f'https://hogehoge/{detail["id"]}'
                    details_message += (
                        f'<span style="color: grey; font-size: small;">'
                        f'タイトル: {detail["title"]}  \n'
                        f'公開日: {(datetime.fromisoformat(detail["published_at"]) + timedelta(hours=9)).date()}</span>  \n'
                        f'<span style="color: grey; font-size: small;">'
                        f'記事URL: <a href="{news_url}">{news_url}</a></span>  \n\n'
                    )
            else:
                details_message = (
                    "参考記事はありません。情報の正確性を検証してください。"
                )
            
            answer = f"{result}  \n\n\n{details_message}"
            try:
                st.markdown(answer, unsafe_allow_html=True)
            except Exception as e:
                st.write(f"Error発生: {str(e)}")

        st.session_state.messages.append({"role": "assistant", "content": answer})

        st.rerun()

if __name__ == "__main__":
    render()
