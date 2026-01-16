import AST_module as am
# import openAI_mode as oai

if __name__ == "__main__":

    file_path = "test_code.py"

    # Create an instance of the CodeAnalyzer class
    analyzer = am.CodeAnalyzer()

    tree = analyzer.create_tree(file_path)
    analyzer.visit(tree)

    for iss in analyzer.issues:
        print(iss)