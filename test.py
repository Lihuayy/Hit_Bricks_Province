#打印商品

print('此商品清仓大甩卖所有商品打九折')
print('金士顿U盘8G-----40元/个')
print('胜创16GTF卡-----50元/个')
print('读卡器-----------8元/个')
print('网线两米--------5元/根')





# 输入购买数量 并赋值到 opq
opq1 = int(input('金士顿U盘8G购买的数量:'))
opq2 = int(input( '胜创16GTF卡购买的数国:'))
opq3 = int(input('读卡器购买的数量:'))
opq4 = int(input('网线两米购买的数里:'))
opq5 = int(input('你拥有的金顿: '))

#物品价格 ， 并赋值到a
a1 = 40
a2 = 50
a3 = 8
a4 = 5

# 总购买数量
Sum1 = opq1+opq2+opq3+opq4

# 每个物品购买后的价格
money1= opq1*a1 # 购买全士顿U盘的数量购买金士顿U盘的价格
money2 = opq2*a2
money3 = opq3*a3
money4 = opq4*a4
sum2 = money1+money2+money3+money4 #购买的总价格
#sum3=sum2*0.9#打九折
QQQ = opq5+sum2



# %5表示字符品，%d表示整数 ， %.nf来指定浮点数的小数位数，其中n是要显示的小数位数。
print('='*35)
print('名称            数量    单价       金额'                )
print('金士顿U盘8G       %s     %.2f      %.2f'%(opq1,a1,money1))
print('胜创16GTF卡       %s     %.2f      %.2f'%(opq2,a2,money2))
print('读卡器            %s     %.2f       %.2f'%(opq3,a3,money3))
print('网线两米          %s      %.2f      %.2f'%(opq4,a4,money4))



if opq5 < sum2:
  print('余费不足,支付失败')
else:
     print('实败:%.2f’ '% sum2 +'找零:% 2f'% QQQ)
     print( '购物成功,欢迎下次光临')
     print('收银:管理员')
     print('*'*35)


