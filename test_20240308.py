file1 = open('2233.txt','w')

str = "Hi,ijaiodjha"
with open('2233.txt',mode = 'w') as f:
    size = f.write(str)
    print(size)
str2 = "水晶剑行动"
with open('2233.txt',mode = 'w+',encoding='utf8') as f:
    size2 = f.write(str2)
    print(size2)
file1.writelines('2165463155\nhdjahd hhoihd\n水晶剑行动')
with open('2233.txt',mode = 'w+',encoding='utf8') as f:
    file1.close()
    print(file1.closed)