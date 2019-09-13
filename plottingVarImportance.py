
import matplotlib.pyplot as plt

outFile = open('out.log')
importanceList = []
variableList = []

for line in outFile.readlines():
    if 'importance' in line:
        importanceList.append(line.split("importance :  ")[1].split("      variable :  ")[0])
        variableList.append(line.split("importance :  ")[1].split("      variable :  ")[1])

# print importanceList
# print variableList
plt.plot(importanceList)
xTicks = []
xTicks.append((value*0.1)-0.5 for value in range(0,1))
plt.xticks(xTicks, variableList)
plt.show()


