# Summary:
# The `gemini.py` module defines a class `Gemini` that integrates with Google's generative AI service.
# This class is primarily used to handle interactions with the Gemini API, specifically for content generation.

# Description:
# - The Gemini class checks for the presence of an API key file (`utils/gemini_key.py`). If it doesn't exist, it copies
#   a template file (`gemini_key_example.py`) to this location and prompts the user to enter their API key.
# - Once the API key is set, it configures the Gemini generative AI model using this key.
# - The class provides a `generate` method that takes a text prompt and returns generated content using the configured model.
# - The default model used is 'gemini-1.5-pro-latest', which likely refers to a specific version of Google's generative AI models.
# - This script integrates API key management and model interaction, ensuring the user provides a valid API key before attempting
#   to generate content.

import os
import shutil
import google.generativeai as genai


class Gemini:
    def __init__(self):
        if not os.path.exists('utils/gemini_key.py'):
            shutil.copy('utils/gemini_key_example.py', 'utils/gemini_key.py')
            raise Exception('Please fill in the Gemini API key and secret in utils/gemini_key.py')
        import utils.gemini_key
        if utils.gemini_key.gemini_key == 'FILL_YOUR_API_KEY_HERE':
            raise Exception('Please fill in the Gemini API key and secret in utils/gemini_key.py')
        self.key = utils.gemini_key.gemini_key
        genai.configure(api_key=self.key)
        self.text_model = 'gemini-1.5-pro-latest'
        self.model = genai.GenerativeModel(self.text_model)

    def generate(self, prompt):
        return self.model.generate_content(prompt)
