import ast

def analyze_file(path):
    with open(path, "r") as f:
        source = f.read()

    tree = ast.parse(source)

    # Print a concise summary of the AST root node and its attributes
    print("analyze_file: AST root type:", type(tree).__name__)
    if hasattr(tree, "_fields"):
        print("analyze_file: _fields =", tree._fields)
        for field in tree._fields:
            value = getattr(tree, field, None)
            if isinstance(value, list):
                print(f"  - {field}: list(len={len(value)})")
            else:
                print(f"  - {field}: {type(value).__name__}")

    # Also print a readable dump of the AST structure
    print("analyze_file: ast.dump(tree, include_attributes=False):")
    print(ast.dump(tree, include_attributes=False, indent=2))

    return tree


if __name__ == "__main__":
    analyze_file("test.py")