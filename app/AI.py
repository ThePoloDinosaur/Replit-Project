import os
from google import genai
from transformers import pipeline
from dotenv import load_dotenv
from timer import timer



class AI:
    def __init__(self):
        load_dotenv()
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    @timer('generate_gemini_content', 'ms')
    def generate_gemini_content(self, context, prompt):
        client = genai.Client(api_key='AIzaSyBDlj4qrzwrNv5VZWhIxQcdLDoI54z1a4M')

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=context + "\n" + prompt,
        )

        return response
    @timer('sentiment_analysis', 'ms')
    def sentiment_analysis(self, data):

        sentiment_pipeline = pipeline(model="nlptown/bert-base-multilingual-uncased-sentiment")
        
        return sentiment_pipeline(data)
    
    
if __name__ == "__main__":
    ai_version = False 
    if ai_version == False:
        ai = AI()
        data = ['<p>?: (ckeditor.W001) django-ckeditor bundles CKEditor 4.22.1 which isn&#39;t supported anymore and which does have unfixed security issues, see for example https://ckeditor.com/cke4/release/CKEditor-4.24.0-LTS . You should consider strongly switching to a different editor (maybe CKEditor 5 respectively django-ckeditor-5 after checking whether the CKEditor 5 license terms work for you) or switch to the non-free CKEditor 4 LTS package. See https://ckeditor.com/ckeditor-4-support/ for more on this. (Note! This notice has been added by the django-ckeditor developers and we are not affiliated with CKSource and were not involved in the licensing change, so please refrain from complaining to us. Thanks.)</p>']
        print(ai.sentiment_analysis(data))
    if ai_version == True:
        ai = AI()
        context = ""
        prompt = ""
        print(ai.generate_gemini_content(context, prompt).text)