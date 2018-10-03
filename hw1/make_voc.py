#!/usr/bin/env python3
import sys

def main():
    # Create a dictionary of (token -> frequency)
    token_frequency_dict = {}

    # Iterate through each line in stdin
    for unparsed_line in sys.stdin:
        # Remove newline char from line
        unparsed_line = unparsed_line.rstrip()

        # Split the line based on whitespace
        split_line = unparsed_line.split()

        # Iterate over tokens in sentence
        for token in split_line:
            # Store token occurance in dict
            if token in token_frequency_dict:
                token_frequency_dict[token] += 1
            else:
                token_frequency_dict[token] = 1

    token_dict_sorted_keys = sorted(token_frequency_dict, key=token_frequency_dict.get, reverse=True)
    for key in token_dict_sorted_keys:
        print(key + "\t" + str(token_frequency_dict[key]))





if __name__ == "__main__":
    main()