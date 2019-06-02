import random, time, pickle, socket

Y_SPEED = 1
X_SPEED = 1
ARR = [400,400,400,400,0,0]

sv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sv_socket.bind(('', 9090))
sv_socket.listen(2)

compound = []

def compounds_waiting():
    while len(compound) < 2:
        connection, address = sv_socket.accept()
        compound.append(connection)
        print(connection)
        print(compound)
		

def info_recieving():
    info_pl1 = pickle.loads(compound[0].recv(1024))
    info_pl2 = pickle.loads(compound[1].recv(1024))
    return info_pl1, info_pl2


def set_position(array, pl1, pl2):

    global Y_SPEED, X_SPEED
	
	  if pl1[1] == True:
        array[0]+=1
    else:
        array[0] = array[0]

    if pl1[0] == True:
        array[0]-=1
    else:
        array[0] = array[0]
		
    if pl2[0] == True:
        array[1]-=1
    else:
        array[1] = array[1]
		
    if pl2[1] == True:
        array[1]+=1
    else:
        array[1] = array[1]

    if array[0]<0:
        array[0] = 0
    elif array[0] > 540:
        array[0] = 540

    if array[1]<0:
        array[1] = 0
    elif array[1] > 540:
        array[1] = 540

    array[2] += round(Y_SPEED)
    array[3] += round(X_SPEED)
	speed_pos = [-1, -1.05, -1.1, -1.15, -1.2, -1.25, -1.3, -1.35, -1.4, -1.45, -1.5]
    speed_neg = [-0.6, -0.65, -0.7, -0.75, -0.8, -0.85, -0.9, -0.95, -1]
	
    if array[2] < 0:
        if Y_SPEED >= 1:
            Y_SPEED *= random.choice(speed_neg)
        elif Y_SPEED < 1:
            Y_SPEED *= random.choice(speed_pos)
			
    if array[3]>795:
        if X_SPEED >= 1:
            X_SPEED *= random.choice(speed_neg)
        elif X_SPEED < 1:
            X_SPEED *= random.choice(speed_pos)
        array[4] += 1
		
    if array[2] > 595:
        if Y_SPEED >= 1:
            Y_SPEED *= random.choice(speed_neg)
        elif Y_SPEED < 1:
            Y_SPEED *= random.choice(speed_pos)
			
    if array[3]<0:
        if X_SPEED >= 1:
            X_SPEED *= random.choice(speed_neg)
        elif X_SPEED < 1:
            X_SPEED *= random.choice(speed_pos)
        array[5] += 1
		
    if array[3]<20 and (array[0]<array[2] and array[0]+60>array[2]):
        X_SPEED *=-1
		
    if array[3]>780 and (array[1]<array[2] and array[1]+60>array[2]):
        X_SPEED *=-1

    return array

while True:
    compounds_waiting()
    data_arr = pickle.dumps(ARR)
    print(data_arr)
    compound[0].send(data_arr)
    compound[1].send(data_arr)
    player_1, player_2 = info_recieving()
    ARR = set_position(ARR, player_1, player_2)