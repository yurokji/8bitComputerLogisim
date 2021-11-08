import sys
from nltk.tokenize import word_tokenize
import array as arr

IMPLIED_MODE = 0
ONE_VALUE_MODE = 1
ONE_REG_MODE = 2
TWO_REG_MODE = 3
ONE_REG_ONE_VALUE_MODE = 4


lines = []
nextAddr = 0
currAddr = 0
labels = {}
notyetlabels = {}
szRAM = 2 ** 24
binData = arr.array('L', [0] * szRAM)

INST_DIC = {
	'LD': 		[0x00, TWO_REG_MODE],
	'ST': 		[0x01, TWO_REG_MODE],
	'DATA': 	[0x02, ONE_REG_ONE_VALUE_MODE],
	'JMPR':		[0x03, ONE_REG_MODE],
	'JMP':		[0x04, ONE_VALUE_MODE],
	'BRC':		[0x41, ONE_VALUE_MODE],
	'BRA': 		[0x42, ONE_VALUE_MODE],
	'BRE': 		[0x43, ONE_VALUE_MODE],
	'BRZ': 		[0x44, ONE_VALUE_MODE],
	'CLF':		[0X06, IMPLIED_MODE],
	'IND':		[0X07, ONE_REG_MODE],
	'INA':		[0X08, ONE_REG_MODE],
	'OUTD':		[0X09, ONE_REG_MODE],
	'OUTA':		[0X0a, ONE_REG_MODE],
	'ADD':		[0x80, TWO_REG_MODE],
	'SHR':		[0x81, ONE_REG_MODE],
	'SHL':		[0x82, ONE_REG_MODE],
	'NOT':		[0x83, ONE_REG_MODE],
	'AND':		[0x84, TWO_REG_MODE],
	'OR':		[0x85, TWO_REG_MODE],
	'XOR':		[0x86, TWO_REG_MODE],
	'CMP':		[0x87, TWO_REG_MODE],
	'HLT':		[0X99, IMPLIED_MODE],
	'NOP':		[0X90, IMPLIED_MODE],
}


def readFile(fn):
	outLines = []
	with open(fn, encoding='UTF-8') as f:
		for line in f:
			outLines.append(line)
	return outLines

def preProcess(lines):
	res = []
	linenum  = 0
	print('preprocessing....')
	for i, line in enumerate(lines):
		if len(line.strip()) > 0 and line[0] != '#':
			line = str(line).upper()
			line = line.replace('\n', '')
			line = word_tokenize(line)
			res.append(line)

	return res

def inAddrRange(s):
	# 24 비트 주소내에 포함되는지 검사
	if s >= 0 and s <= 0xffffff:
		return True
	else:
		return False

def inWordRange(s):
	# 32비트 워드 안에 포함되는지 검사
	if s >= 0 and s <= 0xffffffff:
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
			if inAddrRange(val):
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


# 
def ConvHexListToVal(hexData):
	addr = 0x00000000
	addr = hexData[0] << 24
	addr += hexData[1] << 16
	addr += hexData[2] << 8
	addr += hexData[3]
	return addr


#  토큰 형식 (예) : 'CLF'
def isImpliedMode(l):
	num_tokens = len(l)
	if num_tokens == 1 and INST_DIC[l[0]][1] == IMPLIED_MODE :
		return True
	else:
		return False


#  토큰 형식 두 가지 경우 처리
def isOneValueMode(l):
	num_tokens = len(l)
	# 1번 예) : 'BRC', 'GOADD' 
	if num_tokens == 2 and INST_DIC[l[0]][1] == ONE_VALUE_MODE and l[1][0].isalpha():
		return 1
	# 2번 예)  : 'JMP', '$', '1FFFF' 
	elif num_tokens == 3 and INST_DIC[l[0]][1] == ONE_VALUE_MODE and l[1] == '$' and inAddrRange(int('0x'+l[2], 0)):
		return 2
	else:
		return False


