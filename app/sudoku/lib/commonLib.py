def import_functions(functions: list):
    def decorator(Class):
        for function in functions:
            setattr(Class, function.__name__, function)
        return Class
    return decorator

def register_function(sequence: list, function):
    sequence.append(function)
    return function