from docx import Document
import os
from pathlib import Path


def preprocess(input_dir="data", output_dir="data"):
    """
    指定されたディレクトリ内の全てのWordファイルからテキストを抽出し、txtファイルとして保存します。

    :param input_dir: Wordファイルが保存されているディレクトリ
    :param output_dir: テキストファイルを保存するディレクトリ
    :return: 抽出されたテキストのリスト
    """
    extracted_texts = []
    for file_path in Path(input_dir).glob("*.docx"):
        document = Document(file_path)
        full_text = []
        for paragraph in document.paragraphs:
            full_text.append(paragraph.text)
        extracted_text = '\n'.join(full_text)
        
        # テキストをファイルに保存
        output_file_path = os.path.join(output_dir, f"{file_path.stem}.txt")
        with open(output_file_path, "w") as f:
            f.write(extracted_text)
        
        extracted_texts.append(extracted_text)
    
    return extracted_texts


if __name__ == "__main__":
    extracted_texts = preprocess()
    for text in extracted_texts:
        print(f"抽出されたテキスト:\n{text}\n")
