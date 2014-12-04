#coding=utf-8

'''
input: xml with particular DTD
output: the data_set in the xml
'''

import re
from student_info import student

def get_data(file_path):
    with open(file_path,'rb') as infile:

        student_list = []

        str_tmp = ''
        lines = infile.readlines()
        for line in lines:
            str_tmp += line.rstrip()
        infile.close()

    stu_re = re.compile(r'''<student>(.+?)</student>''',re.DOTALL)
        
    sname_re = re.compile(r'''<sname>(.+?)</sname>''',re.DOTALL)
    sid_re = re.compile(r'''<sID>(.+?)</sID>''',re.DOTALL)
    sgrade_re = re.compile(r'''<sgrade>(.+?)</sgrade>''',re.DOTALL)
    scontact_re = re.compile(r'''<scontact>(.+?)</scontact>''',re.DOTALL)
    street_re = re.compile(r'''<street>(.+?)</street>''',re.DOTALL)
    city_re = re.compile(r'''<city>(.+?)</city>''',re.DOTALL)
    provience_re = re.compile(r'''<provience>(.+?)</provience>''',re.DOTALL)

    stu_list = stu_re.findall(str_tmp)

    for idx,item in enumerate(stu_list):
        s_name = sname_re.findall(item)
        s_id = sid_re.findall(item)
        s_grade = sgrade_re.findall(item)
        s_contact = scontact_re.findall(item)
        s_street = street_re.findall(item)
        s_city = city_re.findall(item)
        s_provience = provience_re.findall(item)
            
        student_list.append(student(s_name,s_id,s_grade,s_contact,s_street,s_city,s_provience,idx+1))
    return student_list

if __name__ == "__main__":
    stu_list = get_data('stu_DTD.xml')
    for stu in stu_list:
        stu.print_info()
