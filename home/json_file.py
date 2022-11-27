import json


class JsonFile:

    @staticmethod
    def read(file_name):
        with open(file_name,"r",encoding="utf-8") as file_object:
            try:
                file_object.seek(0)
                dict_data =json.load(file_object)
            except:
                dict_data={}

        return dict_data

    @staticmethod
    def write(file_name,dict_data):
        with open(file_name,"w",encoding="utf-8") as file_object:
            file_object.write(json.dumps(dict_data,indent=4))
