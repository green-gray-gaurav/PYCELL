#here we are going to implemt the notebook
from collections import defaultdict
from importlib.resources import contents
import os

class OutputFunction:
    """A picklable callable class that stores output in notebook cells."""
    # Global registry to map notebook paths to instances
    _notebook_registry = {}
    
    def __init__(self, notebook_instance, line_index, index):
        self.notebook_path = notebook_instance.notebook_path
        self.line_index = line_index
        self.index = index
        # Register this notebook instance
        OutputFunction._notebook_registry[notebook_instance.notebook_path] = notebook_instance
    
    def __call__(self, *args):
        args = [str(a) for a in args]
        # Get notebook instance from registry
        notebook_instance = OutputFunction._notebook_registry.get(self.notebook_path)
        if notebook_instance:
            notebook_instance.cells[self.line_index][self.index]['output'] = " ".join(args)
    
    def __getstate__(self):
        # Only pickle the data needed to recreate, not the notebook instance
        return {
            'notebook_path': self.notebook_path,
            'line_index': self.line_index,
            'index': self.index
        }
    
    def __setstate__(self, state):
        self.notebook_path = state['notebook_path']
        self.line_index = state['line_index']
        self.index = state['index']

class notebook():
    BASE_DIR = "NOTEBOOKS"

    def __init__(self , notebook_name):

        self.cells = defaultdict(dict)
        self.notebook_name = notebook_name
        self.notebook_path = f"{notebook.BASE_DIR}/{self.notebook_name}"

        #constants
        self.notebook_stamp = "cell"

        #initaliliztions
        import os
        if(not os.path.exists(self.notebook_path)):
            os.mkdir(self.notebook_path)

    
        pass
 
    def rename_notebook(self , new_name):
        #change the folder name
        import os
        os.rename(self.notebook_path, f"{notebook.BASE_DIR}/{new_name}")
        self.notebook_path = f"{notebook.BASE_DIR}/{new_name}"
        

    def create_cell(self , line_index , index = 0 , prev_index = 0):
        
        self.cells[line_index][index] = {
            'previous_index' : prev_index,
            'code' : None,
            'output' : None 
        }

       

    def delete_cell(self ,line_index , index):
        # delete from RAM
        del self.cells[line_index][index]
        # delete from disk
        import os
        cell_file = f"{self.notebook_path}/{self.notebook_stamp}_{line_index}_{index}.pkl"
        if(os.path.exists(cell_file)):
            os.remove(cell_file)
        
        pass
    def update_cell_code(self ,line_index , index,  code):
        self.cells[line_index][index]['code'] = code
        pass

    def update_cell_connection(self , line_index , index , prev_index):
        self.cells[line_index][index]['previous_index'] = prev_index
        pass
    
    def to_json(self):
        import json
        data = {
            "notebook_name": self.notebook_name,
            "notebook_stamp": self.notebook_stamp,
            "cells": []
        }
        for line_index, line in self.cells.items():
            for index, cell in line.items():
                cell_dict = {}
                cell['location'] = [line_index , index]
                cell_dict[f"{line_index}_{index}"] = cell
                data["cells"].append(cell_dict)
        with open(f"{self.notebook_path}/note_loader.json" , "w") as file:
            file.write(json.dumps(data))
    def clean(self):
        import glob ,os
        files = glob.glob(f"{self.notebook_path}/*")
        for file in files:
            name_ext = file.split('\\')[-1].split('.')
            if(name_ext[1] == 'pkl'):
                l , i = name_ext[0].split('_')[1:]
                if not self.cells.get(int(l)):
                    os.remove(file)
                    pass
                else:
                    if not self.cells.get(int(l)).get(int(i)):
                        os.remove(file)
                        pass


    def from_json(self):
        #flush the cells
        self.cells = defaultdict(dict)
        #flush the evnirmonemt
        self.exec_env = {}

        import json
        with open(f"{self.notebook_path}/note_loader.json" , "r") as file:
            data = json.load(file)
            self.notebook_name = data["notebook_name"]
            self.notebook_stamp = data["notebook_stamp"]
            data_cells = data["cells"]

            for cell_data in data_cells:

                cell_attrs = list(cell_data.values())[0]
                content = cell_attrs['code']
                cell_loc = cell_attrs['location']
                cell_ind_prev = cell_attrs['previous_index']
                cell_out = cell_attrs['output']

                self.create_cell(cell_loc[0], cell_loc[1], cell_ind_prev)
                self.update_cell_code(cell_loc[0], cell_loc[1], content)
                self.cells[cell_loc[0]][cell_loc[1]]['output'] = cell_out


    def run_cell(self , line_index, index):
        
        code = self.cells[line_index][index]['code']
        prev_index = self.cells[line_index][index]['previous_index']


        if(self.notebook_path!=""):#if notebookexits
            import pickle
            env = {}
            if(line_index > 0):
                with open(f"{self.notebook_path}/{self.notebook_stamp}_{line_index-1}_{prev_index}.pkl", "rb") as f:
                    env = pickle.load(f)
                    # Recreate output function if it was pickled (it will be an OutputFunction instance)
                    if 'output' in env and isinstance(env['output'], OutputFunction):
                        # Update registry and recreate with current cell info
                        OutputFunction._notebook_registry[self.notebook_path] = self
                        env['output'] = OutputFunction(self, line_index, index)
            # Create output function for this cell
            output = OutputFunction(self, line_index, index)    
            return [code , env , output]
        
        else :
            print("specify the name of notebook")

        pass



    def execute_cell(self , line_index , index) :
        code , env ,  output = self.run_cell(line_index , index)
        env['output'] = output
        exec(code , env, env)

        import pickle
        with open(f"{self.notebook_path}/{self.notebook_stamp}_{line_index}_{index}.pkl", "wb") as f:
            pickle.dump(env, f)
        pass
    

    def flush_output(self, line_index , index):
        self.cells[line_index][index].cell_output = ""


    def get_cell(self , line_index , index):
        return self.cells[line_index][index]


    def get_cells(self): return len(self.cells)

    #only debugging
    def print(self):
        for c in self.cells:
            print(c.content)
    def get_name (self):
        return self.notebook_name
    def set_name (self , name):
        self.notebook_name = name   




n = notebook(notebook_name="test")





