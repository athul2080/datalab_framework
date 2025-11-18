import nbformat
from nbconvert import PythonExporter
from nbconvert.preprocessors import ExecutePreprocessor
import os

def run_notebook(notebook_path):
    """
    Load and run the Jupyter notebook.
    """
    with open(notebook_path, 'r') as f:
        notebook_content = nbformat.read(f, as_version=4)

    # Use the ExecutePreprocessor to execute the notebook code
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(notebook_content, {'metadata': {'path': os.path.dirname(notebook_path)}})

    # After executing, convert the notebook to a Python script
    python_exporter = PythonExporter()
    body, resources = python_exporter.from_notebook_node(notebook_content)
    
    return body  # Returning Python script as string
