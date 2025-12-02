def checktype(identifier:str ,globs):
    import keyword , sys
    try:
        if(contains_python_operator(identifier)):
            return 'o'
        if identifier in sys.modules:
            return "m"
        if hasattr(globs.get(identifier), '_call_'):
            return "f"
        if isinstance(globs.get(identifier), type):
            return "c"
        if(keyword.iskeyword(identifier)):
            return "k"
        if globs.get(identifier):
            return "v"
        if identifier.isdigit():
            return "d"
        
    except Exception as e:
        # print("__ec")
        return "n"
    return 'n'

    
    
  



def contains_python_operator(s):
    python_operators = {'+', '-', '', '/', '%', '*', '//', '=', '==', '!=', '<', '>', '<=', '>=', 'and', 'or', 'not', '&', '|', '^', '~', '<<', '>>', 'in', 'not in', 'is', 'is not'}

    
    if s in python_operators:
        return True
    
    return False


def insert_spaces_around_elements(code_string):
    import re
    # Regular expressions to identify various elements
    patterns = {
        'identifiers': r'\b\w+\b',
        'keywords': r'\b(?:if|else|for|while|def|class|and|or|not|in|is|return|import|from|as)\b',
        'constants': r'\b(?:True|False|None)\b',
        'parentheses': r'[()]',
        'brackets': r'[\[\]]',
        'curly_braces': r'[{}]',
        'operators': r'[-+/%=<>&|^!]=?|\{1,2}|/[/]?|//|<<|>>|==|!=|<=|>=',
    }

    # Apply patterns to insert spaces around elements
    for pattern_type, pattern in patterns.items():
        code_string = re.sub(pattern, r'\g<0>', code_string)

    return code_string

def clear_token(code):
    tokens = code.split('~')
    l =list(map(lambda s : s.lstrip(' ~').rstrip(" ~") , tokens))
    l = list(filter(lambda s : s != '' , l  ))
    return l

def get_tokens(code):
    return clear_token(insert_spaces_around_elements(code))



import re

def insert_tildes_around_elements(code_string):
    # Regular expressions to identify various elements
    patterns = {
        'identifiers': r'\b\w+\b',
        'keywords': r'\b(?:if|else|for|while|def|class|and|or|not|in|is|return|import|from|as)\b',
        'constants': r'\b(?:True|False|None)\b',
        'parentheses': r'\(|\)',
        'brackets': r'[\[\]]',
        'curly_braces': r'[{}]',
        'operators': r'[-+/%=<>&|^!]=?|\{1,2}|/[/]?|//|<<|>>|==|!=|<=|>=',
    }

    # Apply patterns to insert ~ around elements
    for pattern_type, pattern in patterns.items():
        if pattern_type == 'parentheses':
            code_string = re.sub(pattern, r'\g<0>', code_string)
        else:
            code_string = re.sub(pattern, r'\g<0>', code_string)

    return code_string