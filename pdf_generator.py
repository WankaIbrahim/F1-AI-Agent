import os
import requests

file_names = ["constructors.txt", "drivers.txt", "grand_prix.txt"]

baseurl = "https://en.wikipedia.org/api/rest_v1/page/pdf/"


def download_pdf_files():
    txt_list = []
    for file_name in file_names:
        with open(os.path.join("data", file_name), "r") as txt_file:
            lines = txt_file.readlines()
            for line in lines:
                line = line.replace(" ", "_")
                line = line.replace("\n", "")
                txt_list.append(line)

    for line in txt_list:
        pdf_file_path = line + ".pdf"
        file_name = line.replace(" ", "_")


        response = requests.get(baseurl + file_name, stream=True)
        
        with open(os.path.join("data", "wiki_files", pdf_file_path), "wb") as pdf_file:
            for chunk in response.iter_content(chunk_size=4096):
                if chunk:
                    pdf_file.write(chunk)


download_pdf_files()
