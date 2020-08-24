
# write somethong to file example
file = open('txtFile.txt','w')
file.write('aaa 123 456\n')
file.write('bbb 123 789\n')
file.write('ccc 456 789\n')
file.close()

#read file content example
file = open('txtFile.txt','r')
for line in file:
    print(line)
#    world = line.split()
#    print(world)
file.close()

