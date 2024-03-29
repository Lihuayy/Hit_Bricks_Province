import csv

# 数据来自PPT
string = "姓名,语文, 数学,英语,理综\n刘婧, 124, 137,145,260\n" \
"张华, 116, 143,139,263\n刑邵林,120, 130,148,255\n" \
"鞠依依,115,145,131,240\n黄丽萍,123,108,121,235\n"   \
"赵越,132,100,112,210"

# 将数据写入CSV文件
with open('score_02.csv', 'w', newline='',encoding='utf-8') as csv_file:  # 打开并写入数据
    csv_file.writelines(string)
csv_file = open('score.csv','r',encoding='utf-8')  # 打开CSV文件,以只读方式打开,使用UTF-8编码
file_new = open('count.csv','w+')  # 以写入(更新)的方式创建并打开count.csv
lines = []  # 创建空列表
for line in csv_file:
    line = line.replace('\n', '')
    lines.append(line.split(','))
lines[0].append('总分')  # 添加表头
for i in range(len(lines) - 1):   # 创建表格,长度减1
    idx = i + 1
    sun_score = 0
    for j in range(len(lines[idx])):
        if lines[idx][j].isnumeric():
            sun_score += int(lines[idx][j]) # 将分数相加并转换为整数型
    lines[idx].append(str(sun_score))
for line in lines:
    print(line)
    file_new.write(','.join(line) + '\n')  #使用join函数以换行符分割表格
csv_file.close()
file_new.close()
print(file_new.closed)

