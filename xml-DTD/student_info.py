#coding=utf-8

class student:
	def __init__(self,sname,sid,sgrade,scontact,street,city,provience,idx):
		self.__sname = sname
		self.__sid = sid
		self.__sgrade = sgrade
		self.__scontact = scontact
		self.__street = street
		self.__city = city
		self.__provience = provience
		self.__idx = idx

	def print_info(self):
		print "========================================"
		print "This is the No.%s student's information:"%self.__idx
		print " ---> Name : %s <--- "%self.__sname
		print " ---> ID : %s <--- "%self.__sid
		print " ---> Grade : %s <--- "%self.__sgrade
		print " ---> Contact : %s <--- "%self.__scontact
		print " ---> Student ADDR <--- "
		print " ---> Street : %s <--- "%self.__street
		print " ---> City : %s <--- "%self.__city
		print " ---> Provience : %s <--- "%self.__provience
		print "========================================"
