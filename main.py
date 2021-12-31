import os, re


class Keywords:
    USE='use'
    MOVE='mov'
    ADD='add'
    SUB='sub'
    DIV='div'
    NEG='neg'
    SYSCALL='syscall'

class Errors:
    ValueError="Value Error"
    NameError="Name Error"
    RegisterError="Register Error"


small_chars = 'qwertyuiopasdfghjklzxcvbnm'
registers = [f"{chr}x" for chr in small_chars]
print(registers, len(registers))

def exception(err_name, text, file_name=None, wfile=None):
    print(err_name + ':\n' + text)
    if wfile:
        wfile.close()
    if file_name:
        fp = os.path.join(os.path.abspath(os.path.dirname(__file__)), wfile.name)
        os.remove(fp)
    return

def do_tokens():
    # get file name
    fn = input("file name:")
    # get lines
    lines = open(fn).read().split('\n')

    # exception for incorrect extension
    if fn.split(".")[-1] != "takam": exception(Errors.NameError, "This file is not file with '.takam' extension")

    tokens: list[tuple[str, str, str, int]] = []

    for pos in range(1, len(lines)+1):
        # get token (line, striped)
        token = lines[pos-1].strip().split(" ")

        # kw
        token_0 = token[0]
        # first arg
        try: token_1 = token[1].replace(",", "")
        except IndexError: token_1 = None
        # second or other args
        try: 
            token_2 = None
            if len(token[2:]) <= 1: token_2 = token[2]
            else: token_2 = [tk.replace(",", "") for tk in token[2:]]
        except IndexError: token_2 = None

        # excepted options
        if token_0 in [';', '']: continue

        tokens.append((token_0, token_1, token_2, pos))

    return (tokens, fn)

def compile_it():
    # there is (tokens, file_name)
    res = do_tokens()
    # this is really tokens
    tokens = res[0]
    # get file name
    fn = res[1]

    # file for writing, res[1] is file name
    wfile = open(res[1].replace("takam", "js"), "w+")

    for token in tokens:
        if token[0] == 'START:':
            wfile.write("""
function main() {""")

        elif token[0] == Keywords.USE:
            # all_registers is registers which used in use
            all_registers = []

            all_registers.append(token[1])
            # if count of registers in 3 cell, get all them
            if isinstance(token[2], list):
                [all_registers.append(register) for register in token[2]]
            else:
                all_registers.append(token[2])
            for register in all_registers:
                if register not in registers: exception(Errors.RegisterError, f"Incorrect register at {token[3]}, name: {register}")
                wfile.write(f"""
    let {register} = 0;""")
    
        elif token[0] == Keywords.MOVE:
            # if token[2] is list, cause if it is list in token[2] is two or above vars
            if isinstance(token[2], list): exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
            if token[1] not in registers: exception(Errors.RegisterError, f"Incorrect register at {token[3]}, name: {token[1]}")
            # if token[2] is not register, not string, not number
            if token[2] not in registers and not token[2].startswith('"') and not token[2].isdigit(): exception(Errors.RegisterError, f"Incorrect register at {token[3]}, name: {token[2]}")
            wfile.write(f"""
    {token[1]} = {token[2]};""")

        elif token[0] == Keywords.ADD:
            if isinstance(token[2], list): exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
            wfile.write(f"""
    {token[1]} += {token[2]};""")

        elif token[0] == Keywords.SUB:
            if isinstance(token[2], list): exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)

            wfile.write(f"""
    {token[1]} *= {token[2]};""")

        elif token[0] == Keywords.DIV:
            if isinstance(token[2], list): exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)

            wfile.write(f"""
    {token[1]} /= {token[2]};""")

        elif token[0] == Keywords.SYSCALL:
            if token[1] == "1x00":
                wfile.write(f"""
    console.log({','.join(token[2])})""")
            elif token[1] == '1x01':
                wfile.write(f"""
    """)

    # finish writing
    wfile.write("\n}\nmain()")

def main():
    try:
        compile_it()
    except ValueError:
        pass

if __name__ == '__main__': main()