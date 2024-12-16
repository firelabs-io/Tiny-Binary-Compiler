# Tiny-Binary-Compiler
one if not the smallest tiny compiler with generate binary

> [!NOTE]
>  it only works on linux x86_64, if you want edit to binary work on linux and maybe arm feel free do so

its very simple, in fact very simple, it tokenize, translate to assembly and generate binary

# how run
1. make sure nasm is installed (ld should be installed as is part of linux)
2. run python python/main.py or g++ cpp/main.cpp -o cpp/main then execute main
3. run out binary (in python/ or cpp/)
4. enjoy

>[!NOTE]
> if you want edit to like 53 - (28 * 2):

you need edit the source code ("code = '(20 + 12) * 5'") in python.

or ("std::string code = "(20 + 12) * 5";") in c++
