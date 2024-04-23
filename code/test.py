from utils.Scrapper import Scrapper
from utils.gemini import Gemini


def main():
    gemini = Gemini()
    prompt = 'What is the meaning of life?'
    print(gemini.generate(prompt).text)
    # https://ai.google.dev/tutorials/python_quickstart
    # scrapper = Scrapper(['https://i.stack.imgur.com/Ccnnp.png', 'https://i.stack.imgur.com/Ccnnp2.png'])
    # scrapper.get_all_contents(thread_num=1)
    # print(scrapper.result_map)


if __name__ == '__main__':
    main()
