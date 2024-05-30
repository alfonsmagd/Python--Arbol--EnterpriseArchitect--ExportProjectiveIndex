import csv
from collections import defaultdict
# Estructura para almacenar los nodos del árbol
class Node:
    def __init__(self, name, type, key):
        self.name = name
        self.type = type
        self.key = key
        
# Lee los datos del CSV
def read_data():
    data = defaultdict(list)
    with open('ej2.csv', 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            node = Node(row['Name'], row['TYPE'], row['KEY'])
            data[row['PARENT_KEY']].append(node)
            print(f"Agregando nodo: {node.name} a la lista de hijos de {row['PARENT_KEY']}")
            
    return data
# Construye el árbol a partir de los datos y escribe la salida en un CSV
def build_tree(data, key='', indice='', writer=None):
    if key in data:
        for i, node in enumerate(data[key], start=1):
            node.indice = f'{indice}{i}' if indice else str(i)
            print(f'{node.name} [{node.type}] {node.indice}')
            writer.writerow([f'{node.name} [{node.type}]', node.indice])
            build_tree(data, node.key, f'{node.indice}.', writer)
# Ejecuta el script
data = read_data()
with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    build_tree(data, writer=writer)