import ast
import argparse


class Renamer(ast.NodeTransformer):

    def visit_Name(self, node: ast.Name):
        # rename everything to 'x'
        node.id = "x"
        ast.NodeVisitor.generic_visit(self, node)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # rename functions to 'function' (actually it's pointless, but let's keep it)
        node.name = "function"
        ast.NodeVisitor.generic_visit(self, node)
        return node
    
    def visit_Expr(self, node: ast.Expr):
        # remove annotations
        if isinstance(node.value, ast.Constant):
            node.value = ast.Constant(value='hello')
        ast.NodeVisitor.generic_visit(self, node)
        return node



def levenshtein_distance(text1, text2):
    # https://en.wikipedia.org/wiki/Levenshtein_distance
    text1 = text1.split('\n')
    text2 = text2.split('\n')
    m = len(text1)
    n = len(text2)
    m += 1
    n += 1
    d = [[0] * n for _ in range(m)]
    for i in range(1, m):
        d[i][0] = i
    for j in range(1, n):
        d[0][j] = j

    for j in range(1, n):
        for i in range(1, m):
            substitutionCost = 0
            if text1[i - 1] != text2[j - 1]:
                substitutionCost = 1

            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1,
                          d[i - 1][j - 1] + substitutionCost)
    return d[m - 1][n - 1]


def compare_trees(tree1, tree2):
    # this operation also removes all comments as we dreamed to
    renamer = Renamer()
    tree1 = renamer.visit(tree1)
    tree2 = renamer.visit(tree2)

    text1 = ast.unparse(tree1)
    text2 = ast.unparse(tree2)
    dist = levenshtein_distance(text1, text2)
    l = max(len(text1.split('\n')), len(text2.split('\n')))
    print("dist:", dist, "l:", l)
    if l != 0:
        return 1 - dist / l
    return 1


parser = argparse.ArgumentParser(description='Antiplagiat system')
parser.add_argument('input', type=str, help='txt file with names of files')
parser.add_argument('scores', type=str,
                    help='name of the file to write scores')
args = parser.parse_args()

scores = []
with open(args.input) as input:
    lines = [line.rstrip() for line in input]
    for line in lines:
        filename1, filename2 = tuple(line.split())
        file1, file2 = '', ''
        print(filename1, filename2)
        with open(filename1, mode='r') as f:
            file1 = f.read()
        with open(filename2, mode='r') as f:
            file2 = f.read()

        scores.append(compare_trees(ast.parse(file1), ast.parse(file2)))

with open(args.scores, mode='w') as scores_file:
    scores_file.write('\n'.join(str(score) for score in scores))
