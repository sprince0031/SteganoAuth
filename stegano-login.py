from PIL import Image
import binascii
import hashlib
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

def retr(filename):
	img = Image.open(filename)
	binary = ''

	if img.mode in ('RGBA'):
		img = img.convert('RGBA')
		datas = img.getdata()

		for item in datas:
			digit = decode(rgb2hex(item[0],item[1],item[2]))
			if digit == None:
				pass
			else:
				binary = binary + digit
				if (binary[-16:] == '1111111111111110'):
					#print "Success"
					return bin2str(binary[:-16])

		return bin2str(binary)
	return "Incorrect Image Mode, Couldn't Retrieve"

print "Welcome to Stegano Auth login!"
print "View project repo @ https://github.com/sprince0031/SteganoAuth | by Sprince0031"
connection = sqlite3.connect("steganoauth.db")
cursor = connection.cursor()

usrname = str(raw_input("Enter user name: ")).upper()
cursor.execute('SELECT usrname FROM Auth WHERE usrname = ?', (usrname, ))
print usrname
row = cursor.fetchone()
if row is None:
	print "Sorry, this username hasn't been registerd yet! Please register and try again."
	exit()
else:
	pwd = raw_input("Enter password: ")
	hashedPwd = hashlib.sha256(pwd).hexdigest()
	cursor.execute('SELECT pwdhash FROM Auth WHERE usrname = ?', (usrname, ))
	row1 = cursor.fetchone()
	dbpwdHash = row1[0]
	if dbpwdHash == hashedPwd:
		FileDest = raw_input("Enter path of image key file in .png format: ")
		try:
			picHash = retr(FileDest)
		except:
			print "Picture file doesn't contain any hidden hash or wrong destination path set! Attempt failed."
			exit()
		if dbpwdHash == picHash:
			print "User credentials authenticated! Logged in..."
		else:
			print "Picture key wrong or corrupted! Attempt failed."
	else:
		print "Entered password wrong! Attempt failed."