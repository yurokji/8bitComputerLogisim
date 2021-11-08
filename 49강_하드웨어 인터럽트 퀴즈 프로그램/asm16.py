
from PIL import Image
from itertools import chain
import numpy as np
import re
import array


def array2PIL(arr, size):
    mode = 'RGB'
    arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = np.c_[arr, 255*np.ones((len(arr),1), np.uint8)]
    return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)


def convColor24To16(color_in):
    rmax = 2**5 - 1
    gmax = 2**6 - 1
    bmax = 2**5 - 1
    r = int(round(color_in[0] * (rmax / 255)))
    g = int(round(color_in[1] * (gmax / 255)))
    b = int(round(color_in[2] * (bmax / 255)))
    color_out = r << 11
    color_out = color_out | (g << 5)
    color_out = color_out | b
    return color_out





import sys
from nltk.tokenize import word_tokenize
import array as arr

IMPLIED_MODE = 0
ONE_VALUE_MODE = 1
ONE_REG_MODE = 2
TWO_REG_MODE = 3
ONE_REG_ONE_VALUE_MODE = 4
ONE_SHORT_VALUE_MODE = 5


lines = []
nextAddr = 0
currAddr = 0
labels = {}
notyetlabels = []
szRAM = 2 ** 16
binData = arr.array('H', [0] * szRAM)



INST_DIC = {
	'CLF':		[0X06, IMPLIED_MODE],
	'HLT':		[0X99, IMPLIED_MODE],
	'NOP':		[0X90, IMPLIED_MODE],
	'RET': 		[0x61, IMPLIED_MODE],
	'RETI': 	[0x0F, IMPLIED_MODE],


	'LD': 		[0x22, TWO_REG_MODE],
	'LDI': 		[0x23, ONE_REG_ONE_VALUE_MODE],
	'ST': 		[0x28, TWO_REG_MODE],
	'STI': 		[0x29, ONE_REG_ONE_VALUE_MODE],

	'INPORT':	[0X71, ONE_SHORT_VALUE_MODE],
	'OUTPORT':	[0X72, ONE_SHORT_VALUE_MODE],
	'IND':		[0X77, ONE_REG_MODE],
	'INA':		[0X78, ONE_REG_MODE],
	'OUTD':		[0X79, ONE_REG_MODE],
	'OUTA':		[0X7a, ONE_REG_MODE],


	'MOV': 		[0x1a, TWO_REG_MODE],
	'MOVI': 	[0x1b, ONE_REG_ONE_VALUE_MODE],
	'MVXI': 	[0x1c, ONE_REG_ONE_VALUE_MODE],
	'PUSH': 	[0x1d, ONE_REG_MODE],
	'POP': 		[0x1e, ONE_REG_MODE],
	'CALL':		[0x60, ONE_VALUE_MODE],

	'JMP': 		[0x3a, ONE_REG_MODE],
	'JPI':		[0x3b, ONE_VALUE_MODE],

	'BRC':		[0x41, ONE_VALUE_MODE],
	'BRA': 		[0x42, ONE_VALUE_MODE],
	'BRE': 		[0x43, ONE_VALUE_MODE],
	'BRZ': 		[0x44, ONE_VALUE_MODE],

	'BRNC':		[0x48, ONE_VALUE_MODE],
	'BRNA': 	[0x49, ONE_VALUE_MODE],
	'BRNE': 	[0x4a, ONE_VALUE_MODE],
	'BRNZ': 	[0x4b, ONE_VALUE_MODE],


	'ADD':		[0xc0, TWO_REG_MODE],
	'SUB':		[0xc1, TWO_REG_MODE],
	'INC':		[0xc2, ONE_REG_MODE],
	'DEC':		[0xc3, ONE_REG_MODE],
	'SHR':		[0xc8, ONE_REG_MODE],
	'SHL':		[0xc9, ONE_REG_MODE],
	'NOT':		[0xca, ONE_REG_MODE],
	'AND':		[0xcb, TWO_REG_MODE],
	'OR':		[0xcc, TWO_REG_MODE],
	'XOR':		[0xcd, TWO_REG_MODE],
	'CMP':		[0xcf, TWO_REG_MODE],

	'ADI':		[0xd0, ONE_REG_ONE_VALUE_MODE],
	'SBI':		[0xd1, ONE_REG_ONE_VALUE_MODE],
	'SRI':		[0xd8, ONE_REG_ONE_VALUE_MODE],
	'SLI':		[0xd9, ONE_REG_ONE_VALUE_MODE],
	'NTI':		[0xda, ONE_REG_ONE_VALUE_MODE],
	'ANI':		[0xdb, ONE_REG_ONE_VALUE_MODE],
	'ORI':		[0xdc, ONE_REG_ONE_VALUE_MODE],
	'XRI':		[0xdd, ONE_REG_ONE_VALUE_MODE],
	'CPI':		[0xdf, ONE_REG_ONE_VALUE_MODE],
}

