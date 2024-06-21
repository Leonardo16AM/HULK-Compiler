import dill

def save_object(automaton, file_path):
    with open(file_path, 'wb') as file:
        dill.dump(automaton, file)  # Cambia 'object' por 'automaton'

def load_object(file_path):
    with open(file_path, 'rb') as file:
        loaded_object = dill.load(file)  # Cambia 'object' por 'loaded_object'
    return loaded_object