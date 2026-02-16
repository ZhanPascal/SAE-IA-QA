import fitz
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pandas as pd
from Exceptions.FileTypeIsNotAcceptedException import FileTypeIsNotAcceptedException
from googletrans import Translator
import PyPDF2
from io import BytesIO

class Service_File:
    def __init__(self):
        pass

    def file_for_string(self, file):
        translator = Translator()
        
        if file.name.endswith('.docx'):
            print("File is a docx")
            string = self.word_to_string(file)
        
        elif file.name.endswith('.pdf'):
            print("File is a pdf")
            string = self.pdf_to_string(file)

        elif file.name.endswith('.xlsx'):
            print("File is an .xlsx")
            string = self.excel_to_string(file)
        
        elif file.name.endswith('.csv'):
            print("File is a .csv")
            string = self.csv_to_string(file)
        
        else:
            raise FileTypeIsNotAcceptedException('File type is not accepted. Please upload a .docx, .pdf, .xlsx or .csv file.')
        
        string = string.replace('\n', ' ').replace('\t', ' ').replace('"', ' ').replace("'", ' ')
        split = self.split_text(string)
        print(len(split))

        translate = ""
        for i in range(len(split)):
            print(i)
            language = translator.detect(str(split[i])).lang.upper() # Verify the language of the prompt
            if split[i] != "" or len(split[i]) != 0:
                if language != "EN":
                    translate = translate + translator.translate(str(split[i]), src=language, dest="EN").text
                else:
                    translate = translate + split[i]
        
        print("translate: ", translate)
        return translate


    def split_text(self, text, max_chars=1500):
        if len(text) <= max_chars:
            return [text]

        split_texts = []
        current_text = ""
        words = text.split()
        for word in words:
            if len(current_text) + len(word) + 1 <= max_chars:
                current_text += word + " "
            else:
                split_texts.append(current_text)
                current_text = word + " "
        split_texts.append(current_text)

        return split_texts
    

    def pdf_to_string(self, file):
        pdf_data = file.read()
        pdf_document = PyPDF2.PdfReader(BytesIO(pdf_data))
        text = ""
        for page_number in range(len(pdf_document.pages)):
            text += pdf_document.pages[page_number].extract_text()
        return text

    def word_to_string(self, file):
        doc = Document(file)
        full_text = []

        for para in doc.paragraphs:
            full_text.append(para.text)

        return '\n'.join(full_text)
    
    def excel_to_string(self, file):
        df = pd.read_excel(file)
        return self.dataframe_to_formatted_string(df)

    def csv_to_string(self, file):
        df = pd.read_csv(file)        
        return self.dataframe_to_formatted_string(df)

    def dataframe_to_formatted_string(self, df):
        formatted_string = ', '.join(df.columns) + '\n'
        
        for index, row in df.iterrows():
            line_values = [str(value) for value in row]
            formatted_string += ', '.join(line_values) + '\n'
        
        return formatted_string.strip()
    
