#here we are going to implemt the notebook
class notebook():
    from utils import checktype , get_tokens
    class cell():
        def __init__(self , index = -1):
            self.content = ""
            self.cell_index = index
            self.cell_output = ""
            self.token_maping = {}
            pass

    def __init__(self , notebook_name):
        self.cells = []
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
        import pickle
        with open(f"{self.notebook_path}/note_loader.pkl" , "rb") as file:
            attr_dict = pickle.load(file)
            for (k,v) in attr_dict.items():
                print(k,v)
                if(k=="cells"):
                    for c in v:
                        print("----------------------")
                        print(c._dict_)
                self._setattr_(k , v)
        pass
    def save_notebook(self):
        import pickle
        with open(f"{self.notebook_path}/note_loader.pkl" , "wb") as file:
            dic = vars(self)
            
            pickle.dump( {'cells' : dic['cells'] , 'notebook_path' : dic['notebook_path']}, file)

        pass
    def create_cell(self ,cell_index):
        self.cells.insert(cell_index , notebook.cell(cell_index))
        self.update_indices()
        pass
    def delete_cell(self ,cell_index):
        self.cells.pop(cell_index)
        self.update_indices()
        pass
    def update_cell_content(self ,cell_index , content):
        self.cells[cell_index].content = content
        pass
    def run_cell(self , cell_index):

        content = self.cells[cell_index].content
        if(self.notebook_path!=""):#if notebookexits
            override = f"{self.notebook_path}/{self.notebook_stamp}{cell_index}"
            exec_file = ""
            if(cell_index==0):
                exec_file = f"{self.BASE}\n{content}\n{self.OVERRIDE(override)}"
            else:
                load = f"{self.notebook_path}/{self.notebook_stamp}{cell_index-1}"
                exec_file = f"{self.BASE}\n{self.LOAD(load)}\n{content}\n{self.OVERRIDE(override)}"
            #     print(load) 
            # print(exec_file)
            # print(override)
            self.update_indices()
            return [exec_file , self.get_cell_output(cell_index)]
        
        else :
            print("specify the name of notebook")

        pass


    def get_token_info(self , id ,globs):
        l = notebook.get_tokens(self.cells[id].content)
        m = map(lambda s : [s , notebook.checktype(s , globs)] , l)
        l = list(m)
        self.cells[id].token_maping = l
       
        pass
    def get_cell_output(self , index):
        def output(*args):
            args = [str(a) for a in args]
            self.cells[index].cell_output = " ".join(args)
        return output
    def flush_output(self, index):
        self.cells[index].cell_output = ""
    def get_cell(self , index):
        return self.cells[index]
    def update_indices(self):
        for i , c in enumerate(self.cells): c.cell_index = i

    def get_cells(self): return len(self.cells)
    #only debuggin
    def print(self):
        for c in self.cells:
            print(c.content)




print(dir())
n = notebook(notebook_name="my_book")
# n.load_notebook()

n.create_cell(-1)
n.update_cell_content(-1 , "a=20\nb=30\nprint(dir())")

n.create_cell(n.get_cells())
n.update_cell_content(n.get_cells()-1 , "\nprint(a)")

# def make()
code , output = n.run_cell(0)
print(code)
exec(code )
code , output = n.run_cell(1)
exec(code)
print(output)