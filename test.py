l1 = [(1, 1), (2, 2), (3, 3)]
l2 = [(1, 1), (2, 2), (4, 4)]
temp1 = [x for x in l1 if x not in l2][0]
temp2 = [x for x in l2 if x not in l1][0]
print(temp1)
print(temp2)