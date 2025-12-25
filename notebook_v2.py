#here we are going to implemt the notebook
from collections import defaultdict
from importlib.resources import contents
import os
import copy
import traceback
import builtins
import json
import coolprint

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
            notebook_instance.cells[self.line_index][self.index]['output'] += " ".join(args) + '\n'
    
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
    STATUS_INVALID = 0
    STATUS_MODIFIED = 1
    STATUS_VALID = 2


    def __init__(self , notebook_name):

        self.cells = defaultdict(dict)
        
        self.notebook_name = notebook_name
        self.notebook_path = f"{notebook.BASE_DIR}/{self.notebook_name}"

        #constants
        self.notebook_stamp = "cell"

        #sequencer
        self.line_sequencer = 0
        self.index_sequencer = 0


        #
        self.ROOT = None
        self.END = None

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
        

    def create_cell(self , line_index , prev_line , next_line , index = 0, prev_index = 0 , next_index = 0 , status = None):
        
        self.cells[line_index][index] = {
            'previous_index' : prev_index,
            'previous_line' : prev_line,
            'next_line' : next_line,
            'next_index' : next_index,
            'code' : None,
            'output' : None,
            'status' : notebook.STATUS_INVALID if status == None else status
        }
    
    def insert_at_end(self):

        if len(self.cells.keys()) == 0:
            self.create_cell(line_index= self.line_sequencer  ,
                             prev_line=None ,
                             next_line=None ,
                             index= self.index_sequencer)
            self.ROOT = [0 , 0]
            self.END =  [0 , 0]

        else:
            print(self.END)
            pl , pi = self.END

            self.cells[pl][pi]['next_line'] = self.line_sequencer
            self.cells[pl][pi]['next_index'] = self.index_sequencer

            self.create_cell(line_index= self.line_sequencer  ,
                    prev_line=pl ,
                    prev_index= pi,
                    next_line=None ,
                    index= self.index_sequencer)
        

            self.END = [self.line_sequencer , self.index_sequencer]
            
        self.line_sequencer+=1




        pass

    def insert_at_start(self):
        if len(self.cells.keys()) == 0:
            self.create_cell(line_index= self.line_sequencer  ,
                             prev_line=None ,
                             next_line=None ,
                             index= self.index_sequencer)
            self.ROOT = [0 , 0]
            self.END =  [0 , 0]
        else:
            pl , pi = self.ROOT

            self.cells[pl][pi]['previous_line'] = self.line_sequencer
            self.cells[pl][pi]['previous_index'] = self.index_sequencer

            self.create_cell(line_index= self.line_sequencer  ,
                    prev_line=None ,
                    next_line=pl ,
                    next_index=pi,
                    index= self.index_sequencer)
            

            self.ROOT = [self.line_sequencer , self.index_sequencer]
            
        self.line_sequencer+=1

    
    def insert_next(self , line_index , index):

        #---------------check existance-------------
        if self.cells.get(line_index) == None :
            return 
        
        if self.cells.get(line_index).get(index) == None:
            return
        


        if self.END[0] == line_index and self.END[1] == index:
            self.insert_at_end()
        
        else:

            nl = self.cells[line_index][index]['next_line']
            ni = self.cells[line_index][index]['next_index']

            self.cells[line_index][index]['next_line'] = self.line_sequencer
            self.cells[line_index][index]['next_index'] = self.index_sequencer

            self.cells[nl][ni]['previous_line'] = self.line_sequencer
            self.cells[nl][ni]['previous_index'] = self.index_sequencer

            self.create_cell(line_index= self.line_sequencer  ,
                        prev_line=line_index ,
                        prev_index=index,
                        next_line=nl ,
                        next_index=ni,
                        index= self.index_sequencer)

            self.line_sequencer +=1  

    
    def create_cell_version(self  , line):
        if self.cells.get(line) != None:
            self.index_sequencer += 1

            pl = self.cells[line][0]['previous_line']
            pi = self.cells[line][0]['previous_index']

            nl = self.cells[line][0]['next_line']
            ni = self.cells[line][0]['next_index']  
            
            self.create_cell(line , pl , nl , index = self.index_sequencer , prev_index= pi , next_index= ni )
    

    def is_cell_version_active(self , line , index):

        if self.cells.get(line) != None:
            if self.cells.get(line).get(index) != None:

                pl = self.cells[line][index]['previous_line']
                pi = self.cells[line][index]['previous_index']

                nl = self.cells[line][index]['next_line']
                ni = self.cells[line][index]['next_index']

                #------------if cell is first-------------

                if pl == None and nl == None:
                    return self.ROOT[0] == line and self.ROOT[1] == index

                if pl == None :
                    if self.cells[nl][ni]['previous_line'] == line \
                    and self.cells[nl][ni]['previous_index'] == index:
                        return  True
                    
                if self.cells[pl][pi]['next_line'] == line \
                and self.cells[pl][pi]['next_index'] == index:
                    return  True
                
                return False
            
        return None

    
    def delete_cell_version(self, line , index):
        if self.cells.get(line) != None:
            if self.cells.get(line).get(index) != None:

                if self.is_cell_version_active(line , index):
                    print('DELETION FAILED : cell version is active')
                    return 
                
                # else we can remve this
                del self.cells[line][index]

                # # delete from disk
                # import os
                # cell_file = f"{self.notebook_path}/{self.notebook_stamp}_{line}_{index}.pkl"
                # cell_import_file = f"{self.notebook_path}/{self.notebook_stamp}_{line}_{index}.json"
                
                # if(os.path.exists(cell_file)):
                #     os.remove(cell_file)

                # if(os.path.exists(cell_import_file)):
                #     os.remove(cell_import_file)
    
                
    
    def switch_to_cell_version(self , line , index):

        if self.cells.get(line) != None:
            if self.cells.get(line).get(index) != None:
                
                pl = self.cells[line][index]['previous_line']
                # pi = self.cells[line][index]['previous_index']

                nl = self.cells[line][index]['next_line']
                # ni = self.cells[line][index]['next_index']

                if pl == None: #change the root
                    self.ROOT = [line , index]
                
                if nl == None : #change the end
                    self.END = [line , index]


                if pl != None :

                    # self.cells[pl][pi]['next_line'] = line
                    # self.cells[pl][pi]['next_index'] = index
                    for cell_i in self.cells[pl].keys():
                        self.cells[pl][cell_i]['next_line'] =  line
                        self.cells[pl][cell_i]['next_index'] =  index
                    print(pl)

                if nl != None:

                    # self.cells[nl][ni]['previous_line'] = line
                    # self.cells[nl][ni]['previous_index'] = index
                    for cell_i in self.cells[nl].keys():
                        self.cells[nl][cell_i]['previous_line'] =  line
                        self.cells[nl][cell_i]['previous_index'] =  index
                    print(nl)

                return 
        
        print("ERROR at switching") 




    def delete_cell(self , line_index , index):

        if self.is_cell_version_active(line_index , index) == True:

            #get the previoud and next links
            pl = self.cells[line_index][index]['previous_line']
            pi = self.cells[line_index][index]['previous_index']

            nl = self.cells[line_index][index]['next_line']
            ni = self.cells[line_index][index]['next_index']


            # delete from RAM
            del self.cells[line_index]

            
            #reconfigure the links
            if pl != None:
                self.cells[pl][pi]['next_line'] = nl
                self.cells[pl][pi]['next_index'] = ni

            if nl != None:
                self.cells[nl][ni]['previous_line'] = pl
                self.cells[nl][ni]['previous_index'] = pi

            # configure root / end

            if pl == None:
                if nl == None:
                    self.ROOT = None  # no root
                    self.END = None
                else:
                    self.ROOT = [nl , ni]
            else :
                if nl == None:
                    self.END = [pl , pi]  # no root
                else:
                    pass        


            # delete from disk
            # import os
            # cell_file = f"{self.notebook_path}/{self.notebook_stamp}_{line_index}_{index}.pkl"
            # cell_import_file = f"{self.notebook_path}/{self.notebook_stamp}_{line_index}_{index}.json"
            # if(os.path.exists(cell_file)):
            #     os.remove(cell_file)

            # if(os.path.exists(cell_import_file)):
            #     os.remove(cell_import_file)
                
            
            pass
        else :
            print('cell is not in its active version')

    def update_cell_code(self , line_index , index ,  code):
        self.cells[line_index][index]['status'] = notebook.STATUS_MODIFIED
        self.cells[line_index][index]['code'] = code
        pass

    def update_cell_connection(self , line_index , index , prev_line ,prev_index  , next_line , next_index):
        
        self.cells[line_index][index]['previous_index'] = prev_index
        self.cells[line_index][index]['previous_line'] = prev_line
        self.cells[line_index][index]['next_line'] = next_line
        self.cells[line_index][index]['next_index'] = next_index
        
        pass
    
    def to_json(self):

        import json
        data = {
            "notebook_name": self.notebook_name,
            "notebook_stamp": self.notebook_stamp,
            "root" : self.ROOT,
            "end" : self.END,
            'lseq' : self.line_sequencer,
            'iseq' : self.index_sequencer,
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
            f_name = file.split('\\')[-1]
            stamp = f_name.split('_')[0]
            name_ext = f_name.split('.')

            if(stamp == self.notebook_stamp): # cell type files

                l , i = name_ext[0].split('_')[1:]
                if not self.cells.get(int(l)):
                    os.remove(file)
                    pass
                else:
                    if not self.cells.get(int(l)).get(int(i)):
                        os.remove(file)
                        pass
           
    
    def save_notebook(self):
        self.to_json()
        self.clean()
        pass


    def from_json(self):
        import os
        if(not os.path.exists(f"{self.notebook_path}/note_loader.json")):
            print('NOTHING TO LOAD')
            return
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
            self.ROOT = data['root']
            self.END = data['end']
            self.line_sequencer = data['lseq']
            self.index_sequencer = data['iseq']


            for cell_data in data_cells:

                cell_attrs = list(cell_data.values())[0]
                content = cell_attrs['code']
                cell_loc = cell_attrs['location']
                cell_ind_prev = cell_attrs['previous_index']
                cell_line_prev = cell_attrs['previous_line']
                cell_line_next = cell_attrs['next_line']
                cell_ind_next = cell_attrs['next_index']
                cell_out = cell_attrs['output']
                cell_status = cell_attrs['status']

        


                self.create_cell(line_index= cell_loc[0], index= cell_loc[1], prev_line= cell_line_prev ,  prev_index = cell_ind_prev , next_index= cell_ind_next , next_line= cell_line_next)

                self.update_cell_code(cell_loc[0], cell_loc[1], content)

                self.cells[cell_loc[0]][cell_loc[1]]['output'] = cell_out
                self.cells[cell_loc[0]][cell_loc[1]]['status'] = cell_status



    def __handle_cell_imports(self ,env, line , index ,  save=True):
        """
        Save or load & replay imports for a notebook cell.
        
        Parameters:
        - env: dict, the cell environment
        - notebook_path: str, directory to store imports
        - notebook_stamp: str, notebook identifier
        - cell_index: int, index of the cell
        - save: bool, True to save imports, False to load & replay
        """
        filepath = f"{self.notebook_path}/{self.notebook_stamp}_{line}_{index}.json"
        
        if save:
            # Save current tracked imports to JSON
            imports = env.get('_imports', [])
            with open(filepath, "w") as f:
                json.dump(imports, f, indent=2)
        else:
            # Load imports from JSON and replay them
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    tracked_imports = json.load(f)
                
                import_str = ""
                for stmt in tracked_imports:
                    import_str += f"{stmt}\n"
                return import_str
                    



    def run_cell(self , line_index, index):
        if self.cells.get(line_index) == None or self.cells.get(index) == None:
            print('cell/version must exist')
            return None

        
        code = self.cells[line_index][index]['code']


        prev_line = self.cells[line_index][index]['previous_line']
        prev_index = self.cells[line_index][index]['previous_index']

        # next_line = self.cells[line_index][index]['next_line']
        # next_index = self.cells[line_index][index]['next_index']

        import_str = ""


        if(self.notebook_path!=""):#if notebookexits
            import pickle
            env = {}
            if(prev_line != None):
                if not os.path.exists(f"{self.notebook_path}/{self.notebook_stamp}_{prev_line}_{prev_index}.pkl"):
                    print(f'Cell execution depends on previous cell {prev_line}_{prev_index} | previous cell must execute atleast once')
                    return None

                with open(f"{self.notebook_path}/{self.notebook_stamp}_{prev_line}_{prev_index}.pkl", "rb") as f:
                    env = pickle.load(f)
                    # Recreate output function if it was pickled (it will be an OutputFunction instance)
                    if 'output' in env and isinstance(env['output'], OutputFunction):
                        # Update registry and recreate with current cell info
                        OutputFunction._notebook_registry[self.notebook_path] = self
                        env['output'] = OutputFunction(self, line_index, index)
                

                if os.path.exists(f"{self.notebook_path}/{self.notebook_stamp}_{prev_line}_{prev_index}.json"):
                        #-------------------load the imports---------------------------
                    import_str = self.__handle_cell_imports(None  , prev_line , prev_index , save=False)
                

            # Create output function for this cell
            output = OutputFunction(self, line_index, index)  
            
            return [import_str , code , env , output]
        
        else :
            print("specify the name of notebook")
            return None
        pass



    def execute_cell(self , line_index , index) :
        S_D = self.run_cell(line_index , index)
        if S_D == None :
            return 
        
        im_str , code , env ,  output = S_D

        env['output'] = output

        if code == None :
            print('Cell is Empty')
            return

        # exec(code , env, env)

        try:

            #---------------------------------track the imports-----------------------------------------
            env['_imports'] = []

            real_import = builtins.__import__

            def tracking_import(name, globals=None, locals=None, fromlist=(), level=0):
                if fromlist:
                    env['_imports'].append(f"from {name} import {', '.join(fromlist)}")
                else:
                    env['_imports'].append(f"import {name.split('.')[0]}")
                return real_import(name, globals, locals, fromlist, level)

            if '__builtins__' not in env:
                env['__builtins__'] = builtins.__dict__.copy()

            env['__builtins__']['__import__'] = tracking_import



            #-----------------flush the output buffer------------------
            self.flush_output(line_index , index)

            #--------------------execute the cell-----------------------


            exec(im_str + code, env, env)
            self.cells[line_index][index]['status'] = notebook.STATUS_VALID


            #-------------------save the imports---------------------------
            self.__handle_cell_imports(env  , line_index , index , save=True)



        except Exception as e:
            print(f"\n Error in cell [{line_index}, {index}]")
            print("-" * 40)
            traceback.print_exc()
            print("-" * 40)
            return   # stop execution, don’t save env


        import pickle
        with open(f"{self.notebook_path}/{self.notebook_stamp}_{line_index}_{index}.pkl", "wb") as f:
            
            
            #clean -------------remove modules
            import types

            clean = {}
            for k, v in env.items():
                if k == '__builtins__':
                    continue
                if isinstance(v, types.ModuleType):
                    continue
                clean[k] = v

            pickle.dump(clean, f)
        pass
    

    def flush_output(self, line_index , index):
        self.cells[line_index][index]['output'] = ""


    def get_cell(self , line_index , index):
        return self.cells[line_index][index]


    def get_cells(self): return len(self.cells)


    def is_root(self , line , index):
        if self.cells.get(line) != None:
            if self.cells.get(index) != None:
                return self.cells[line][index]['previous_line'] == None
        return None
    
    #notebook printer
    def print_notebook(self):
        #get the root cell
        root = self.ROOT

        if root == None: 
            print("NOTE BOOK IS EMPTY")
            return
        #traverse the whole graph from the 
        ptr_line , ptr_index = root
        while ptr_line != None:
            self.print_cell(ptr_line , ptr_index)

            ni = self.cells[ptr_line][ptr_index]['next_index']
            nl = self.cells[ptr_line][ptr_index]['next_line'] 
            
            ptr_index = ni
            ptr_line = nl
        pass


    #only debugging
    def print(self):
        for c in self.cells:
            print(c.content)
    def get_name (self):
        return self.notebook_name
    def set_name (self , name):
        self.notebook_name = name   

    def print_cell(self, line, index):
        cell = self.cells[line][index]

        # pi, pl = cell['previous_index'], cell['previous_line']
        # ni, nl = cell['next_index'], cell['next_line']


        code = str(cell['code']).strip()
        output = str(cell['output']).strip()
        status = cell['status']

        status_str = None
        color_ = None
        if status == notebook.STATUS_MODIFIED : 
            status_str = '*'
            color_ = coolprint.C.YELLOW
        if status == notebook.STATUS_VALID: 
            status_str = '~'
            color_ = coolprint.C.fg256(120) #light green
        if status == notebook.STATUS_INVALID: 
            status_str = '?'
            color_ = coolprint.C.BRIGHT_RED


        
        cell_versions = list(self.cells[line].keys())

        width = 120

        # def box(title):
        #     print(f"╔{'═' * (width-2)}╗")
        #     print(f"║ {title.center(width-4)} ║")
        #     print(f"╚{'═' * (width-2)}╝")

        # def content(text):
        #     for line in text.splitlines():
        #         print(f"│ {line[:width-4].ljust(width-4)} │")

        # # Header
        # box(f" CELL [{line},{index}] ({status_str})")

        # print(f" Previous → ({pl},{pi})")
        # print(f" Next     → ({nl},{ni})")
        # print("")

        # Code block
        # print("┌" + "─" * (width-2) + "┐")
        # print("│ CODE".ljust(width-1) + "│")
        # print("├" + "─" * (width-2) + "┤")
        # content(code)
        # print("└" + "─" * (width-2) + "┘")


        # # version block
        # print("┌" + "─" * (width-2) + "┐")
        # # print("│ CVS".ljust(width-1) + "│")
        cv_str = " ".join(map( lambda x : str(x)+"v" if x != index else f"[{index}]v" , cell_versions))
        # content("CVS: "+cv_str)
        # # content(output)
        # print("└" + "─" * (width-2) + "┘")

        # # Output block
        # print("┌" + "─" * (width-2) + "┐")
        # print("│ OUTPUT".ljust(width-1) + "│")
        # print("├" + "─" * (width-2) + "┤")
        # content(output)
        # print("└" + "─" * (width-2) + "┘")


        coolprint.print_box_title(f" CELL [{line},{index}] ({status_str})" ,fg =  coolprint.C.fg256(208) , bg = coolprint.C.BG_BLACK)
        coolprint.print_box_text("CVS: " + cv_str , italic = True)
        coolprint.print_section("CODE" , code , fg=color_ , italic = True)
        coolprint.print_section("OUTPUT" , output , fg=color_ , italic = True)



    def execute_n_cell(self, line = None , index = None , n_cells  = None):
        #get the root cell
        root = self.ROOT

        if line != None and index!= None :
            root = [line , index]
        
        if root == None: 
            print("NOTE BOOK IS EMPTY")
            return
        #traverse the whole graph from the 
        ptr_line , ptr_index = root
        while ptr_line != None:
            if n_cells != None  and n_cells == 0: break 
            if n_cells != None : n_cells -=1

            self.execute_cell(ptr_line , ptr_index)
            

            ni = self.cells[ptr_line][ptr_index]['next_index']
            nl = self.cells[ptr_line][ptr_index]['next_line'] 
            
            ptr_index = ni
            ptr_line = nl

            
        pass

    def execute_n_cell_versions(self, line):
        #---------------get the root cell-------------------
        for cell_version_id in self.cells[line].keys():
            self.execute_cell(line , cell_version_id)

            

    
# while True:
#     data = input('>> ').strip()
#     command , line , index = data.split(' ')
#     if command == 'add':
#         n.insert_at_end()
#         pass
#     if command == 'delete':
#         n.delete_cell(line , index)
    
#     if command == 'exe':
#         n.execute_cell(line, index)
#     if command == 'q':
#         break

# n.to_json()




