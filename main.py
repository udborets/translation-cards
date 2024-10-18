from dictionary import Dictionary
from consts import JSON_DICT_PATH


def main():
    dictionary = Dictionary(JSON_DICT_PATH)
    dictionary.menu()


if __name__ == "__main__":
    main()
