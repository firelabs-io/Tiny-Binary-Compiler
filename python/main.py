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

def remove_parentheses(tokens):
    return [token for token in tokens if token not in ('(', ')')]

def codegen(tokens):
    result = ['section .text', 'global _start', '_start:']
    i = 0
    while i < len(tokens):
        if tokens[i].isdigit():
            result.append(f'mov ebx, {tokens[i]}')  
        elif tokens[i] == '+':
            result.append(f'add ebx, {tokens[i + 1]}')  
            i += 1
        elif tokens[i] == '-':
            result.append(f'sub ebx, {tokens[i + 1]}')  
            i += 1
        elif tokens[i] == '*':
            result.append(f'imul ebx, {tokens[i + 1]}')  
            i += 1
        elif tokens[i] == '/':
            
            result.append(f'mov eax, ebx')  
            result.append(f'xor edx, edx')  
            result.append(f'mov ebx, {tokens[i + 1]}')
            result.append(f'idiv ebx')  
            result.append(f'mov ebx, eax')  
            i += 1
        i += 1
    result.append('mov eax, 60')  
    result.append('mov edi, ebx')  
    result.append('syscall')  
    return result

if __name__ == '__main__':
    code = '(20 + 12) * 5'  
    tokens = tokenize(code)
    tokens = remove_parentheses(tokens)
    newcode = codegen(tokens)
    
    with open('out.s', 'w') as file:
        for line in newcode:
            file.write(line + '\n')
    
    subprocess.run(["nasm", "-f", "elf64", "-o", "out.o", "out.s"], check=True)
    subprocess.run(["ld", "-o", "out", "out.o"], check=True)
