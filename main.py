import argparse
import shlex
from notebook_v2 import notebook
import tempfile
import subprocess
import os
from NM import NoteBookManager

def open_notepad(existing_code=""):
    with tempfile.NamedTemporaryFile(
        suffix=".py",
        delete=False,
        mode="w",
        encoding="utf-8"
    ) as f:
        f.write(existing_code)   # ⭐ write old code first
        path = f.name

    subprocess.call(["notepad.exe", path])

    with open(path, encoding="utf-8") as f:
        code = f.read()

    os.unlink(path)
    return code




parser = argparse.ArgumentParser(prog="")
sub = parser.add_subparsers(dest="command")

# add
add_p = sub.add_parser("add")
add_p.add_argument(
    'at',
    nargs='?',      # makes it optional
    default='e',    # default value
    choices=['e', 's' , 'a'],
    help="e = end, s = start, a = after"
)
add_p.add_argument(
    'pos',
    nargs='*',
    type=int,
    help="position arguments (required for a)"
)


# delete
del_p = sub.add_parser("del")
del_p.add_argument("line", type=int)
del_p.add_argument("index", type=int)

# exe

exe_p = sub.add_parser("exe")
# exe_p.add_argument("line", type=int)
# exe_p.add_argument("index", type=int)
exe_p.add_argument(
    'pos',
    nargs='*',
    type=int,
    help="cell location (required for execution)"
)

# show
show_p = sub.add_parser("show")
show_p.add_argument(
    'com',
    nargs='?',      # makes it optional
    default='c',    # default value
    choices=['c'],
    help="c : clear"
)

# save
sub.add_parser("save")

# load
sub.add_parser("load")

# clear
sub.add_parser("c")


# switch
switch_p = sub.add_parser("sw")
switch_p.add_argument(
    'com',
    nargs='?',      # makes it optional
    default='n',    # default value
    choices=['n' , 'c' , 'l'],
    help="n : none, l : load, c : clear"
)

switch_p.add_argument("name" , type=str)



# code
code_p = sub.add_parser("code")
code_p.add_argument("line" , type=int)
code_p.add_argument("index" , type=int)



# switch cell version
switch_cv_p = sub.add_parser("v")
# switch_cv_p.add_argument("line" , type=int)
# switch_cv_p.add_argument("index" , type=int)
switch_cv_p.add_argument(
    'com',
    nargs='?',      # makes it optional
    default='a',    # default value
    choices=['d' , 'a' , 's'],
    help="d : delete, a : add, s : switch"
)
switch_cv_p.add_argument(
    'pos',
    nargs='*',
    type=int,
    help="position arguments (required for a)"
)

# create cell version
switch_crv_p = sub.add_parser("cv")
switch_crv_p.add_argument("line" , type=int)


# switch cell version
note = sub.add_parser("note")
# switch_cv_p.add_argument("line" , type=int)
# switch_cv_p.add_argument("index" , type=int)
note.add_argument(
    'com',
    nargs='?',      # makes it optional
    default='l',    # default value
    choices=['l' , 'd' , 's'],
    help="d : delete, l : list, s : search"
)
note.add_argument(
    'params',
    nargs='*',
    type=str,
    help="paramas (required for d and s)"
)







n = notebook(notebook_name='test')

nm = NoteBookManager(notebook.BASE_DIR)


while True:
    try:
        data = input(">> ").strip()
        if not data:
            continue
        if data in ("q", "quit", "exit"):
            break

        # split like shell (handles extra spaces)
        args = parser.parse_args(shlex.split(data))

        if args.command == "add":
            if args.at == 'e':
                n.insert_at_end()
            elif args.at == 's':
                n.insert_at_start()
            elif args.at == 'a':
                if len(args.pos) != 2:
                    print("add a requires 2 integers: add a <line> <index>")
                    continue
                line, index = args.pos
                n.insert_next(line , index)


        elif args.command == "del":
            n.delete_cell(args.line, args.index)

        elif args.command == "exe":
            if len(args.pos) == 2:
                line, index = args.pos
                n.execute_cell(line, index)

            elif len(args.pos) == 0:
                #execute all.
                n.execute_n_cell()
            
            elif len(args.pos) == 1:
                #execute all versions
                n.execute_n_cell_versions(args.pos[0])

            elif len(args.pos) == 3:
                #execute n cells
                line, index , n_cells = args.pos
                if n_cells == -1 : n_cells = None
                n.execute_n_cell(line, index , n_cells)

            
        
        elif args.command == "show" :
            if args.com == 'c':
                os.system('cls')
            n.print_notebook()

        
        elif args.command == "sw":
            n = notebook(notebook_name=args.name)
            if args.com == 'l':
                n.from_json()
            if args.com == 'c':
                os.system('cls')
            
        
        elif args.command == "save" :
            # n.to_json()
            n.save_notebook()
        
        elif args.command == "load" :
            n.from_json()
        
        elif args.command == "c" :
            os.system('cls')
            

        elif args.command == "code":
            # here write code in cmd editor
            ext_code = n.get_cell(args.line , args.index)['code']
            if ext_code == None:
                ext_code = ''
            code = open_notepad(existing_code=ext_code)
            n.update_cell_code(args.line , args.index , code)

        elif args.command == 'v':
            if args.com == 'a':
                if len(args.pos) == 1:
                    line = int(args.pos[0])
                    n.create_cell_version(line)

            if args.com == 'd':
                if len(args.pos) == 2:
                    line, index = args.pos
                    n.delete_cell_version(line, index) 

            if args.com == 's':
                if len(args.pos) == 2:
                    line, index = args.pos
                    n.switch_to_cell_version(line , index)

        elif args.command == "note":
            if args.com == 'l':
                nm.list_notebooks()
            if args.com == 'd':
                if len(args.params) == 1:
                    nm.delete_notebook(args.params[0])
            if args.com == 's':
                if len(args.params) == 1:
                    nm.search_notebook(args.params[0])
                if len(args.params) == 2:
                    case = True if args.params[1] == 't' else False
                    nm.search_notebook(args.params[0] , case)

    except SystemExit:
        # prevents argparse from killing the loop
        print("invalid command")
