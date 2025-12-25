import glob
import coolprint
import shutil
import os
import re


class NoteBookManager():
    def __init__(self , path):
        self.notebooks_path = path
        pass
    def list_notebooks(self):
        files = glob.glob(f'{self.notebooks_path}/*')
        list_str = "\n".join(map(lambda x : x.split('\\')[1] , files))
        coolprint.print_section("NOTEBOOKS" , list_str)

    def delete_notebook(self, name):
        path = os.path.join(self.notebooks_path, name)

        if not os.path.exists(path):
            print(f"Notebook '{name}' not found")
            return

        try:
            shutil.rmtree(path)
            print(f"Notebook '{name}' deleted")
        except Exception as e:
            print(f"Failed to delete '{name}': {e}")

    def search_notebook(self, pattern, ignore_case=True):
        

        flags = re.IGNORECASE if ignore_case else 0

        try:
            regex = re.compile(pattern, flags)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")

      
        files = glob.glob(f"{self.notebooks_path}/*")

        list_str = ""
        for path in files:
            name = path.split('\\')[1]
            if regex.search(name):
                list_str += name +"\n"

        coolprint.print_section(f"{pattern} matches " , list_str)

        

