import re
import os
import inspect
import ast
import types
from sympy import symbols, Matrix, solve, Eq, lambdify, latex


def save_function(func, func_name=None, filename=None, docstring=None):
    """
    Save the function to a python file.
    
    Parameters:
    -----------
    func : function
        The function to be saved.
    func_name : str
        The desired name of the function. If not provided, the original function name is used.
    filename : str
        The desired filename. If not provided, the function name is used.
    docstring : str
        The desired docstring for the function.
    """
    # Use the function name as the filename if no filename is given
    if filename is None:
        filename = func.__name__

    # Use the function name as the function name if no function name is given
    if func_name is None:
        func_name = func.__name__
    
    # Check if file exists and function name is already used
    if os.path.isfile(filename + '.py'):
        with open(filename + '.py', 'r') as f:
            file_content = f.read()
            parsed_content = ast.parse(file_content)
            function_names = [f.name for f in parsed_content.body if isinstance(f, ast.FunctionDef)]
            if func_name in function_names:
                print(f"Function {func_name} already exists in the file. The function was not saved.")
                return

    # Get the source code of the function
    source_code = inspect.getsource(func)

    # Replace the original function name with the provided function name
    source_code = source_code.replace(func.__name__, func_name, 1)

    # If a docstring is provided, replace dummy variable names with provided names
    if docstring:
        param_names = re.findall(r'\*\*(.+?):', docstring)  # Find all variable names in docstring
        for i, param in enumerate(param_names):
            source_code = source_code.replace(f'dummy_{i}', param)  # Replace dummy variable names in function definition

        # Find the first newline (which is right after the function definition)
        idx = source_code.find('\n')

        # Add the docstring right after the function definition
        source_code = source_code[:idx] + f'\n    """{docstring}"""\n' + source_code[idx:]

    # Save the function to the file
    with open(filename + '.py', 'a') as f:
        f.write(source_code + "\n")


def create_function(expr):
    # Get the names of the parameters from the expression
    param_names = list(expr.free_symbols)
    param_names = [str(p) for p in param_names]
    
    # Clean the names for python
    param_names_clean = []
    for p in param_names:
        p = re.sub('[{}]', '', p)
        p = re.sub('\^', '__', p)
        p = p.replace('\x00', '')
        p = p.replace('-', '_minus_')
        p = p.replace(',', '')
        param_names_clean.append(p)
    
    # Replace the parameters in the expression with the cleaned names
    expr_clean = expr
    for p_old, p_new in zip(param_names, param_names_clean):
        expr_clean = expr_clean.subs(p_old, p_new)

    # Create the function with the cleaned expression and parameters
    f = lambdify([symbols(p) for p in param_names_clean], expr_clean, "numpy")

    # Create a detailed docstring
    docstring = f"Function corresponding to the equation {expr}.\n"
    docstring += "\nArguments:\n"
    for var in param_names_clean:
        docstring += f"- {var}: Value for the variable '{var}' in the equation.\n"
    f.__doc__ = docstring

    return f
def minimal_p_rc(g__11_ff, c, M__E1, g_rc, p__11_ff):
    """Function corresponding to the equation (-M^{E,1}*c*g^{11}_{ff}*p^{11}_{ff} + 1)/(M^{E,1}**2*c**2*g^{11}_{ff}*g_rc*p^{11}_{ff}).

Arguments:
- g__11_ff: Value for the variable 'g__11_ff' in the equation.
- c: Value for the variable 'c' in the equation.
- M__E1: Value for the variable 'M__E1' in the equation.
- g_rc: Value for the variable 'g_rc' in the equation.
- p__11_ff: Value for the variable 'p__11_ff' in the equation.
"""

    return ((-M__E1*c*g__11_ff*p__11_ff + 1)/(M__E1**2*c**2*g__11_ff*g_rc*p__11_ff))

def minimal_p_11ff_2seqs(g__11_ff, c, M__E1, r__E0_i_minus_1, p_rc, g__01_ffi, p_ffi, M__E0, g_rc):
    """Function corresponding to the equation (M^{E,0}*M^{E,1}*c**2*g^{01}_{ffi}*g_rc*p_ffi*p_rc*r^{E,0}_{i-1} + 1)/(M^{E,1}*c*g^{11}_{ff}*(M^{E,1}*c*g_rc*p_rc + 1)).

Arguments:
- g__11_ff: Value for the variable 'g__11_ff' in the equation.
- c: Value for the variable 'c' in the equation.
- M__E1: Value for the variable 'M__E1' in the equation.
- r__E0_i_minus_1: Value for the variable 'r__E0_i_minus_1' in the equation.
- p_rc: Value for the variable 'p_rc' in the equation.
- g__01_ffi: Value for the variable 'g__01_ffi' in the equation.
- p_ffi: Value for the variable 'p_ffi' in the equation.
- M__E0: Value for the variable 'M__E0' in the equation.
- g_rc: Value for the variable 'g_rc' in the equation.
"""

    return ((M__E0*M__E1*c**2*g__01_ffi*g_rc*p_ffi*p_rc*r__E0_i_minus_1 + 1)/(M__E1*c*g__11_ff*(M__E1*c*g_rc*p_rc + 1)))

