from utils.Scrapper import Scrapper
from utils.gemini import Gemini


def main():
    # gemini = Gemini()
    # prompt = 'What is the meaning of life?'
    # print(gemini.generate(prompt).text)
    # https://ai.google.dev/tutorials/python_quickstart
    scrapper = Scrapper('https://i.stack.imgur.com/Ccnnp.png')
    print(scrapper.get_content())


if __name__ == '__main__':
    main()
