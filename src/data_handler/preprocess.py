from docx import Document

def extract_text_from_docx(file_path):
    """
    指定されたWordファイルからテキストを抽出します。

    :param file_path: Wordファイルのパス
    :return: 抽出されたテキスト
    """
    document = Document(file_path)
    full_text = []
    for paragraph in document.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)




if __name__ == "__main__":
    file_path = "/Users/kazukikomura/Developer/quackshift/kyowa-chatbot/data/00指針表紙.docx"
    extracted_text = extract_text_from_docx(file_path)
    print(f"抽出されたテキスト:\n{extracted_text}\n")
