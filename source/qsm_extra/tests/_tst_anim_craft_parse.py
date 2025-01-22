# coding:utf-8
import re

# The given data string
data = """
CSF0f<0,1>(matrix3 [-0.8921042680740356,-0.02059752680361271,0.4513603150844574] [-0.04932306334376335,0.9974299073219299,-0.05196893587708473] [-0.4491298794746399,-0.06862417608499527,-0.8908274173736572] [-0.034841522574424744,23.60810089111328,0.007131293416023254])<0,2>(matrix3 [-0.04181754216551781,0.9971072673797607,0.06347089260816574] [0.35092809796333313,-0.044820912182331085,0.9353294372558594] [0.9354686141014099,0.06138698384165764,-0.34803855419158936])
CSF1f<0,1>(matrix3 [-0.8921042680740356,-0.02059752680361271,0.4513603150844574] [-0.04932306334376335,0.9974299073219299,-0.05196893587708473] [-0.4491298794746399,-0.06862417608499527,-0.8908274173736572] [-0.034841522574424744,23.60810089111328,0.007131293416023254])<0,2>(matrix3 [-0.04181754216551781,0.9971072673797607,0.06347089260816574] [0.35092809796333313,-0.044820912182331085,0.9353294372558594] [0.9354686141014099,0.06138698384165764,-0.34803855419158936])
"""

# Split the data into lines
lines = data.strip().split("\n")

# Regular expression to capture the necessary data
pattern = re.compile(r'CSF(\d)f<(\d),(\d)>\(matrix3 (.*?)\)\s*<(\d),(\d)>\(matrix3 (.*?)\)')

# Dictionary to store the parsed data
result = {}

# Process each line individually
for line in lines:
    matches = pattern.findall(line)

    for match in matches:
        group1 = int(match[1])
        group2 = int(match[2])
        matrix1 = match[3].strip().split('] [')
        matrix2 = match[6].strip().split('] [')

        matrix1 = [list(map(float, m[1:-1].split(','))) for m in matrix1]
        matrix2 = [list(map(float, m[1:-1].split(','))) for m in matrix2]

        # If the key doesn't exist in the result dictionary, create it
        if (group1, group2) not in result:
            result[(group1, group2)] = []

        # Append the tuple (index, matrix) to the corresponding entry in the dictionary
        result[(group1, group2)].append((int(match[0]), matrix1))
        result[(group1, group2)].append((int(match[0]), matrix2))

# Print the result
print(result)



