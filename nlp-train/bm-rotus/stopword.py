#coding=utf-8
#to get the stop words set.

def stop_set(sw_path):
    sw_list = []
    with open(sw_path,"rb") as sw_file:
        for line in sw_file.readlines():
            sw_list.append(line.rstrip('\r\n'))
    sw_file.close()
    return set(sw_list)
