#FROM http://code.activestate.com/recipes/578178-colorize-python-sourcecode-syntax-highlighting/
import keyword, tokenize, functools

def is_builtin(s):
    'Return True if s is the name of a builtin'
    return hasattr(builtins, s)

def combine_range(lines, start, end):
    'Join content from a range of lines between start and end'
    (srow, scol), (erow, ecol) = start, end
    if srow == erow:
        return lines[srow-1][scol:ecol], end
    rows = [lines[srow-1][scol:]] + lines[srow: erow-1] + [lines[erow-1][:ecol]]
    return ''.join(rows), end

def analyze_python(source):
    '''Generate and classify chunks of Python for syntax highlighting.
       Yields tuples in the form: (category, categorized_text).
    '''
    lines = source.splitlines(True)
    lines.append('')
    readline = functools.partial(next, iter(lines), '')
    kind = tok_str = ''
    tok_type = tokenize.COMMENT
    written = (1, 0)
    for tok in tokenize.generate_tokens(readline):
        prev_tok_type, prev_tok_str = tok_type, tok_str
        tok_type, tok_str, (srow, scol), (erow, ecol), logical_lineno = tok
        kind = ''
        if tok_type == tokenize.COMMENT:
            kind = 'comment'
        elif tok_type == tokenize.OP and tok_str[:1] not in '{}[](),.:;@':
            kind = 'operator'
        elif tok_type == tokenize.STRING:
            kind = 'string'
            if prev_tok_type == tokenize.INDENT or scol==0:
                kind = 'docstring'
        elif tok_type == tokenize.NAME:
            if tok_str in ('def', 'class', 'import', 'from'):
                kind = 'definition'
            elif prev_tok_str in ('def', 'class'):
                kind = 'defname'
            elif keyword.iskeyword(tok_str):
                kind = 'keyword'
            elif is_builtin(tok_str) and prev_tok_str != '.':
                kind = 'builtin'
        if kind:
            if written != (srow, scol):
                text, written = combine_range(lines, written, (srow, scol))
                yield '', text
            text, written = tok_str, (erow, ecol)
            yield kind, text
    line_upto_token, written = combine_range(lines, written, (erow, ecol))
    yield '', line_upto_token

default_ansi = {
    'comment': ('\033[0;31m', '\033[0m'),
    'string': ('\033[0;32m', '\033[0m'),
    'docstring': ('\033[0;32m', '\033[0m'),
    'keyword': ('\033[0;33m', '\033[0m'),
    'builtin': ('\033[0;35m', '\033[0m'),
    'definition': ('\033[0;33m', '\033[0m'),
    'defname': ('\033[0;34m', '\033[0m'),
    'operator': ('\033[0;33m', '\033[0m'),
}

def ansi_highlight(classified_text, colors=default_ansi):
    'Add syntax highlighting to source code using ANSI escape sequences'
    # http://en.wikipedia.org/wiki/ANSI_escape_code
    result = []
    for kind, text in classified_text:
        opener, closer = colors.get(kind, ('', ''))
        result += [opener, text, closer]
    return ''.join(result)

def highlight(text):
    classified_text = analyze_python(text)
    return ansi_highlight(classified_text)

