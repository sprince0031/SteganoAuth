from PIL import Image
import binascii
import hashlib
#import random
import sqlite3

def rgb2hex(r, g, b):
	return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex2rgb(hexcode):
	return tuple(map(ord, hexcode[1:].decode('hex')))

def str2bin(message):
	binary = bin(int(binascii.hexlify(message), 16))
	return binary[2:]

def bin2str(binary):
	message = binascii.unhexlify('%x' % int('0b'+binary,2))
	return message

def encode(hexcode, digit):
	if hexcode[-1] in ('0','1', '2', '3', '4', '5'):
		hexcode = hexcode[:-1] + digit
		return hexcode
	else:
		return None

def decode(hexcode):
	if hexcode[-1] in ('0', '1'):
		return hexcode[-1]
	else:
		return None

def rand():
	randNums = list()
	randArg = random.randint(1,1001)
	for x in range(10):
		randNums.append(random.randint(1,randArg))
	return randNums

def hide(filename, message):
	img = Image.open(filename)
	binary = str2bin(message) + '1111111111111110'
	if img.mode in ('RGBA'):
		img = img.convert('RGBA')
		datas = img.getdata()

		newData = []
		digit = 0
		temp = ''
		for item in datas:
			if digit < len(binary):
				newpix = encode(rgb2hex(item[0],item[1],item[2]),binary[digit])
				if newpix == None:
					newData.append(item)
				else:
					r, g, b = hex2rgb(newpix)
					newData.append((r,g,b,255))
					digit += 1
			else:
				newData.append(item)
		img.putdata(newData)
		#randNum = rand()
		#keyNum = randNum[random.randint(0,10)]
		#keyPic = filename[:len(filename) - 4] + str(keyNum) + ".png"
		img.save(filename[:len(filename)-4] + "-key.png", "PNG")
		print "Picture key is saved @ location " + filename + " ."
        #print "Please rename the picture file, removing the pin, for safety!"
        #print "Your pin number is " + str(keyNum)
        return "Completed!"

	return "Incorrect Image Mode, Couldn't Hide"

print "Welcome to Stegano Auth registration!"
print "View project repo @ https://github.com/sprince0031/SteganoAuth | by Sprince0031"
connection = sqlite3.connect("steganoauth.db")
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Auth (usrname NVARCHAR(32), pwdhash NVARCHAR(256))')

usrname = str(raw_input("Enter new user name: ")).upper()
cursor.execute('SELECT usrname FROM Auth WHERE usrname = ?', (usrname, ))
row = cursor.fetchone()
if row is None:
	pwd = raw_input("Enter password: ")
	if pwd == '' :
		print "No password entered! Aborting..."
		exit()
	hashedPwd = hashlib.sha256(pwd).hexdigest()
	FileDest = raw_input("Enter path of image file in .png format: ")
	cursor.execute('INSERT INTO Auth (usrname, pwdhash) VALUES (?, ?)', (usrname, hashedPwd))
	connection.commit()
	print hide(FileDest, hashedPwd)
else:
	print usrname + " is already registered!"
