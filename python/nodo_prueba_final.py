import csv
from collections import defaultdict

class Node:
    def __init__(self, name, key, type):
        self.name = name
        self.key = key
        self.type = type
        self.children = []
    def add_child(self, child_node):
        self.children.append(child_node)
    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.name) + " [" + self.type + "]" + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret
def build_tree_from_csv(file_path):
    nodes = {}
    root = None
    # Leer el archivo CSV
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile ,  delimiter=';')
        for row in reader:
            name = row['Name']
            key = row['KEY']
            type = row['TYPE']
            parent_key = row['PARENT_KEY']
            node = Node(name, key, type)
            nodes[key] = node
            if parent_key == '':
                root = node
            else:
                if parent_key in nodes:
                    nodes[parent_key].add_child(node)
                else:
                    # Si el padre no existe aún, inicializamos una lista para sus hijos
                    nodes[parent_key] = Node(None, parent_key, None)
                    nodes[parent_key].add_child(node)
    # Asegurar que todos los nodos huérfanos son asignados a sus padres correspondientes
    for key, node in nodes.items():
        if node.name is None:  # Nodo huérfano encontrado
            for child in node.children:
                if child.key in nodes:
                    nodes[child.key] = child
    return root

def generate_paths_from_root_to_leaves(node, path=None, index=''):
    if path is None:
        path = []
        index = '1'
    path.append(f"{node.name} [{node.type}] {index}")
    if not node.children:  # Es una hoja
        yield path.copy()
    else:
        for i, child in enumerate(node.children, start=1):
            child_index = f"{index}.{i}"
            yield from generate_paths_from_root_to_leaves(child, path, child_index)
    path.pop()  # Retroceder


def write_paths_to_csv(paths, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Path'])  # Encabezado del CSV
        written = set()  # Conjunto de elementos ya escritos
        for path in paths:
            for element in path:
                if element not in written:
                    writer.writerow([element])
                    written.add(element)

# Ejemplo de uso
if __name__ == "__main__":
    # Construir el árbol desde el archivo CSV
    root = build_tree_from_csv('ej2.csv')
    
    # Mostrar el árbol
    print(root)
    
    # Generar las cadenas desde la raíz hasta cada nodo hoja
    paths = list(generate_paths_from_root_to_leaves(root))
    
    # Escribir las cadenas en un nuevo archivo CSV
    write_paths_to_csv(paths, 'out.csv')
    
    print("Paths from root to leaves have been written to 'output_paths.csv'")
