import subprocess
def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        char = expression[i]
        
        if char.isdigit():
            num = char
            while i + 1 < len(expression) and expression[i + 1].isdigit():
                i += 1
                num += expression[i]
            tokens.append(num)
        
        elif char in "+-*/()":
            tokens.append(char)
        
        elif char.isspace():
            pass
        
        i += 1
    
    return tokens


def remove(tokens):
    return [token for token in tokens if token not in ('(', ')')]

def codegen(code):
    result = ['section .text', 'global _start', '_start:']
    i = 0
    while i < len(code):
        if code[i].isdigit():
            result.append(f'mov rbx, {code[i]}')
        if code[i] == '+':
            result.append(f'add rbx, {code[i+1]}')
            i += 1
        if code[i] == '-':
            result.append(f'sub rbx, {code[i+1]}')
            i += 1
        if code[i] == '*':
            result.append(f'imul rbx, {code[i+1]}')
            i += 1
        if code[i] == '/':
            result.append(f'idiv rbx, {code[i+1]}')
            i += 1
        i += 1
    result.append('mov eax, 60')
    result.append('mov rdi, rbx')
    result.append('syscall')
    return result

if __name__ == '__main__':
    code = '(20 + 12) * 5'
    tokens = tokenize(code)
    tokens = remove(tokens)
    newcode = codegen(tokens)
    with open('out.s', 'w') as file:
        for line in newcode:
            file.write(line + '\n')
    
    subprocess.run(["nasm", "-f", "elf64", "-o", "out.o", "out.s"], check=True)
    subprocess.run(["ld", "-o", "out", "out.o"], check=True)
