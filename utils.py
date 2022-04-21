import requests
import csv
import re
import pathlib
from RPA.Robocorp.WorkItems import WorkItems
import logging

class Utils:

    @staticmethod
    def save_image(image_src, image_filename, folder_to_save):
        path_to_saved_image = str(pathlib.Path(folder_to_save).joinpath(image_filename).resolve())
        with open(str(path_to_saved_image), 'wb') as handle:
            response = requests.get(image_src, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

    @staticmethod
    def write_result_to_file(data, headers):
        with open('result.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for item in data:
                writer.writerow(item)

    @staticmethod
    def get_image_name(src):
        split_item = None
        if ".jpg" in src:
            split_item = ".jpg"
        elif ".png" in src:
            split_item = ".png"
        else:
            return None
        if split_item is not None:
            return src.split(".jpg")[0].split("/")[-1] + ".jpg"

    @staticmethod
    def check_text_on_money_occurrence(input_str):
        regex = r"(\$\d+(?:\,?\d+)*(?:\.?\d+))|(\d+\s*dollar(?:s)?)|(\d+\s*USD)"
        return True if re.search(regex, input_str) is not None else False

    @staticmethod
    def get_input_vars():
        items = WorkItems()
        items.get_input_work_item()
        variables = items.get_work_item_variables()
        for variable, value in variables.items():
            print(f"{variable} = {value}")
