"""
a = [1, 2, 3]


def permute(start,end):
    if start == end:
        print(a)
        return
    for i in range(start,end+1):
        a[start],a[i] = a[i],a[start]
        permute(start+1,end)
        a[start], a[i] = a[i], a[start]


permute(0,len(a)-1)
print("permutatin end")

n = 3
arr = [0]*n


count = 0
def combinat(i):
    if i == n:
        global count
        count = count+1
        print(arr)
        return
    arr[i] = 0
    combinat(i+1)
    arr[i] = 1
    combinat(i+1)
    arr[i] = 2
    combinat(i + 1)


combinat(0)
print(count)
print("1D array combination end")


n = 2
arr = [[0 for i in range(n)] for j in range(n)]

def myprint():
    print("arr start")
    for i in range(n):
        for j in range(n):
            print(arr[i][j], end=' ')
        print("\n")
    print("arr end")
#myprint()

count = 0
def combinat2Darray(i,j):
    #print("Recurse: i: ",i," j ",j)
    if i == n and j == n:
        global count
        count = count+1
        myprint()
        return
    arr[i][j] = 0
    new_j = j+1
    new_i = i
    if new_j == n:
        if new_i != n-1:
            new_j = 0
        new_i = i+1

    combinat2Darray(new_i,new_j)
    arr[i][j] = 1
    combinat2Darray(new_i,new_j)
    arr[i][j] = 2
    combinat2Darray(new_i, new_j)


combinat2Darray(0,0)
print(count)
print("2D array combination end")



"""

n = 3
arr = [[0 for i in range(n)] for j in range(n)]

def mapstates(state):
    h = 0
    for i in range(3):
        for j in range(3):
            h = 3 * h + state[i][j]
    return h

def gameover_old(state):
    for id in range(1,3):
        ##  row check
        for i in range(3):
            res = True
            for j in range(3):
                if state[i][j] != id:
                    res = False
                    continue
            if res == True:
                return id

        ##  col check
        for i in range(3):
            res = True
            for j in range(3):
                if state[j][i] != id:
                    res = False
                    continue
            if res == True:
                return id

        ## Diag check
        if (state[0][0] == id) and (state[1][1] == id) and (state[2][2] == id):
            return id
        if (state[0][2] == id) and (state[1][1] == id) and (state[2][0] == id):
            return id

    #Check if it's a tie and game is ended
    for i in range(n):
        for j in range(n):
            if state[i][j] == 0:   # means game is still going on as there is a 0 remaining
                return False

    return 3   # 3 is Tie



def myprint():
    print("arr start")
    for i in range(n):
        for j in range(n):
            print(arr[i][j], end=' ')
        print("\n")
    print("arr end")
#myprint()




n = 3
all_states = []

from enum import IntEnum

class WinId(IntEnum):
    ROW1 = 1
    ROW2 = 2
    ROW3 = 3
    COL1 = 4
    COL2 = 5
    COL3 = 6
    DIAG1 = 7
    DIAG2 = 8

#print(int(WinId.DIAG2))


def gameover(state,winHash):
    for id in range(1,3):
        ##  row check
        for i in range(3):
            res = True
            for j in range(3):
                if state[i][j] != id:
                    res = False
                    continue
            if res == True:
                #print("id: ",id," i: ",i)
                winHash[id][i] = True
                #return id

        ##  col check
        for i in range(3):
            res = True
            for j in range(3):
                if state[j][i] != id:
                    res = False
                    continue
            if res == True:
                winHash[id][i+3] = True
                #return id

        ## Diag check
        if (state[0][0] == id) and (state[1][1] == id) and (state[2][2] == id):
            winHash[id][6] = True
            #return id
        if (state[0][2] == id) and (state[1][1] == id) and (state[2][0] == id):
            winHash[id][7] = True
            #return id

    #Check if it's a tie and game is ended
    for i in range(n):
        for j in range(n):
            if state[i][j] == 0:   # means game is still going on as there is a 0 remaining
                return False

    return True   # 3 is Tie


winningmove = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]

invalid_state = []

