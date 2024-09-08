import sys


def main(args):
    condition = ''.join(args)

    # condition = "((A == True) or ((B != b) or (G == False))) and (((C) or ((E != e) and (F == f))) or (D == d))"

    root = []

    level = 0
    inner = ''
    branch = root

    parents_dict = {}

    for ch in condition:
        if ch == '(':
            new_branch = []
            if inner != '':
                for word in inner.strip().split():
                    branch.append(word)
            inner = ''
            branch.append(new_branch)
            parents_dict[level] = branch
            branch = new_branch
            level += 1
        elif ch == ')':
            if inner != '':
                for word in inner.strip().split():
                    branch.append(word)
            inner = ''
            branch = parents_dict[level-1]
            level -= 1
        else:
            inner += ch
    if level != 0:
        raise SyntaxError(condition)
    print(root)
    root = reorder(root)
    print(root)
    root = flatten(root)
    print(root)


def replace_operator(operator):
    if operator == 'or':
        return '|'
    if operator == 'and':
        return '&amp;'
    raise SyntaxError(operator)


def replace_boolean(variable):
    if variable.lower() == 'true':
        return True
    if variable.lower() == 'false':
        return False
    return variable


def reorder(root):
    if len(root) == 1:
        root = [root[0], '==', 'True']
    if root[1] in {'or', 'and'}:
        root = [replace_operator(root[1]), reorder(root[0]), reorder(root[2])]
    else:
        root = (root[0], root[1], replace_boolean(root[2]))
    return root


def flatten(root):
    if not isinstance(root, list) or root == []:
        return root
    if isinstance(root[0], list):
        return flatten(root[0]) + flatten(root[1:])
    return root[:1] + flatten(root[1:])


if __name__ == "__main__":
    main(sys.argv[1:])
