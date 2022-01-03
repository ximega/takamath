import os, re


class Keywords:
    USE='use'
    MOVE='mov'
    ADD='add'
    SUB='sub'
    DIV='div'
    NEG='neg'
    SYSCALL='syscall'
    SIN='sin'
    COS='cos'
    TG='tg'
    CTG='ctg'
    IML='iml'
    INC='inc'
    SQRT='sqrt'
    LN='ln'
    LG='lg'
    RAD='rad'
    SETPI='stp'
    ARCSIN='arcsin'
    ARCCOS='arccos'
    ARCTG='arctg'
    ARCCTG='arcctg'
    POW='pow'
    FRC='frc'

class Errors:
    ValueError="Value Error"
    NameError="Name Error"
    RegisterError="Register Error"
    CommandError="Command Error"
    SyntaxError="Syntax Error"


small_chars = 'qwertyuiopasdfghjklzxcvbnm'
registers = [f"{chr}x" for chr in small_chars]

reserved_words = ["pi"]

for reg in registers: reserved_words.append(reg)


def exception(err_name, text, file_name=None, wfile=None):
    print(err_name + ':\n' + text + '\n\n\n')
    if wfile:
        wfile.close()
    if file_name:
        fp = os.path.join(os.path.abspath(os.path.dirname(__file__)), wfile.name)
        os.remove(fp)
    return

def is_num(num) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False

def compile_it():
    # get file name
    fn = input("file name:")
    # get lines
    lines = open(fn).read().split('\n')

    # exception for incorrect extension
    if fn.split(".")[-1] != "takam": 
        exception(Errors.NameError, "This file is not file with '.takam' extension")
        return

    tokens: list[tuple[str, str, str, int]] = []

    for pos in range(1, len(lines)+1):
        line = lines[pos-1]

        # threw error if last char is ","
        if len(line) > 0 and not line.strip().startswith(";"):
            if line[-1] in [",", "$", "\\", "^"]:
                exception(Errors.SyntaxError, f"Unexcepted char (',') at {pos}")
                return

        # get token (line, striped)
        token = line.strip().split(" ")

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

    # file for writing, res[1] is file name
    wfile = open(fn.replace("takam", "js"), "w+")

    for token in tokens:
        if not token[1] and token[0] not in ['START:', 'END', '.main']:
            exception(Errors.SyntaxError, f"Null operand at {token[3]}, command: {token[0]}", fn, wfile)
            return

        if token[0] == 'START:':
            wfile.write("""
function main() {
    pi = Math.PI;
    e = Math.E;""")

        elif token[0] in ['.main', 'END']:
            pass

        elif token[0] == Keywords.USE:
            # all_registers is registers which used in use
            all_registers = []

            all_registers.append(token[1])
            # if count of registers in 3 cell, get all them
            if isinstance(token[2], list):
                [all_registers.append(register) for register in token[2]]
            elif token[2]:
                all_registers.append(token[2])

            for register in all_registers:
                if register not in registers: 
                    exception(Errors.RegisterError, f"Incorrect register at {token[3]}, name: {register}")
                    return

                wfile.write(f"""
    let {register} = 0;""")
    
        elif token[0] == Keywords.MOVE:
            # if token[2] is list, cause if it is list in token[2] is two or above vars
            if isinstance(token[2], list): 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return
            if token[1] not in registers: 
                exception(Errors.RegisterError, f"Incorrect register at {token[3]}, name: {token[1]}")
                return
            # if token[2] is not register, not string, not number
            if token[2] not in reserved_words and not token[2].startswith('"') and not is_num(token[2]): 
                exception(Errors.RegisterError, f"Incorrect register at {token[3]}, name: {token[2]}")
                return

            wfile.write(f"""
    {token[1]} = {token[2]};""")

        elif token[0] == Keywords.ADD:
            if isinstance(token[2], list): 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} += {token[2]};""")

        elif token[0] == Keywords.SUB:
            if isinstance(token[2], list): 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} *= {token[2]};""")

        elif token[0] == Keywords.DIV:
            if isinstance(token[2], list): 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} /= {token[2]};""")

        elif token[0] == Keywords.NEG:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = -{token[1]};""")

        elif token[0] == Keywords.SYSCALL:
            if token[1] == "1x00":
                joined_token_2 = token[2]
                if isinstance(token[2], list): 
                    joined_token_2 = ','.join(token[2])
                wfile.write(f"""
    console.log({joined_token_2});""")
            else:
                exception(Errors.ValueError, f"Unkown command for syscall at {token[3]}, name: {token[1]}", fn, wfile)
                return

        elif token[0] == Keywords.SIN:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = Math.sin({token[1]});""")

        elif token[0] == Keywords.COS:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = Math.cos({token[1]});""")

        elif token[0] == Keywords.TG:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = Math.tan({token[1]});""")

        elif token[0] == Keywords.CTG:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = Math.ctg({token[1]});""")

        elif token[0] == Keywords.IML:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} *= {token[1]};""")

        elif token[0] == Keywords.INC:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} += 1;""")

        elif token[0] == Keywords.SQRT:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = Math.sqrt({token[1]});""")

        elif token[0] == Keywords.LN:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = Math.log({token[1]});""")

        elif token[0] == Keywords.LG:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = Math.log({token[1]});""")

        elif token[0] == Keywords.RAD:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = pi/180 * {token[1]};""")

        elif token[0] == Keywords.ARCSIN:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = Math.asin({token[1]});""")

        elif token[0] == Keywords.ARCSIN:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = Math.acos({token[1]});""")

        elif token[0] == Keywords.ARCTG:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = Math.atan({token[1]});""")

        elif token[0] == Keywords.ARCCTG:
            if isinstance(token[2], list) or token[2]: 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = Math.actg({token[1]});""")

        elif token[0] == Keywords.POW:
            if isinstance(token[2], list): 
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = Math.pow({token[1]}, {token[2]});""")

        elif token[0] == Keywords.FRC:
            if isinstance(token[2], list) and len(token[2]) > 2:
                exception(Errors.ValueError, f"Maximum of arguments was reach at {token[3]}, command: {token[0]}", fn, wfile)
                return
            elif not token[2]:
                exception(Errors.SyntaxError, f"After first arguuments should be 2 arguments, was given one at {token[3]}, command: {token[0]}", fn, wfile)
                return
            elif isinstance(token[2], str):
                exception(Errors.ValueError, f"Was given not much arguments in third position", fn, wfile)
                return

            wfile.write(f"""
    {token[1]} = {token[2][0]}/{token[2][1]};""")

        else:
            exception(Errors.CommandError, f"Unkown command at {token[3]}, name: {token[0]}", fn, wfile)
            return

    # finish writing
    wfile.write(r"""
}

Math.ctg = (x) => {
    return 1 / Math.tan(x)
}

Math.actg = (x) => {
    return Math.PI / 2 - Math.atan(x);
}

function exception(err_name, text) {
    console.log(err_name + ':\n' + text + '\n\n\n');
    return;
}

main();""")

def main():
    try:
        compile_it()
    except ValueError:
        pass

if __name__ == '__main__': main()