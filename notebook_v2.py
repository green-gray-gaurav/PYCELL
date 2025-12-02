#here we are going to implemt the notebook
from collections import defaultdict
class notebook():
    # from utils import checktype , get_tokens
    class cell():
        def __init__(self , line_index = -1 , index= 0 , prev_index = 0):
            self.content = ""
            self.cell_location = [line_index , index]
            self.cell_location_prev = [line_index -1 , prev_index]
            self.cell_output = ""
            self.token_maping = {}
            pass

    def __init__(self , notebook_name):
        self.cells = defaultdict(dict)
        self.notebook_path = notebook_name
        
        #contants
        self.notebook_stamp = "cell"
        self.BASE = "import dill"
        self.LOAD = lambda s : f"dill.load_session('{s}')"
        self.OVERRIDE = lambda s : f"dill.dump_session('{s}')"

        #initaliliztions
        
        import os
        if(not os.path.exists(self.notebook_path)):
            os.mkdir(self.notebook_path)

        
    def load_notebook(self):
        import os
        if(not os.path.exists(f"{self.notebook_path}/note_loader.pkl")): return None
        import dill
        with open(f"{self.notebook_path}/note_loader.pkl" , "rb") as file:
            attr_dict = dill.load(file)
            for (k, v) in attr_dict.items():
                setattr(self, k, v)
        pass
    def save_notebook(self):
        import dill
        with open(f"{self.notebook_path}/note_loader.pkl" , "wb") as file:
            dic = vars(self)
            dill.dump({'cells': dic['cells'], 'notebook_path': dic['notebook_path']}, file)

        pass
    def create_cell(self , line_index , index =0 , prev_index = 0):
        # self.cells.insert(cell_index , notebook.cell(cell_index))
        self.cells[line_index][index] = notebook.cell(line_index , index, prev_index)
        
        pass
    def delete_cell(self ,line_index , index):
        del self.cells[line_index][index]
        
        pass
    def update_cell_content(self ,line_index , index,  content):
        self.cells[line_index][index].content = content
        pass

    def update_cell_connection(self , line_index , index , prev_index):
        self.cells[line_index][index].cell_location_prev = [line_index -1 , prev_index]
        pass
    def run_cell(self , line_index, index):

        content = self.cells[line_index][index].content
        _ , prev_index = self.cells[line_index][index].cell_location_prev


        if(self.notebook_path!=""):#if notebookexits
            override = f"{self.notebook_path}/{self.notebook_stamp}_{line_index}_{index}"
            exec_file = ""
            if(line_index==0):
                exec_file = f"{self.BASE}\n{content}\n{self.OVERRIDE(override)}"
            else:
                load = f"{self.notebook_path}/{self.notebook_stamp}_{line_index-1}_{prev_index}"
                exec_file = f"{self.BASE}\n{self.LOAD(load)}\n{content}\n{self.OVERRIDE(override)}"
            
            return [exec_file , self.get_cell_output(line_index=line_index , index=index)]
        
        else :
            print("specify the name of notebook")

        pass


    # def get_token_info(self , id ,globs):
    #     l = notebook.get_tokens(self.cells[id].content)
    #     m = map(lambda s : [s , notebook.checktype(s , globs)] , l)
    #     l = list(m)
    #     self.cells[id].token_maping = l
       
        pass
    def get_cell_output(self , line_index , index):
        def output(*args):
            args = [str(a) for a in args]
            self.cells[line_index][index].cell_output = " ".join(args)
        return output
    

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
        return self.notebook_path
    def set_name (self , name):
        self.notebook_path = name   





# n = notebook(notebook_name="my_book")
# n.load_notebook()

# code , o = n.run_cell(0,0)
# exec( code )
# print(o())
# code , o = n.run_cell(1,0)
# exec( code )
# print(o())

# code , o = n.run_cell(1,1)
# exec( code )
# print(o())

