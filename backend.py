from collections import defaultdict
from flask import Flask, request, jsonify
from notebook_v2 import notebook
from flask_cors import CORS
app = Flask(__name__)


CORS(app)

@app.route('/create_notebook', methods=['POST'])
def create_notebook(): 
    data = request.json
    notebook_name = data.get('notebook_name')
    # create a new notebook and make it the active module-level instance
    global notebook_instance
    notebook_instance = notebook(notebook_name=notebook_name)
    response = {
        'message': f'Notebook {notebook_name} created successfully.'
    }
    return jsonify(response)

@app.route('/rename_notebook', methods=['POST'])
def rename_notebook():
    data = request.json
    new_name = data.get('name_new')
    # update the active notebook's name
    global notebook_instance
    # notebook_v2 provides set_name
    notebook_instance.set_name(new_name)
    response = {
        'message': f'Notebook renamed to {new_name} successfully.'
    }
    return jsonify(response)

@app.route('/load_notebook', methods=['POST'])
def load_notebook():
    data = request.json
    notebook_name = data.get('notebook_name')
    # load the requested notebook and make it the active instance
    global notebook_instance
    notebook_instance = notebook(notebook_name)
    notebook_instance.load_notebook()
    print('load', notebook_instance.notebook_path)
    response = {
        'message': f'Notebook {notebook_name} loaded successfully.'
    }
    return jsonify(response)

@app.route('/save_notebook', methods=['POST'])
def save_notebook():
    data = request.json
    notebook_instance.save_notebook()
    response = {
        'message': f'Notebook {notebook_instance} saved successfully.'
    }
    return jsonify(response)

@app.route('/run_cell', methods=['POST'])
def run_cell():
    data = request.json
    line_index = data.get('line_index')
    index = data.get('index')
    code, output = notebook_instance.run_cell(line_index, index)
    response = {
        'code': code,
        'output': output
    }
    return jsonify(response)

@app.route('/add_cell', methods=['POST'])
def add_cell():
    data = request.json
    line_index = int(data.get('line_index'))
    index = int(data.get('index'))
    notebook_instance.create_cell(line_index, index)
    response = {
        'message': f'Cell added at line {line_index}, index {index}.'
    }
    for k , v in notebook_instance.cells.items():
        
        for i , j in v.items():
            print("   " , k , i , j)
    return jsonify(response)

@app.route('/update_cell', methods=['POST'])
def update_cell():
    data = request.json
    line_index = data.get('line_index')
    index = data.get('index')
    content = data.get('content')
    notebook_instance.update_cell_content(line_index, index, content)
    response = {
        'message': f'Cell at line {line_index}, index {index} updated successfully.'
    }
    return jsonify(response)

@app.route('/update_cell_connection', methods=['POST'])
def update_cell_connection():   
    data = request.json
    line_index = data.get('line_index')
    index = data.get('index')
    prev_index = data.get('prev_index')
    notebook_instance.update_cell_connection(line_index, index, prev_index)
    response = {
        'message': f'Cell connection at line {line_index}, index {index} updated successfully.'
    }
    return jsonify(response)

@app.route('/delete_cell', methods=['POST'])
def delete_cell():
    data = request.json
    line_index = int(data.get('line_index'))
    index = int(data.get('index'))
    notebook_instance.delete_cell(line_index, index)
    response = {
        'message': f'Cell at line {line_index}, index {index} deleted successfully.'
    }
    return jsonify(response)


@app.route('/get_all_notebook_names', methods=['GET'])
def get_all_notebook_names():
    import os
    if not os.path.exists(notebook.BASE_DIR ):
        os.makedirs(notebook.BASE_DIR)
    notebook_names = os.listdir(notebook.BASE_DIR)
    response = {
        'notebook_names': notebook_names
    }
    return jsonify(response)


@app.route('/get_cell_data', methods=['GET'])
def get_cell_data():
    data = defaultdict(dict)
    global notebook_instance
    print(notebook_instance.notebook_path)
    for line_index, line in notebook_instance.cells.items():
        for index, cell in line.items():
            data[line_index][index] = {
                'content': cell.content,
                'cell_location_prev': cell.cell_location_prev
            }
    response = {
        'cell_data': data
    }
    return jsonify(response) 




if __name__ == '__main__':
    notebook_instance = notebook(notebook_name="default_notebook")
    app.run(debug=True)