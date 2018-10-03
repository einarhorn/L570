# Notes about tokenizer
I made a decision to parse '30-day' as three tokens: '30' '-' 'day', rather than keeping it as a single token. This applies to any
word that has a '-' in the middle of it, such as 'mid-November'.

I also use a English contractions file, which exists in this directory as 'eng-contraction'. This file is a list of contractions
and their corresponding tokenized versions. To simplify executing code 
for the grader, this file is referred to within the python source code, instead of taking the filename as a command argument.
If the code does not find the 'eng-contraction' file, it will simply not tokenize contractions.

# Q3 Responses
Number of tokens in ex2: 
Number of tokens in ex2.tok:

Number of lines in ex2.voc:
Number of lines in ex2.tok.voc:
