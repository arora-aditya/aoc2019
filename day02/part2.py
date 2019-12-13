with open("input.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        for j in range(1, 100):
            for k in range(1, 100):
                li = list(map(lambda x: int(x), line.split(',')))
                li[1] = j
                li[2] = k
                for i in range(0, len(li), 4):
                    opcode = li[i]
                    if opcode == 1:
                        i1, i2, i3 = li[i+1], li[i+2], li[i+3]
                        li[i3] = li[i1] + li[i2]
                    elif opcode == 2:
                        i1, i2, i3 = li[i+1], li[i+2], li[i+3]
                        li[i3] = li[i1] * li[i2]
                    elif opcode == 99:
                        break
                    else:
                        break
                if li[0] == 19690720:
                    # print(li)
                    print(li[1]*100 + li[2])
                    break
                    

# 6979

