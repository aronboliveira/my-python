def sort_words_in_file(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()
        sorted_lines = []
        for line in lines:
            words = line.split()  # Split the line into words
            words.sort()          # Sort the words alphabetically
            sorted_line = ' '.join(words)  # Join the sorted words back into a line
            sorted_lines.append(sorted_line)
        with open(output_file, 'w') as outfile:
            outfile.writelines('\n'.join(sorted_lines))
        print(f"Sorted words have been written to {output_file}")
    except FileNotFoundError:
        print(f"The file {input_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
input_file = 'input.txt'
output_file = 'output.txt'
sort_words_in_file(input_file, output_file)