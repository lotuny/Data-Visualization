# input_file_path = "boundary.json"
# output_file_path = "boundary-new-lines.csv"
# input_f = open(input_file_path, "r", encoding='utf-8')
# output_f = open(output_file_path, "w", encoding='utf-8')
#
# chars = input_f.read()
# flag = 0
# for char in chars:
#     output_f.write(char)
#     if char == ',' and flag == 1:
#         output_f.write('\n')
#         flag = 0
#     elif char == '}':
#         flag = 1
#     elif flag == 1:
#         flag = 0
#
# input_f.close()
# output_f.close()

input_file_path = "boundary-new-lines.csv"
output_file_path = "boundary-request.txt"
input_f = open(input_file_path, "r", encoding='utf-8')
output_f = open(output_file_path, "w", encoding='utf-8')

output_f.write('https://data.police.uk/api/crimes-street/all-crime?poly=')
date = '2019-02'
lines = input_f.readlines()
i = 0
for line in lines:
    i += 1
    if i == 1:
        continue
    else:
        new_line = ''
        new_char = ''
        for char in line:
            new_char = char
            if char == '\n':
                if i == len(lines):
                    new_char = ''
                else:
                    new_char = ':'
            new_line += new_char
        output_f.write(new_line)
output_f.write('&date='+date)

input_f.close()
output_f.close()
