from home.json_file import *

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64


class Word:

    def __init__(self, word, meaning, sample):
        self.word = word
        self.meaning = meaning
        self.sample = sample


class Dictionary:
    saved = False

    def __init__(self, file_name):
        self.file_name = file_name
        self.DecryptFile(self.file_name, "15")

        self.dict_words = JsonFile.read(self.file_name)


        self.word_list = []

        for word_data in self.dict_words:
            words = Word(word_data['word'], word_data['meaning'], word_data['sample'])
            self.word_list.append(words)

    def display_all_words(self):
        length_word = []
        for key in self.dict_words:
            print(key)
            for k, value in key.items():
                length_word.append(value)
        self.a = len(max(length_word, key=len))

        # print(f"{'Word':^{self.a}} | {'Meaning':^{self.a}} | {'Sample':^{self.a}} ")
        # print("__________________________________________")
        for word_data in self.word_list:
            print(f"{word_data.word:<{self.a}} | {word_data.meaning:<{self.a}} | {word_data.sample:<{self.a}}")
        self.EncryptFile(self.file_name, "15")

    def insert_word(self, **kwargs):
        new_word = {}
        for key, value in kwargs.items():
            new_word[key] = value
        list_of_words = []

        for inner_dict in self.dict_words:
            list_of_words.append(inner_dict["word"])
            if new_word["word"] == inner_dict["word"]:
                if new_word["meaning"] == inner_dict["meaning"]:
                    print("Aynısı var")
                    break
                else:
                    print("ANLAMLAR FARKLI")
                    self.dict_words.append(new_word)
                    self.Save()
                    break
            else:
                continue
        if new_word["word"] not in list_of_words:
            print("LİSTEDE HİÇ YOK")
            self.dict_words.append(new_word)
            self.Save()

    def search_word(self, value):
        print("{:<8}   ".format('Meaning'))
        print('─' * 45)
        meaning_list=[]
        index = 0
        while index < len(self.dict_words):
            for key in self.word_list:
                try:
                    if value == key.word:
                        meaning_list.append(key.meaning)
                except Exception as exceptionObject:
                    print("Hata", exceptionObject)
                index += 1
        return meaning_list

    def delete_word(self, value):

        index = 0
        while index < len(self.dict_words):
            for i, j in enumerate(self.dict_words):
                for key in j:
                    if value == j[key]:
                        del self.dict_words[i]
                        continue
                    else:
                        continue
            self.Save()
            index += 1

    # def update_word(self):
    #     # bir tane değer girilmesi gerek
    #     # bu gelen değeri gidip listede bulsun ve bu değeri değiştirsin
    #
    #     new_value = input("değer girin:")
    #
    #     for index, dicts in enumerate(self.dict_words):
    #         for i in dicts:
    #             if new_value == dicts[i]:
    #                 print("burDaaa")
    #                 del self.dict_words[index]
    #                 new_words = {
    #                     "word": input("word gir"),
    #                     "meaning": input("meaning gir"),
    #                     "sample": input("sample gir"),
    #                 }
    #                 for key, value in new_words.items():
    #                     new_words[key] = value
    #
    #                 self.dict_words.append(new_words)
    #                 self.Save()

    def edit_word(self, new_value, word, meaning):
        for i in self.dict_words:
            if str(word).upper() == i.get('word').upper():
                if str(meaning).upper() == i.get('meaning').upper():
                    i['meaning'] = new_value
        self.Save()
        word_list = self.word_list
        for word_data in self.dict_words:
            word = Word(word_data["word"], word_data["meaning"],
                        word_data["sample"])
            word_list.append(word)
        # self.EncryptFile(self.file_name, "15")



    def DeriveKey(self, passwordParam):
        if type(passwordParam) == str:
            passwordParam = passwordParam.encode("utf-8")
        keyDerivationFunction = Scrypt(
            salt=b'ABCDEFGHIJKLMNOP',
            length=32,
            n=2 ** 14,
            r=8,
            p=1,
            backend=default_backend()
        )
        deriveKey = keyDerivationFunction.derive(passwordParam)
        key = base64.urlsafe_b64encode(deriveKey)
        return key

    def Encrypt(self, chunkParam, passwordParam: str):
        convertChunkToString = False
        if type(chunkParam) == str:
            chunkParam = chunkParam.encode("utf-8")
            convertChunkToString = True
        key = self.DeriveKey(passwordParam)
        fernet = Fernet(key)
        encryptedChunk = fernet.encrypt(chunkParam)
        if convertChunkToString == True:
            encryptedChunk = encryptedChunk.decode("utf-8")
        return encryptedChunk

    def Decrypt(self, chunkParam, passwordParam: int):
        key = self.DeriveKey(passwordParam)
        fernet = Fernet(key)
        try:
            decryptedChunk = fernet.decrypt(chunkParam)
        except  Exception:
            return None

        return decryptedChunk

    def EncryptFile(self, fileNameParam: str, passwordParam: str) -> None:
        with open(fileNameParam, "rb") as fileObject:
            fileContent = fileObject.read()
            encryptedFileContent = self.Encrypt(fileContent, passwordParam)
        with open(f"{fileNameParam}", "wb") as fileObject:
            fileObject.write(encryptedFileContent)

    def DecryptFile(self, fileNameParam: str, passwordParam: str) -> None:
        with open(fileNameParam, "rb") as fileObject:
            fileContent = fileObject.read()
            decryptedFileContent = self.Decrypt(fileContent, passwordParam)

            if decryptedFileContent == None:
                print(" ")
            else:
                with open(f"{fileNameParam}", "wb") as fileObject:
                    fileObject.write(decryptedFileContent)

    def Save(self):
        with open(f"{self.file_name}", "w", encoding="utf-8") as file_object:
            json.dump(self.dict_words, file_object, indent=4, separators=(',', ': '))
        # self.EncryptFile(self.file_name, "15")
        self.saved = True


# #
# cl = Dictionary("../home/deneme.json")
# #
#
# cl.display_all_words()

# while True:
#     command = input("İşlem türünü giriniz(E/D): ").upper()
#     if command == "E" or command == "D":
#         break
#     else:
#         print("işlem türünü E veya D olarak giriniz:")
#
# password = input("Şifre giriniz:")
# fileName = input("İşlem yapmak istediğiniz dosya ismini giriniz: ")
#
# if command == "E":
#     cl.EncryptFile(fileName,password)
# elif command== "D" :
#     cl.DecryptFile(fileName,password)
