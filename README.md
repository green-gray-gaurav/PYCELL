# Simple Book - Console-Based Multi-Version Cell Notebook

A powerful console-based notebook system for Python that supports cell versioning, persistent execution environments, and flexible cell management.

## Features

- **Multi-version cells**: Create and switch between different versions of cells
- **Persistent execution environments**: Each cell maintains its own execution environment with variables and state
- **Cell chaining**: Cells can reference previous cells' outputs and variables
- **Notebook management**: Create, list, search, and delete notebooks
- **Interactive code editing**: Edit cell code using your default text editor (Notepad on Windows)
- **Output capture**: Use the `output()` function to capture and display cell outputs

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd simple-book
```

2. Ensure you have Python 3.x installed

3. Install dependencies (if any):
```bash
pip install -r requirements.txt
```

## Usage

Run the main script to start the interactive notebook console:

```bash
python main.py
```

You'll see a prompt `>>` where you can enter commands.

### Commands

#### Cell Management

**Add a cell**
- `add` or `add e` - Add a cell at the end
- `add s` - Add a cell at the start
- `add a <line> <index>` - Add a cell after the specified cell

**Delete a cell**
- `del <line> <index>` - Delete the cell at the specified position

**Edit cell code**
- `code <line> <index>` - Open the cell's code in your default editor (Notepad on Windows)

**Show notebook**
- `show` or `show c` - Display the notebook structure (clears screen first if 'c' is used)

#### Execution

**Execute cells**
- `exe <line> <index>` - Execute a specific cell
- `exe` - Execute all cells
- `exe <line>` - Execute all versions of a specific line
- `exe <line> <index> <n>` - Execute n cells starting from the specified cell (use -1 for all remaining)

#### Cell Versioning

**Create cell version**
- `cv <line>` - Create a new version of a cell at the specified line

**Manage versions**
- `v a <line>` - Add a new version to a cell
- `v d <line> <index>` - Delete a specific cell version
- `v s <line> <index>` - Switch to a specific cell version

#### Notebook Management

**Switch notebook**
- `sw <name>` - Switch to a notebook (creates new if doesn't exist)
- `sw l <name>` - Switch to a notebook and load it from disk
- `sw c <name>` - Switch to a notebook and clear screen

**Save and load**
- `save` - Save the current notebook to disk
- `load` - Load the current notebook from disk

**Notebook operations**
- `note l` - List all notebooks
- `note d <name>` - Delete a notebook
- `note s <pattern>` - Search notebooks by pattern (case-insensitive by default)
- `note s <pattern> t` - Search notebooks by pattern (case-sensitive)

#### Utility

- `c` - Clear the screen
- `q`, `quit`, or `exit` - Exit the program

## Examples

### Basic Workflow

```bash
>> add                    # Add a cell at the end
>> code 0 0              # Edit the first cell
>> exe 0 0               # Execute the first cell
>> add                   # Add another cell
>> code 1 0              # Edit the second cell
>> exe 1 0               # Execute the second cell
>> show                  # Display the notebook
>> save                  # Save the notebook
```

### Using Cell Versions

```bash
>> add                   # Create first cell
>> code 0 0              # Write some code
>> cv 0                  # Create a version of cell 0
>> code 0 1              # Edit the new version
>> v s 0 1               # Switch to version 1
>> exe 0 1               # Execute version 1
```

### Working with Multiple Notebooks

```bash
>> note l                # List all notebooks
>> sw mynotebook         # Switch to/create 'mynotebook'
>> sw l mynotebook       # Switch and load 'mynotebook'
>> note s test           # Search for notebooks matching 'test'
```

### Using the output() Function

In your cell code, use `output()` to capture results:

```python
# Cell 0
x = 10
y = 20
output("The sum is:", x + y)

# Cell 1 (can access x and y from previous cell)
z = x * y
output("The product is:", z)
```

## Project Structure

```
simple-book/
├── main.py              # Main CLI interface
├── notebook_v2.py       # Core notebook implementation
├── notebook.py          # Original notebook implementation
├── NM.py                # Notebook manager for managing multiple notebooks
├── coolprint.py         # Utility for formatted printing
└── NOTEBOOKS/           # Directory where notebooks are stored
    └── <notebook-name>/
        ├── note_loader.json    # Notebook metadata
        └── cell_<line>_<index>.pkl  # Cell execution environments
```

## How It Works

1. **Cells**: Each cell has a line number and index (for versions). Cells can be chained together where each cell can access variables from previous cells.

2. **Execution Environments**: Each cell's execution environment is pickled and stored. When executing a cell, it loads the environment from the previous cell (if any) and adds its own variables.

3. **Versioning**: Multiple versions of a cell can exist at the same line number but with different indices. You can switch between versions and execute different ones.

4. **Persistence**: Notebooks are saved as JSON files containing cell metadata, while execution environments are stored as pickle files.

## Notes

- The `output()` function is available in each cell's execution environment to capture output
- Cell execution environments persist between sessions
- Variables from previous cells are accessible in subsequent cells
- The system uses pickle for serialization, so be cautious when loading untrusted notebooks

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

