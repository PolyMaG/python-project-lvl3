import os
import re
import requests


def change_file_name(old_name):
    if old_name[:5] == 'https':
        path = old_name[8:]
    else:
        path = old_name[7:]
    new_path = re.sub(r'\W', '-', path)
    return new_path + '.html'


def get_page(source, output_path):
    new_name = change_file_name(source)
    source_data = requests.get(source)
    output_full_path = os.path.join(output_path, new_name)
    with open(output_full_path, 'w') as saved_file:
        saved_file.write(source_data.text)
    return output_full_path
