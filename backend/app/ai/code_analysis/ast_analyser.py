from typing import Generator
import os
from tree_sitter import Language, Parser, Tree, Node
import tree_sitter_python
from pprint import pprint  

PY_LANGUAGE = Language(tree_sitter_python.language())
parser = Parser()
parser.language = PY_LANGUAGE

def traverse_tree(tree: Tree) -> Generator[Node, None, None]:
    cursor = tree.walk()
    visited_children = False
    while True:
        if not visited_children:
            yield cursor.node
            if not cursor.goto_first_child():
                visited_children = True
        elif cursor.goto_next_sibling():
            visited_children = False
        elif not cursor.goto_parent():
            break

def analyze_python_code(code: str):
    tree = parser.parse(bytes(code, "utf8"))
    functions = {}

    for node in traverse_tree(tree):
        if node.type == "function_definition":
            name_node = node.child_by_field_name("name")
            params_node = node.child_by_field_name("parameters")
            body_node = node.child_by_field_name("body")
            
            if name_node:
                func_name = name_node.text.decode('utf8')
                functions[func_name] = {
                    'params': [p.text.decode('utf8') for p in params_node.children if p.type == "identifier"],
                    'returns': []  
                }
                
                if body_node:
                    for child in traverse_tree(body_node):
                        if child.type == "return_statement":
                            return_value = child.children[1] if len(child.children) > 1 else None
                            if return_value:
                                # Get the actual return value and its type
                                value_text = return_value.text.decode('utf8')
                                value_type = return_value.type
                                functions[func_name]['returns'].append({
                                    'value': value_text,
                                    'type': value_type
                                })
    
    return functions

def analyze_source_directory(source_dir: str):
    """
    Analyzes all Python files in the specified directory and returns their function information.
    
    Args:
        source_dir (str): Path to the directory containing Python files
        
    Returns:
        dict: Dictionary with filenames as keys and their function analysis as values
    """
    results = {}
    
    for filename in os.listdir(source_dir):
        if filename.endswith('.py'):
            file_path = os.path.join(source_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                analysis = analyze_python_code(code)
                if analysis: 
                    results[filename] = analysis
                    
            except Exception as e:
                print(f"Error analyzing {filename}: {str(e)}")
    
    return results

if __name__ == "__main__":
    source_directory = "source_code"
    
    results = analyze_source_directory(source_directory)
    
    print("\nFunction Analysis Results:")
    print("=" * 50)
    for filename, functions in results.items():
        print(f"\nFile: {filename}")
        print("-" * 30)
        pprint(functions, indent=2, width=60)