for i in range(szRAM):
	binData[i] = INST_DIC['NOP'][0] << 8


def readFile(fn):
	outLines = []
	with open(fn, encoding='UTF-8') as f:
		for line in f:
			outLines.append(line)
	return outLines

def preProcess(lines):
	res = []
	print('preprocessing....')
	for i, line in enumerate(lines):
		if len(line.strip()) > 0 and line[0] != '#':
			line = line.replace('\n', '')
			line = line.strip()
			
			if line[:5].strip() == ".TEXT":
				line = line.split("@@")
				line[0] = line[0].strip()
			else:
				line = word_tokenize(line)
			res.append(line)
		# print(line)
	return res


def isAddr16bit(s):
	# 24 비트 주소내에 포함되는지 검사
	if s >= 0 and s <= 0xffff:
		return True
	else:
		return False


def isWord16bit(s):
	# 16비트 워드 안에 포함되는지 검사
	if s >= 0 and s <= 0xffff:
		return True
	else:
		return False


def inRegSize(num):
	# r00 부터 r15까지만 쓸 수 있음
	if num >= 0 and num < 16:
		return True
	else:
		return False





#  토큰 형식 (예) : '.ORG', '$', 'F10A'
def isOrg(l):
	num_tokens = len(l)
	try:
		if num_tokens == 3 and l[0] == '.ORG' and l[1] == '$':
			val = int('0x'+l[2], 0)
			if isAddr16bit(val):
				return True
			else:
				return False
		else:
			return False
	except:
		print(l, "is wrong")
		sys.exit()

#  토큰 형식 (예) : 'NEXTBIT', ':'
def isLabel(l):
	num_tokens = len(l)
	if num_tokens == 2 and l[0][0].isalpha() and l[1] == ':':
		return True
	else:
		return False



def isWord(l):
	num_tokens = len(l)
	try:
		if num_tokens == 3 and l[0] == '.WORD' and l[1] == '$':
			val = int('0x'+l[2], 0)
			if isWord16bit(val):
				return 1
			else:
				return False

		elif num_tokens == 3 and l[0] == '.WORD' and l[1] == '@':
			return 2
		else:
			return False
	except:
		print (l, 'is wrong!')
		sys.exit()  


def isText(l):
	num_tokens = len(l)
	if num_tokens == 2 and l[0] == '.TEXT':
		return True
	else:
		return False



# 
def ConvHexListToVal(hexData):
	addr = 0x00000000
	addr = hexData[0] << 8
	addr += hexData[1]
	return addr


#  토큰 형식 (예) : 'CLF'
def isImpliedMode(l):
	num_tokens = len(l)
	if num_tokens == 1 and INST_DIC[l[0]][1] == IMPLIED_MODE :
		return True
	else:
		return False


#  짧은 주소 모드
def isOneValueMode(l):
	num_tokens = len(l)
	# 1번 예) : 'BRC', 'GOADD' 
	if num_tokens == 3 and INST_DIC[l[0]][1] == ONE_VALUE_MODE and l[1] == '$' and isAddr16bit(int('0x'+l[2], 0)):
		return 1
	elif num_tokens == 3 and INST_DIC[l[0]][1] == ONE_VALUE_MODE and l[1] == '@':
		return 2
	else:
		return False


#  짧은 주소 모드
def isOneShortValueMode(l):
	num_tokens = len(l)
	# 1번 예) : 'BRC', 'GOADD' 
	if num_tokens == 3 and INST_DIC[l[0]][1] == ONE_SHORT_VALUE_MODE and l[1] == '$' and isAddr16bit(int('0x'+l[2], 0)):
		return 1
	elif num_tokens == 3 and INST_DIC[l[0]][1] == ONE_SHORT_VALUE_MODE and l[1] == '@':
		return 2
	else:
		return False




#  토큰 형식 (예) : 'NOT', 'R12'
def isOneRegMode(l):
	num_tokens = len(l)
	if num_tokens == 2 and INST_DIC[l[0]][1] == ONE_REG_MODE:
		rb = l[1]
		if rb[0] == 'R' and inRegSize(int(rb[1:])):
			if l[0] == 'PUSH' or l[0] == 'POP':
				return 1
			else:
				return 2
		else:
			return False
	return False

#  토큰 형식 (예) : 'ADD',  'R5',  ',',  'R14'
def isTwoRegRegMode(l):
	num_tokens = len(l)
	if num_tokens == 4 and l[2] == ',' and INST_DIC[l[0]][1] == TWO_REG_MODE:
		ra = l[1]
		rb = l[3]
		if ra[0] == 'R' and inRegSize(int(ra[1:])) and rb[0] == 'R' and inRegSize(int(rb[1:])):
			return True
		else:
			return False
	else:
		return False

#  토큰 형식 (예) : 'MOVI',  'R0',  ',',  '$',  'FF4210FF'
def isOneRegOneValueMode(l):
	num_tokens = len(l)
	if INST_DIC[l[0]][1] == ONE_REG_ONE_VALUE_MODE:
		if   num_tokens == 5 and l[1][0] == 'R' and inRegSize(int(l[1][1:])) and l[2] == ',' and l[3] == '$' and isWord16bit(int('0x'+l[4], 0)):
			return 1
		elif num_tokens == 5 and l[1] == 'SP' and l[2] == ',' and l[3] == '$' and isWord16bit(int('0x'+l[4], 0)):
			return 2
		elif num_tokens == 5 and l[1][0] == 'R' and inRegSize(int(l[1][1:])) and l[2] == ',' and l[3] == '@':
			return 3
		else:
			return False
	else:
		return False



def parseCommand(tokens):
	global nextAddr
	global notyetlabels
	if isOrg(tokens):
		newOrigin = int('0x'+tokens[2], 0)
		nextAddr = newOrigin
		# print ("@NEXT ADDR:", format(nextAddr, '06x'))
		return None

	elif isLabel(tokens):
		labels[tokens[0]] = nextAddr
		# print(labels)
		return None

	elif isWord(tokens) == 1:
		# print("@WORD : ",format(nextAddr,'08x'))
		val = int('0x'+tokens[2], 0)
		nextAddr = currAddr + 1
		return [val]

	elif isWord(tokens) == 2:
		# print("@WORD : ",format(nextAddr,'08x'))
		val = ord(tokens[2])
		nextAddr = currAddr + 1
		return [val]
	
	elif isText(tokens):
		text = []
		val = 0
		print(tokens)
		for i, ch in enumerate(tokens[1]):
			if i < len(tokens[1]) - 1 and tokens[1][i] == '\\':
				if  tokens[1][i+1] == 'n':
					val = 0xA
					text.append(val)
					nextAddr = currAddr + 1
				elif  tokens[1][i+1] == ' ':
					val = ord(tokens[1][i])
					text.append(val)
					nextAddr = currAddr + 1
				elif  tokens[1][i+1] == 't':
					val = 0x9
					text.append(val)
					nextAddr = currAddr + 1
				elif  tokens[1][i+1] == '0':
					val = 0x3
					text.append(val)
					nextAddr = currAddr + 1
			elif i > 0 and tokens[1][i-1] == '\\':
				continue
			else:
				val = ord(tokens[1][i])
				text.append(val)
				nextAddr = currAddr + 1
			print('count:', len(text))
		return text


	elif isImpliedMode(tokens):
		op_code = INST_DIC[tokens[0]][0]
		hexData = [op_code, 0]
		val = ConvHexListToVal(hexData)
		nextAddr = currAddr + 1
		# print(val)
		return [val]


		# 분기할 주소가 숫자로 되어 있을 때 1
	elif isOneShortValueMode(tokens) == 1:
		op_code = INST_DIC[tokens[0]][0]
		operand = int('0x'+tokens[2], 0)
		hexData = [op_code, operand]
		val1 = ConvHexListToVal(hexData)
		nextAddr = currAddr + 1
		return [val1]

		# 분기할 주소가 숫자로 되어 있을 때 1
	elif isOneValueMode(tokens) == 1:
		op_code = INST_DIC[tokens[0]][0]
		hexData = [op_code, 0]
		val1 = ConvHexListToVal(hexData)
		val2 = int('0x'+tokens[2], 0)
		nextAddr = currAddr + 2
		return [val1, val2]

		# 분기할 주소가 라벨명으로 되었을때 2
	elif isOneValueMode(tokens) == 2:
		# print(tokens)
		op_code = INST_DIC[tokens[0]][0]
		hexData = [op_code, 0]
		val1 = ConvHexListToVal(hexData)
		if tokens[2] in labels:
			val2 = labels[tokens[2]]
		# 만약 아직 라벨을 만나지 못했다면 그냥 0으로 주소를 채워준다
		# 그리고 아직 처리되지 못한 라벨을 저장한다
		else:
			notyetlabels.append({tokens[2]: [2, currAddr]})
			val2 = 0
		nextAddr = currAddr + 2
		return [val1, val2]




	elif isOneRegMode(tokens) == 1:
		rb = int(tokens[1][1:])
		op_code = INST_DIC[tokens[0]][0]
		hexData = [op_code, rb]
		val = ConvHexListToVal(hexData)
		nextAddr = currAddr + 1
		return [val]

	elif isOneRegMode(tokens) == 2:
		rb = int(tokens[1][1:])
		op_code = INST_DIC[tokens[0]][0]
		hexData = [op_code, rb]
		val = ConvHexListToVal(hexData)
		nextAddr = currAddr + 1
		return [val]

	elif isTwoRegRegMode(tokens):
		ra = int(tokens[1][1:])
		rb = int(tokens[3][1:])
		reg = (ra << 4) | rb
		op_code = INST_DIC[tokens[0]][0]
		hexData = [op_code, reg]
		val = ConvHexListToVal(hexData)
		nextAddr = currAddr + 1
		return [val]

	elif isOneRegOneValueMode(tokens) == 1:
		rb = int(tokens[1][1:])
		val2 = int('0x'+tokens[4], 0)
		op_code = INST_DIC[tokens[0]][0]
		hexData = [op_code, rb]
		val1 = ConvHexListToVal(hexData)
		nextAddr = currAddr + 2
		return [val1, val2]
	
	elif isOneRegOneValueMode(tokens) == 2:
		# rb = int(tokens[1][1:])
		val2 = int('0x'+tokens[4], 0)
		op_code = INST_DIC[tokens[0]][0] + 1
		hexData = [op_code, 0]
		val1 = ConvHexListToVal(hexData)
		nextAddr = currAddr + 2
		return [val1, val2]

	elif isOneRegOneValueMode(tokens) == 3:
		rb = int(tokens[1][1:])
		op_code = INST_DIC[tokens[0]][0]
		hexData = [op_code, rb]
		val1 = ConvHexListToVal(hexData)
		if tokens[4] in labels:
			val2 = labels[tokens[4]]
		# 만약 아직 라벨을 만나지 못했다면 그냥 0으로 주소를 채워준다
		# 그리고 아직 처리되지 못한 라벨을 저장한다
		elif tokens[4] == 'ADDR_USER_INPUT':
			val2 = 0x6000
		else:
			notyetlabels.append({tokens[4]: [2, currAddr]})
			val2 = 0
		nextAddr = currAddr + 2
		return [val1, val2]

	else:
		print(tokens, 'NO SUCH COMMAND!')
		sys.exit()










# 어셈블리 파일을 읽어들여서 명령 코드로 해독한 후 바이너리 파일을 만듭니다
lines = readFile(sys.argv[1])
toklines = preProcess(lines)
# print(toklines)

allLines = []
for i, toks in enumerate(toklines):
	resData = parseCommand(toks)
	if resData != None:
		idx = currAddr
		for _, val in enumerate(resData):
			binData[idx] = val
			allLines.append(idx)
			idx += 1
	currAddr = nextAddr



# 아직 라벨 주소 치환이 되지 않은 부분이 있어 그것을 처리

# print(notyetlabels)
for _, notlabels in enumerate(notyetlabels):
	for key, value in notlabels.items():
		# 주소는 2번째 입력 바이트이기에 라벨 주소에서 1을 더함
		# print(key, value, labels[key])
		if value[0] == 1:
			binData[value[1]] += labels[key]
		else:
			binData[value[1] + 1] = labels[key]

print("Machine Language Code")
for _, idx in enumerate(allLines):
	print(format(idx, '04x'), format(binData[idx], '04x'))


# 처리된 바이너리 데이터를 파일에 저장
fw = open(sys.argv[1][:-4]+'.bin', 'wb')





im = Image.open("messi.jpg")
# im = Image.fromarray(np.array(Image.open(imgName)).astype("uint16"))
print("Image mode: ",im.mode)
im2 = Image.new(im.mode, im.size)
pix = im.load()
width = im.size[0]
height = im.size[1]


offset = 0x1000
count = 0
for i in range(width):
    for j in range(height):
        col_in = list(pix[j, i])
        binData[offset + count] = convColor24To16(col_in)
        count += 1

binData.tofile(fw)
fw.close()
