import os
import sys
import ast
# ensure project root is on sys.path so tests can import local modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AST_module import CodeAnalyzer


def run_test(source, analyzer):
    tree = ast.parse(source)
    analyzer.visit(tree)
    return analyzer.get_issues()


def test_function_length():
    src = """
def long_func():
    a = 1
    b = 2
    c = 3
"""
    analyzer = CodeAnalyzer(max_function_length=2)
    issues = run_test(src, analyzer)
    assert any("too long" in msg for msg in issues)


def test_too_many_args():
    src = "def f(a,b,c,d,e,f):\n    pass\n"
    analyzer = CodeAnalyzer(max_args=5)
    issues = run_test(src, analyzer)
    assert any("too many arguments" in msg for msg in issues)


def test_nested_blocks():
    src = """
def nested():
    if True:
        if True:
            if True:
                pass
"""
    analyzer = CodeAnalyzer(max_nested_blocks=2)
    issues = run_test(src, analyzer)
    assert any("deep nesting" in msg for msg in issues)


def test_short_variable_name():
    src = "q = 1\n"
    analyzer = CodeAnalyzer(min_var_name_len=2)
    issues = run_test(src, analyzer)
    assert any("Short variable name" in msg for msg in issues)


def test_wildcard_import():
    src = "from math import *\n"
    analyzer = CodeAnalyzer()
    issues = run_test(src, analyzer)
    assert any("Wildcard import" in msg for msg in issues)


def test_unused_variable_simple():
    analyzer = CodeAnalyzer()
    issues = run_test("a = 1\n", analyzer)
    assert any("Unused variable" in msg for msg in issues)


def test_assigned_not_in_rhs():
    analyzer = CodeAnalyzer()
    issues = run_test("a = b\n", analyzer)
    assert any("Unused variable" in msg for msg in issues)


def test_unused_variable_used_in_rhs():
    analyzer = CodeAnalyzer()
    issues = run_test("a = a + 1\n", analyzer)
    assert not any("Unused variable" in msg for msg in issues)


def test_underscore_ignored():
    analyzer = CodeAnalyzer()
    issues = run_test("_ = 1\n", analyzer)
    assert not any("Unused variable" in msg for msg in issues)


if __name__ == '__main__':
    test_function_length()
    test_too_many_args()
    test_nested_blocks()
    test_short_variable_name()
    test_wildcard_import()
    test_unused_variable_simple()
    test_assigned_not_in_rhs()
    test_unused_variable_used_in_rhs()
    test_underscore_ignored()
    print('All analyzer tests passed')