#  토큰 형식 (예) : 'NOT', 'R12'
def isOneRegMode(l):
	num_tokens = len(l)
	if num_tokens == 2 and INST_DIC[l[0]][1] == ONE_REG_MODE:
		ra = l[1]
		if ra[0] == 'R' and inRegSize(int(ra[1:])):
			return True
		else:
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

#  토큰 형식 (예) : 'DATA',  'R0',  ',',  '$',  '10FF'
def isOneRegOneValueMode(l):
	num_tokens = len(l)
	if num_tokens == 5 and l[2] == ',' and INST_DIC[l[0]][1] == ONE_REG_ONE_VALUE_MODE:
		rb = l[1]
		if rb[0] == 'R' and inRegSize(int(rb[1:])) and l[3] == '$' and inWordRange(int('0x'+l[4], 0)):
			return True
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

	elif isImpliedMode(tokens):
		op_code = INST_DIC[tokens[0]][0]
		hexData = [op_code, 0, 0, 0]
		val = ConvHexListToVal(hexData)
		nextAddr = currAddr + 1
		# print(val)
		return [val]

		# 분기할 주소가 라벨명으로 되었을때 1
	elif isOneValueMode(tokens) == 1:
		op_code = INST_DIC[tokens[0]][0]
		hexData = [op_code, 0, 0, 0]
		val1 = ConvHexListToVal(hexData)
		if tokens[1] in labels:
			val2 = labels[tokens[1]]
		# 만약 아직 라벨을 만나지 못했다면 그냥 0으로 주소를 채워준다
		# 그리고 아직 처리되지 못한 라벨을 저장한다
		else:
			notyetlabels[tokens[1]] = currAddr
			val2 = 0
		nextAddr = currAddr + 2
		return [val1, val2]


		# 분기할 주소가 숫자로 되어 있을 때 2로  구분
	elif isOneValueMode(tokens) == 2:
		op_code = INST_DIC[tokens[0]][0]
		hexData = [op_code, 0, 0, 0]
		val1 = ConvHexListToVal(hexData)
		val2 = int('0x'+tokens[2], 0)
		nextAddr = currAddr + 2
		return [val1, val2]


	elif isOneRegMode(tokens):
		rb = int(tokens[1][1:])
		op_code = INST_DIC[tokens[0]][0]
		hexData = [op_code, rb, 0, 0]
		val = ConvHexListToVal(hexData)
		nextAddr = currAddr + 1
		return [val]

	elif isTwoRegRegMode(tokens):
		ra = int(tokens[1][1:])
		rb = int(tokens[3][1:])
		reg = (ra << 4) | rb
		op_code = INST_DIC[tokens[0]][0]
		hexData = [op_code, reg, 0, 0]
		val = ConvHexListToVal(hexData)
		nextAddr = currAddr + 1
		return [val]

	elif isOneRegOneValueMode(tokens):
		rb = int(tokens[1][1:])
		val2 = int('0x'+tokens[4], 0)
		op_code = INST_DIC[tokens[0]][0]
		hexData = [op_code, rb, 0, 0]
		val1 = ConvHexListToVal(hexData)
		nextAddr = currAddr + 2
		return [val1, val2]

	else:
		print(tokens, 'NO SUCH COMMAND!')
		sys.exit()










# 어셈블리 파일을 읽어들여서 명령 코드로 해독한 후 바이너리 파일을 만듭니다
lines = readFile(sys.argv[1])
toklines = preProcess(lines)
# print(toklines)

for i, toks in enumerate(toklines):
	resData = parseCommand(toks)
	if resData != None:
		idx = currAddr
		for _, val in enumerate(resData):
			print(format(idx, '06x'), format(val, '08x'))
			binData[idx] = val
			idx += 1
	currAddr = nextAddr


# 아직 라벨 주소 치환이 되지 않은 부분이 있어 그것을 처리
for key, value in notyetlabels.items():
	# 주소는 2번째 입력 바이트이기에 라벨 주소에서 1을 더함
	binData[value + 1] = labels[key]
	print(key, format(binData[value + 1], '08x'))

# 처리된 바이너리 데이터를 파일에 저장
fw = open('program.bin', 'wb')
binData.tofile(fw)
fw.close()
