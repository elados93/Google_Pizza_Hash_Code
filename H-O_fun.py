import random
def all_shapes(width,height,L,H,i,j):
    max_ex_right = min(width-j,H)
    max_ex_down = min(height-i,H)
    min_squers = 2*L
    all_op = []
    for index2 in range(i,i+max_ex_down):
        for index in range(j,j+max_ex_right):
            if (index*index2 >= 2*L) and (index*index2 <= H):
                all_op.append([index2,index])
    return all_op