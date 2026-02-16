import os

os.environ['TRANSFORMERS_CACHE'] = '/code/.cache/'

from transformers import pipeline
import torch
from googletrans import Translator


class IA:
    def __init__(self, cache_dir="/code/.cache/"):

        self.model_bert = pipeline("question-answering", model="DracolIA/BERT-Context-based-QA", cache_dir=cache_dir)

        self.model_bigbird = pipeline("question-answering", model="DracolIA/BigBird-Roberta-Context-based-QA", cache_dir=cache_dir)

        self.model_splinter = pipeline("question-answering", model="DracolIA/Splinter-Context-based-QA", cache_dir=cache_dir)

        self.model_squeeze = pipeline("question-answering", model="DracolIA/SqueezeBert-Context-based-QA", cache_dir=cache_dir)


    def generate_responses(self, question, file_content, have_file, selected_model):
        print("file_content: ", file_content)
        translator = Translator()
        language = translator.detect(str(question)).lang.upper() # Verify the language of the prompt

        if have_file:
            context = str(file_content)
        else:
            context = str()

        if selected_model.upper() == "BERT":
            print("Choosen model: BERT")
            model = self.model_bert

        if selected_model.upper() == "BIGBIRD":
            print("Choosen model: BIGBIRD")
            model = self.model_bigbird

        if selected_model.upper() == "ALBERT":
            print("Choosen model: ALBERT")
            model = self.model_albert

        if selected_model.upper() == "SPLINTER":
            print("Choosen model: SPLINTER")
            model = self.model_splinter

        if selected_model.upper() == "SQUEEZE":
            print("Choosen model: SQUEEZE")
            model = self.model_squeeze


        if language != "EN":
                question = translator.translate(str(question), src=language, dest="en").text # Translation of user text to english for the model
        
        answer = model(context = context, question = question)
        if answer != "" or len(answer) != 0:
            answer = answer["answer"]
            if language != "EN":
                answer = Translator().translate(str(answer), src="en", dest=language).text # Translation of model's te*xt to user's language
                
        print("====================> answer: ", answer)
        return str(answer)