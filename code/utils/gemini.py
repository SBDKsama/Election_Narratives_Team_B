import os
import shutil
import google.generativeai as genai


class Gemini:
    def __init__(self):
        if not os.path.exists('utils/gemini_key.py'):
            shutil.copy('utils/gemini_key_example.py', 'utils/gemini_key.py')
            raise Exception('Please fill in the Gemini API key and secret in utils/gemini_key.py')
        import utils.gemini_key
        if utils.gemini_key.key == 'FILL_YOUR_API_KEY_HERE':
            raise Exception('Please fill in the Gemini API key and secret in utils/gemini_key.py')
        self.key = utils.gemini_key.key
        genai.configure(api_key=self.key)
        self.text_model = 'gemini-1.5-pro-latest'
        self.model = genai.GenerativeModel(self.text_model)

    def generate(self, prompt):
        return self.model.generate_content(prompt)
