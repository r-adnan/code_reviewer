import ast

class CodeAnalyzer(ast.NodeVisitor):
    # Analyze the ASTs and collect style/complexity issues

    # The analyzer is modular - each check is implemented in its own method so
    # the checks are easy to unit-test and reuse

    def __init__(self, *, max_function_length=50, max_args=5, max_nested_blocks=4, min_var_name_len=2):
        self.issues = []
        self.tree = None
        self.max_function_length = max_function_length
        self.max_args = max_args
        self.max_nested_blocks = max_nested_blocks
        self.min_var_name_len = min_var_name_len
        # short names that are commonly acceptable
        self.acceptable_short_names = {"i", "j", "k", "x", "y", "z", "_"}

    # Create an AST from a file and store it on the instance
    def create_tree(self, file_path):
        with open(file_path, "r") as f:
            source = f.read()
        self.tree = ast.parse(source)
        return self.tree

    # --- Visitors -----------------------------------------------------------------
    # Run all function-related checks and continue traversal
    def visit_FunctionDef(self, node):
        self.check_function_length(node)
        self.check_too_many_args(node)
        self.check_nested_blocks(node)
        self.generic_visit(node)

    def visit_Assign(self, node):
        self.check_variable_names(node)
        self.check_unused_variables(node)
        self.generic_visit(node)
    
    # def visit_Performance(self, node):
    #     self.repeated_calculations(node)
    #     self.inefficient_loops(node)
    #     self.string_concatenation(node)
    #     self.generic_visit(node)

    def visit_ImportFrom(self, node):
        # flag wildcard imports (from module import *)
        for alias in node.names:
            if alias.name == "*":
                self.issues.append(f"Wildcard import from '{node.module}' is discouraged")
        self.generic_visit(node)

    # --- Checks -------------------------------------------------------------------
    def check_function_length(self, node: ast.FunctionDef):
        length = len(node.body)
        if length > self.max_function_length:
            self.issues.append(
                f"Function '{node.name}' is too long ({length} statements, limit: {self.max_function_length})"
            )

    def check_too_many_args(self, node: ast.FunctionDef):
        # count positional, keyword-only, vararg and kwarg
        argc = len(node.args.args) + len(node.args.kwonlyargs)
        if node.args.vararg:
            argc += 1
        if node.args.kwarg:
            argc += 1
        if argc > self.max_args:
            self.issues.append(
                f"Function '{node.name}' has too many arguments ({argc}, limit: {self.max_args})"
            )

    # Compute max nesting depth of control flow statements within the function
    def check_nested_blocks(self, node: ast.FunctionDef):
        def depth_of_nodes(nodes, depth=0):
            maxd = depth
            for n in nodes:
                # consider constructs that increase nesting
                if isinstance(n, (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.AsyncFor, ast.AsyncWith)):
                    d = depth_of_nodes(getattr(n, 'body', []), depth + 1)
                    # also consider orelse and handlers
                    d = max(d, depth_of_nodes(getattr(n, 'orelse', []), depth + 1))
                    if isinstance(n, ast.Try):
                        for handler in getattr(n, 'handlers', []):
                            d = max(d, depth_of_nodes(getattr(handler, 'body', []), depth + 1))
                    maxd = max(maxd, d)
                elif hasattr(n, 'body') and isinstance(getattr(n, 'body'), list):
                    maxd = max(maxd, depth_of_nodes(getattr(n, 'body'), depth))
            return maxd

        max_depth = depth_of_nodes(node.body, 0)
        if max_depth > self.max_nested_blocks:
            self.issues.append(
                f"Function '{node.name}' has deep nesting (depth {max_depth}, limit: {self.max_nested_blocks})"
            )

    def check_variable_names(self, node: ast.Assign):
        for target in node.targets:
            # simple case: single name assignment
            if isinstance(target, ast.Name):
                name = target.id
                if len(name) < self.min_var_name_len and name not in self.acceptable_short_names:
                    self.issues.append(f"Short variable name '{name}' at line {node.lineno}")
            # tuple assignments: check components
            elif isinstance(target, (ast.Tuple, ast.List)):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        name = elt.id
                        if len(name) < self.min_var_name_len and name not in self.acceptable_short_names:
                            self.issues.append(f"Short variable name '{name}' at line {node.lineno}")

    def check_unused_variables(self, node: ast.Assign):
        # Simple analysis: collect names assigned in the targets and names used in the value (RHS).
        # This flags assignments where the assigned names do not appear in the RHS expression.
        assigned_vars = set()
        used_vars = set()

        # collect assigned names (handle Name, Tuple, List)
        def collect_targets(t):
            if isinstance(t, ast.Name):
                assigned_vars.add(t.id)
            elif isinstance(t, (ast.Tuple, ast.List)):
                for elt in t.elts:
                    collect_targets(elt)
            # other target types (Attribute, Subscript) are ignored for now

        for target in node.targets:
            collect_targets(target)

        # collect names used in the RHS expression
        for n in ast.walk(node.value):
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                used_vars.add(n.id)

        # ignore common "throwaway" names like '_'
        unused = {name for name in assigned_vars if name not in used_vars and name not in self.acceptable_short_names}

        if unused:
            self.issues.append(f"Unused variable(s) {', '.join(sorted(unused))} at line {node.lineno}")


    # Utility
    def get_issues(self):
        return list(self.issues)

    def clear_issues(self):
        self.issues.clear()

    # Print a concise summary of the AST root node and its attributes
    def print_ast(self, tree):
        print("analyze_file: AST root type:", type(tree).__name__)
        if hasattr(tree, "_fields"):
            print("analyze_file: _fields =", tree._fields)
            for field in tree._fields:
                value = getattr(tree, field, None)
                if isinstance(value, list):
                    print(f"  - {field}: list(len={len(value)})")
                else:
                    print(f"  - {field}: {type(value).__name__}")

        # Print a readable dump of the AST structure
        print("analyze_file: ast.dump(tree, include_attributes=False):")
        print(ast.dump(tree, include_attributes=False, indent=2))


