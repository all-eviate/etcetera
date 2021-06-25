import pickle

with open('comment.pickle', 'rb') as fr:
    comment = pickle.load(fr)

on = True

while on:
    print("1: add record\n2: delete record\n3: fix record\n4: view dict\n5: search dict by key\n0: exit")
    command = input("INPUT COMMAND: ")
    if command == '1':
        key = input("Input key (detail) : ")
        val = input("Input value (category) : ")
        if key not in comment:
            comment[key] = val
        else:
            print("ERROR: KEY ALREADY EXISTS")
    elif command == '2':
        key = input("Input key : ")
        if key not in comment:
            print("ERROR: KEY NOT FOUND")
        else:
            del comment[key]
    elif command == '3':
        key = input("Input key (detail) : ")
        if key not in comment:
            print("ERROR: KEY NOT FOUND")
        else:
            val = input("Input new value : ")
            del comment[key]
            comment[key] = val
    elif command == '4':
        print(comment)
    elif command == '5':
        key = input("Input key (detail) : ")
        if key in comment:
            print(comment[key])
        else:
            print('no result')
    elif command == '0':
        on = False

with open('comment.pickle', 'wb') as fw:
    pickle.dump(comment, fw)
