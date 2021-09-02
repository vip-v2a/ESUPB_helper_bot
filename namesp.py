namespaces = {'global': []}

# key: namespace, value: parent
namespaces_inheritance_map = dict()


class ParentDoesNotExist(Exception):
    pass


class NamespaceDoesNotExist(Exception):
    pass


def add_variable_to_namespace(namespace, variable):
    if namespace not in namespaces.keys():
        raise NamespaceDoesNotExist("You cant get variable from non-existant namespace")
    namespaces[namespace].append(variable)


def get_variable_from_namespace(namespace, variable):
    if namespace not in namespaces.keys():
        raise NamespaceDoesNotExist("You cant get variable from non-existant namespace")
    if namespace == 'global' and variable not in namespaces['global']:
        return None
    if variable in namespaces[namespace]:
        return namespace
    parent = namespaces_inheritance_map[namespace]
    return get_variable_from_namespace(parent, variable)


def create_namespace(namespace, parent):
    if parent not in namespaces.keys():
        raise ParentDoesNotExist("You couldn't inherit namespace from non-existant one")
    namespaces_inheritance_map[namespace] = parent
    namespaces[namespace] = []


if __name__ == '__main__':
    number_of_queries_to_execute = int(input())
    methods_handlers_mapping = {
        'add': add_variable_to_namespace,
        'create': create_namespace,
        'get': get_variable_from_namespace,
    }
    for attempt in range(number_of_queries_to_execute):
        method, namespace, arg = input().split()
        method_handler = methods_handlers_mapping[method]
        output = method_handler(namespace, arg)
        if method == 'get':
            print(output)
