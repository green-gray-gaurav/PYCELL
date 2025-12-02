from flask import Flask, request, jsonify
from notebook_v2 import notebook
app = Flask(__name__)




@app.route('/create_notebook', methods=['POST'])
def create_notebook(): 
    data = request.json
    notebook_name = data.get('notebook_name')
    notebook_instance = notebook(notebook_name=notebook_name)
    response = {
        'message': f'Notebook {notebook_name} created successfully.'
    }
    return jsonify(response)

@app.route('/rename_notebook', methods=['POST'])
def rename_notebook():
    data = request.json
    new_name = data.get('name_new')
    notebook_instance.set_name(new_name)
    response = {
        'message': f'Notebook renamed to {new_name} successfully.'
    }
    return jsonify(response)

@app.route('/load_notebook', methods=['POST'])
def load_notebook():
    data = request.json
    notebook_name = data.get('notebook_name')
    notebook_instance = notebook(notebook_name)
    notebook_instance.load_notebook()
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
    line_index = data.get('line_index')
    index = data.get('index')
    notebook_instance.create_cell(line_index, index)
    response = {
        'message': f'Cell added at line {line_index}, index {index}.'
    }
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

@app.route('/delete_cell', methods=['POST'])
def delete_cell():
    data = request.json
    line_index = data.get('line_index')
    index = data.get('index')
    notebook_instance.delete_cell(line_index, index)
    response = {
        'message': f'Cell at line {line_index}, index {index} deleted successfully.'
    }
    return jsonify(response)



if __name__ == '__main__':
    notebook_instance = notebook(notebook_name="default_notebook")
    app.run(debug=True)