def count1and2(state):
    count1 = 0
    count2 = 0
    for x in state:
        for y in x:
            if y == 1:
                count1 = count1 + 1
            elif y == 2:
                count2 = count2 + 1
    return count1, count2

import random
dummystate = [[random.randint(0,2) for i in range(3)] for j in range(3)]
#print(dummystate)
#print(count1and2(dummystate))

def generate_tictactoe_iterative():
    global winHash
    c = 0
    while c < 262144:
        valid = True
        valid &= (c & 3) < 3
        valid &= ((c >> 2) & 3) < 3
        valid &= ((c >> 4) & 3) < 3
        valid &= ((c >> 6) & 3) < 3
        valid &= ((c >> 8) & 3) < 3
        valid &= ((c >> 10) & 3) < 3
        valid &= ((c >> 12) & 3) < 3
        valid &= ((c >> 14) & 3) < 3
        valid &= ((c >> 16) & 3) < 3
        if valid:
            i = c
            j = 0
            state = [[0 for x in range(n)] for y in range(n)] #[0 for x in range(n*n)]#[[0 for x in range(n)] for y in range(n)]
            for x in range(n):
                for y in range(n):
                    state[x][y] = i & 3
                    i >>= 2
                    j = j + 1
            winHash = [[False for i in range(n * n - 1)] for j in range(3)]   # but use index 1,2 only of winhash rows as player id 1 ,2 are possible
            #print(winHash)
            cnt1, cnt2 = count1and2(state)
            if abs(cnt1 - cnt2) > 1:
                c = c + 1
                continue
            if cnt1 < cnt2:
                c = c + 1
                continue
            if cnt1 == cnt2 and gameover_old(state) == 1:
                c = c + 1
                continue
            if cnt1 > cnt2 and gameover_old(state) == 2:
                c = c + 1
                continue
            count = 0
            """
            gameover(state, winHash)
            for x in winHash:
                if x == winHash[0]:
                    #print("x: ",x)
                    continue
                for y in x:
                    if y:
                        count = count + 1
            """
            if count > 1:
                invalid_state.append(state)
            else:
                all_states.append(state)
        c = c + 1
    return

generate_tictactoe_iterative()
print("******************ITERATIVE START********************")
print(len(all_states))
print(all_states)
print(len(invalid_state))
print(invalid_state)



print("******************JJ RECURSE START********************")
jj_all_state = []
jj_invalid_state = []

state = [[0 for i in range(n)] for j in range(n)]


def combinat2Darray(i,j):
    #print("Recurse: i: ",i," j ",j)
    if i == n and j == n:
        """winHash = [[False for i in range(n * n - 1)] for j in
                   range(3)]  # but use index 1,2 only of winhash rows as player id 1 ,2 are possible"""
        cnt1, cnt2 = count1and2(state)
        if abs(cnt1 - cnt2) > 1:
            return
        if cnt1 < cnt2:
            return
        if cnt1 == cnt2 and gameover_old(state) == 1:
            return
        if cnt1 > cnt2 and gameover_old(state) == 2:
            return
        count = 0
        """
        gameover(state, winHash)
        for x in winHash:
            #print(x)
            if x == winHash[0]:
                #print("x: ",x)
                continue
            for y in x:
                if y:
                    count = count + 1
        """
        newstate = [x[:] for x in state]
        if count > 1:
            jj_invalid_state.append(newstate)
        else:
            jj_all_state.append(newstate)

        #newstate = [x[:] for x in state]
        #jj_all_state.append(newstate)
        #myprint()
        return
    state[i][j] = 0
    new_j = j+1
    new_i = i
    if new_j == n:
        if new_i != n-1:
            new_j = 0
        new_i = i+1

    combinat2Darray(new_i, new_j)
    state[i][j] = 1
    combinat2Darray(new_i, new_j)

    state[i][j] = 2
    combinat2Darray(new_i, new_j)



#all_state.append(state)
combinat2Darray(0,0)
print(jj_all_state)
print(len(jj_all_state))
print(jj_invalid_state)
print(len(jj_invalid_state))
print("my recurse array combination end")

