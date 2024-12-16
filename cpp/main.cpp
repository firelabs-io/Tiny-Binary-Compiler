#include <fstream>
#include <string>
#include <vector>
#include <cctype>
#include <iostream>

std::vector<std::string> program = {"section .text", "global _start", "_start:"};
std::vector<std::string> tokenize(const std::string& expression) {
    std::vector<std::string> tokens;
    std::string current;

    for (char ch : expression) {
        if (std::isdigit(ch)) {
            current += ch;
        } else {
            if (!current.empty()) {
                tokens.push_back(current); 
                current.clear();
            }

            if (ch == '+' || ch == '-' || ch == '*' || ch == '/') {
                tokens.emplace_back(1, ch);
            }
        }
    }

    
    if (!current.empty()) {
        tokens.push_back(current);
    }

    return tokens;
}
void codegen(std::vector<std::string> tokens){
    int i = 0;
    while(i < tokens.size()){
        if (tokens[i].find_first_not_of("0123456789") == std::string::npos){
            program.push_back("mov ebx, " + tokens[i]);
            
        }
        if (tokens[i] == "+"){
            program.push_back("add ebx, " + tokens[i+1]);
            i++;
        }
        if (tokens[i] == "-"){
            program.push_back("sub ebx, " + tokens[i+1]);
            i++;
        }
        if (tokens[i] == "*"){
            program.push_back("imul ebx, " + tokens[i+1]);
            i++;
        }
        if (tokens[i] == "/"){
            program.push_back("mov eax, ebx");
            program.push_back("xor edx, edx");
            program.push_back("mov ebx, " + tokens[i+1]);
            program.push_back("idiv ebx");
            program.push_back("mov ebx, eax");
            i++;
        }
        i++;
    } 
}
int main(){
    std::string code = "(20 + 12) * 5";
    std::vector<std::string> tokens = tokenize(code);
    codegen(tokens);
    program.push_back("mov eax, 60");
    program.push_back("mov edi, ebx");
    program.push_back("syscall");
    for (const auto& line : program) {
        std::cout << line << '\n';
    }

    std::ofstream outFile("out.s");
    if(outFile.is_open()){
        for (const auto& line : program) {
            outFile << line << '\n';
        }
        outFile.close();
        // assuming you have nasm and ld installed
        system("nasm -f elf64 -o out.o out.s");
        system("ld -o out out.o");
        return 0;
    }
    return 1; // it din't work for some reason
}
