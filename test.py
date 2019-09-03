received_msg_ = ["090 0000FFFF11111111", "090 0000AAAAFFFFFFFF"]
response_list = ["090 0000FFFF11111111", "090 XXXXXXXXFFFFFFFF", "090 0000AAAAFFFFFFFA"]
msg_to_remove = []
for received_msg in received_msg_:
    id = received_msg.split(' ')[0]
    msg = received_msg.split(' ')[1]
    #self.view.printMsg("received: " + received_msg + "\n")
    for i in range(len(response_list)):
        check_id = response_list[i].split(' ')[0]
        check_msg = response_list[i].split(' ')[1]
        msg_match = True
        if check_id == id:
            for j in range(len(msg)):
                if check_msg[j] != "X":
                    if check_msg[j] != msg[j]:
                        msg_match = False
            if msg_match:
                msg_to_remove.append(response_list[i])
for i in msg_to_remove:
    response_list.remove(i)
print(response_list)