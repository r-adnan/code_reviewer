def decrypt_caesar(s):
    for i in range(1, 27):
        sout = ""
        for char in s:
            if char == " ":
                sout += char
                continue
            sout += chr(((ord(char) - 64 - i) % 26) + 64)
        print("key: ", i, sout)

    return

# Intentionally problematic examples for CodeAnalyzer
from math import *  # wildcard import should be flagged by the analyzer

def unused_variable():
    i = 3
    j = 6
    k = 5
    return j + k

def too_many_args(a, b, c, d, e, f, g):
    """Function with too many arguments (should be flagged)."""
    return a + b + c + d + e + f + g


def deep_nesting():
    """Function with deep nesting (should be flagged)."""
    if True:
        if True:
            if True:
                if True:
                    if True:
                        print("deep")
    return


def short_names():
    # 'q' is shorter than min_var_name_len=2 and not in acceptable_short_names
    q = 1
    (a, b) = (2, 3)  # 'a' and 'b' are also short and should be flagged
    return q + a + b

# Keep the existing long function to demonstrate length detection (rep)

def rep():
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")

    return