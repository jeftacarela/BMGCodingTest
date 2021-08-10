
# for i in range (x, 1):
#     if i%3 == 0:
#         print('Frontend')
#     if i%5 ==0:
#         print('Backend')
#     else:
#         print(i)
j = []
i = 1
while(i <= 50):
    if i%3==0 and i%5 == 0:
        j.append('Frontend Backend')
    elif i%3 == 0:
        j.append('Frontend')
    elif i%5 ==0:
        j.append('Backend')
    else:
        j.append(i)
    i +=1
print(*j, sep=',')