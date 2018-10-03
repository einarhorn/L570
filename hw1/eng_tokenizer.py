#!/usr/bin/env python3
import re
import sys


# This program takes one input:
#   abbrev_list - a list of abbreviations

# The program will also iterate through stdin, line by line, tokenizing each line

# The output will simply be stdout. The user can pipe this to a file if they choose

# The program will also use a file 'eng-contraction', which is a list of contractions
# The format of each line of this file should be *contraction* (tab) *contraction_token*

def main(abbrev_list, contraction_dict):
    # Iterate through each line
    for unparsed_line in sys.stdin:
        # Remove newline char from line
        unparsed_line = unparsed_line.rstrip()
        #print(unparsed_line)
        # Split the line based on whitespace
        split_line = unparsed_line.split()
        fixed_line = []
        # Go through each item, and split further if necessary
        for token in split_line:
            if token_is_contraction(token, contraction_dict):
                updated_tokens = adjust_contraction_token(token, contraction_dict)
                fixed_line.extend(updated_tokens)

            elif token_is_monetary(token):
                updated_token_as_list = re.split('(\$)', token)
                updated_token_as_list = [item for item in updated_token_as_list if item is not '' and item is not None]
                fixed_line.extend(updated_token_as_list)
            
            elif token_is_number(token) or \
                token_is_email(token) or \
                token_is_url(token) or \
                token_is_path(token):
                strip_chars = [',','"','.','\'',';']
                last_char = token[-1]
                if last_char in strip_chars:
                    fixed_line.append(token[:-1])
                    fixed_line.append(last_char)
                else:
                    fixed_line.append(token)
            
            elif token_is_abbreviation(token, abbrev_list):

                strip_chars = [',','"','\'',';']
                last_char = token[-1]
                if last_char in strip_chars:
                    fixed_line.append(token[:-1])
                    fixed_line.append(last_char)
                else:
                    fixed_line.append(token)
            else:
                updated_token_as_list = re.split(r'(--)|(,)|(")|(\.)|(:)|(/)|(-)|(%)|(\')', token)
                updated_token_as_list = [item for item in updated_token_as_list if item is not '' and item is not None]

                # Adjust ' tokens
                remove_apostraphes = False
                for index, token in enumerate(updated_token_as_list):
                    if token is '\'' and index is not len(updated_token_as_list) - 1:
                        updated_token_as_list[index + 1] = '\'' + updated_token_as_list[index + 1]
                        remove_apostraphes = True
                    elif token is '\'' and index >= 1:
                        updated_token_as_list[index - 1] = updated_token_as_list[index - 1] + '\''
                        remove_apostraphes = True
                    elif token is '\'':
                        remove_apostraphes = False
                if remove_apostraphes:
                    updated_token_as_list = [item for item in updated_token_as_list if item is not '\'']
                fixed_line.extend(updated_token_as_list)
        
        if len(fixed_line) > 0:
            tokenized_sentence = " ".join(fixed_line)
            print(" " + tokenized_sentence.rstrip())
        else:
            print()



def token_is_contraction(token, contraction_dict):
    return token in contraction_dict


def adjust_contraction_token(token, contraction_dict):
    return contraction_dict[token]

def token_is_number(token):
    # Continuous string of numbers
    continous_number_pattern = re.compile(r"^(-?)(\d)+")
    comma_separated_number_pattern = re.compile(r"^(-?)(\d+)((,?)(\d*))*")
    decimal_number_pattern = re.compile(r"^(-?)(\d+).(\d+)")
    comma_decimal_number_pattern = re.compile(r"^(-?)(\d+)((,?)(\d*))*.(\d*)")
    percentage_pattern = re.compile(r"^(-?)(\d+)(.?)(\d*)%")
    fraction_pattern = re.compile(r"^(\d+)/(\d+)")
    return continous_number_pattern.match(token) or \
        comma_separated_number_pattern.match(token) or \
        decimal_number_pattern.match(token) or \
        comma_decimal_number_pattern.match(token) or \
        percentage_pattern.search(token) or \
        fraction_pattern.match(token)

def token_is_email(token):
    email_pattern = re.compile(r"^(\w+)@(\w+).(\w+)")
    return email_pattern.match(token)

def token_is_url(token):
    url_pattern = re.compile(r"^(http)(s?)(://)(\w*)(.)(\w*)")
    return url_pattern.match(token)

def token_is_path(token):
    path_pattern = re.compile(r"^(.*)(:\\)(.*)")
    alt_path_pattern = re.compile(r"^(~/|./|/)(.*)")
    return path_pattern.match(token) or\
        alt_path_pattern.match(token)

def token_is_abbreviation(token, abbrev_list):
    abbrev_pattern = re.compile(r"^(\w\.)+")
    for abbrev in abbrev_list:
        if abbrev in token:
            return True
    return abbrev_pattern.match(token)

def token_is_monetary(token):
    dollar_pattern = re.compile(r"^\$(.*)")
    return dollar_pattern.match(token)



if __name__ == "__main__":
    # Get number of args
    num_args = len(sys.argv)

    # Get list of abbreviations from passed in text file (first argument)
    abbrev_list = []
    if num_args >= 2:
        abbrev_filename = sys.argv[1]
        try:
            abbrev_file = open(abbrev_filename,'r')
            token_list = abbrev_file.read().splitlines()
            for token in token_list:
                if token is not '':
                    abbrev_list.append(token)
        except:
            print("Could not find file")
            import sys
            sys.exit()
    

    # Try to read 'eng_contaction' file into a dictionary
    contraction_filename = 'eng-contraction'
    contraction_dict = {}
    try:
        contraction_file = open(contraction_filename,'r')
        contraction_list = contraction_file.read().splitlines()

        # Iterate through contraction file
        for contraction_pair in contraction_list:
            # Split line based on spaces
            contraction_pair_as_list = contraction_pair.split()

            # If the line was in the expected format, resulting list will have at least three items
            if len(contraction_pair_as_list) >= 3:
                key = contraction_pair_as_list[0]
                value = contraction_pair_as_list[1:]
                contraction_dict[key] = value
    except:
        pass

    main(abbrev_list, contraction_dict)