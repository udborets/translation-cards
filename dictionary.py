import os
import random
import json


class Dictionary(dict):
    def __init__(self, path: str):
        assert path[-5:] == ".json"
        self.path = path
        self.__init_file()

    def clear_data(self):
        self.__update_file(dict())

    def get_data(self):
        with open(self.path, "r") as f:
            json_data = json.load(f)
        return json_data

    def __update_file(self, data: dict):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(
                data, f, indent=4, sort_keys=True, ensure_ascii=True)
            f.close()

    def __init_file(self):
        if os.path.getsize(self.path) != 0:
            return
        self.__update_file(dict())

    def ensure_dict(self) -> bool:
        current_data = self.get_data()
        if not isinstance(current_data["translations"], dict):
            return False
        if not isinstance(current_data["show_after"], dict):
            return False
        return True

    def __init_sentence(self, sentence: str) -> dict:
        current_data = self.get_data()
        sentence_dict = {"translations": [], "show_after": 0}
        current_data[sentence] = sentence_dict
        self.__update_file(current_data)
        return current_data

    def get_random_sentence(self) -> str:
        current_data = self.get_data()
        sentences = list(current_data.keys())
        random_sentence = sentences[random.randrange(len(sentences))]
        return random_sentence

    def get_translation(self, sentence: str) -> list[str]:
        current_data = self.get_data()
        if sentence not in current_data:
            return []
        return current_data[sentence]["translations"]

    def menu(self):
        request = ''
        while request != "q":
            request = input(
                "A(a)dd translation/L(l)earn/P(p)rint/Q(q)uit: ").lower().strip()
            if request == "a":
                sentence = input("Enter sentence: ")
                translation = input("Enter translation: ")
                add_result = self.add_translation(sentence, translation)
                if add_result:
                    print("Added translation to the dictionary!")
                if not add_result:
                    print("Something went wrong!")
            if request == "l":
                if len(self.get_data().keys()) == 0:
                    print("There is nothing to learn yet")
                    continue
                learn_request = ""
                while learn_request != "q":
                    random_sentence = self.get_random_sentence()
                    print(random_sentence, end="")
                    learn_request = input()
                    print(self.get_translation(random_sentence))
            if request == "p":
                print(json.dumps(self.get_data(), indent=4))
        self.clear_data()

    def add_translation(self, sentence: str, translation: str) -> bool:
        current_data = self.get_data()
        formatted_sentence = sentence.strip()
        formatted_translation = translation.strip()
        if not formatted_sentence or not formatted_translation:
            return False
        if formatted_sentence in current_data:
            print("This sentence is already in your a dictionary.\n\
            Do you want to add a new translation or replace the old one?")
            answer = ""
            while len(answer) == 0:
                answer = input("Add(a): ").lower().strip()
                if answer[0] == "a":
                    current_data[formatted_sentence]["translations"].append(
                        formatted_translation)
        if formatted_sentence not in current_data:
            current_data = self.__init_sentence(formatted_sentence)
            current_data[formatted_sentence]["translations"].append(
                formatted_translation)

        self.__update_file(current_data)
        return True
