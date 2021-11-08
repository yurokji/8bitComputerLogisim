BUS1_E =            0b10000000000000000000000000000000
MAR_S =             0b01000000000000000000000000000000
PC_S =              0b00100000000000000000000000000000
PC_E =              0b00010000000000000000000000000000
IR_S =              0b00001000000000000000000000000000
RAM_S =             0b00000100000000000000000000000000
RAM_E =             0b00000010000000000000000000000000
ACC_S =             0b00000001000000000000000000000000
ACC_E =             0b00000000100000000000000000000000
RA_S =              0b00000000010000000000000000000000
RA_E =              0b00000000001000000000000000000000
RB_S =              0b00000000000100000000000000000000
RB_E =              0b00000000000010000000000000000000
TMP_S =             0b00000000000001000000000000000000
CI_E =              0b00000000000000100000000000000000
IOCLK_S =           0b00000000000000010000000000000000
IOCLK_E =           0b00000000000000001000000000000000
FLAGS_S =           0b00000000000000000100000000000000
IN_OUT =            0b00000000000000000010000000000000
DATA_ADDR =         0b00000000000000000001000000000000
FC =                0b00000000000000000000100000000000
FA =                0b00000000000000000000010000000000
FE =                0b00000000000000000000001000000000
FZ =                0b00000000000000000000000100000000
HLT_E =             0b00000000000000000000000000000010
END_INST =          0b00000000000000000000000000000001


#Define the opcode and DECODE/EXECUTION steps of NON-ALU Instructions
LD =        [0x00, MAR_S | RA_E, RAM_E | RB_S, END_INST]
ST=         [0x01, MAR_S | RA_E, RAM_S | RB_E, END_INST]
DATA =      [0x02, BUS1_E | MAR_S | PC_E | ACC_S, RAM_E | RB_S, PC_S | ACC_E, END_INST] 
JMPR =      [0x03, PC_S | RB_E, END_INST]
JMP =       [0x04, MAR_S | PC_E, PC_S  | RAM_E, END_INST]
CLF =       [0x06, BUS1_E | FLAGS_S, END_INST]
IND =       [0x07, RB_S | IOCLK_E, END_INST]
INA =       [0x08, IND[0] | DATA_ADDR, DATA_ADDR, DATA_ADDR, END_INST]
OUTD =      [0x09, RB_E | IOCLK_S | IN_OUT, IN_OUT, IN_OUT, END_INST]
OUTA =      [0x0a, OUTD[0] | DATA_ADDR, OUTD[1] | DATA_ADDR, OUTD[2] | DATA_ADDR, END_INST]
#Define the opcode and DECODE/EXECUTION steps of ALU Instructions
ADD =       [0x80, RB_E | TMP_S, ACC_S | RA_E | CI_E | FLAGS_S, ACC_E | RB_S, END_INST]
SHR =       [0x81, RB_E | TMP_S, ACC_S | RA_E | CI_E | FLAGS_S, ACC_E | RB_S, END_INST]
SHL =       [0x82, RB_E | TMP_S, ACC_S | RA_E | CI_E | FLAGS_S, ACC_E | RB_S, END_INST]
NOT =       [0x83, RB_E | TMP_S, ACC_S | RA_E | CI_E | FLAGS_S, ACC_E | RB_S, END_INST] 
AND =       [0x84, RB_E | TMP_S, ACC_S | RA_E | CI_E | FLAGS_S, ACC_E | RB_S, END_INST]
OR =        [0x85, RB_E | TMP_S, ACC_S | RA_E | CI_E | FLAGS_S, ACC_E | RB_S, END_INST]
XOR =       [0x86, RB_E | TMP_S, ACC_S | RA_E | CI_E | FLAGS_S, ACC_E | RB_S, END_INST]
CMP =       [0x87, RB_E | TMP_S, ACC_S | RA_E | CI_E | FLAGS_S, ACC_E | RB_S, END_INST]
# newly added instructions
BRC =        [0x41, BUS1_E | MAR_S | PC_E | ACC_S | FC, PC_S | ACC_E | FC, PC_S | RAM_E | FC, END_INST]
BRA =        [0x42, BUS1_E | MAR_S | PC_E | ACC_S | FA, PC_S | ACC_E | FA, PC_S | RAM_E | FA, END_INST]
BRE =        [0x43, BUS1_E | MAR_S | PC_E | ACC_S | FE, PC_S | ACC_E | FE, PC_S | RAM_E | FE, END_INST]
BRZ =        [0x44, BUS1_E | MAR_S | PC_E | ACC_S | FZ, PC_S | ACC_E | FZ, PC_S | RAM_E | FZ, END_INST]
HLT =       [0x99, HLT_E]
NOP =       [0x90, END_INST]


#ALL Instructions
ALL_INSTRUCTIONS = [LD, ST, DATA, JMPR, JMP, CLF, IND, INA, OUTD, OUTA, 
                    ADD, SHR, SHL, NOT, AND, OR, XOR, CMP, BRC, BRA, BRE, BRZ, HLT, NOP]

import array as arr

wordSize = 32
bitsForOP = 8
bitsForSteps = 4
oneCycle = 2 ** bitsForSteps
szROM = 2 ** (bitsForOP + bitsForSteps)
print('micro code ROM size: ', szROM, 'words')
# 4K x 32bit ROM 
data = arr.array('L', [0] * szROM)
filename = 'microcode_matrix32.bin'
f = open(filename, 'wb')

# Steps for instruction fetch for ALL instructions (4096개, 4+8비트 = 헥스코드로 0x000~0xfff )
for i in range(0, 0x1000, oneCycle):
    if i == 0x990:
        data[i + 0 ] =      HLT_E

    else:
        data[i + 0 ] =      BUS1_E | MAR_S | PC_E | ACC_S
        data[i + 1] =       IR_S | RAM_E
        data[i + 2] =       PC_S | ACC_E

# Steps for decoding and execution for ALL instructions
for i, inst in enumerate(ALL_INSTRUCTIONS):
    idx = inst[0] << 4
    for j in range(len(inst) - 1):
        data[idx+ 3 + j] = inst[j + 1]


# # print all micro code for NON-ALU instructions
# for i in range(0, 0x0b0, oneCycle):
#     print('opcode: ', format(i >> 4, '02x'))
#     print('micro code: ')
#     print(format(data[i], '08x'), format(data[i+1], '08x'), format(data[i+2], '08x'),format(data[i+3], '08x'),format(data[i+4], '08x'),format(data[i+5], '08x'))

# # print all micro code for ALU instructions
# for i in range(0x800, 0x880, oneCycle):
#     print('opcode: ', format(i >> 4, '02x'))
#     print('micro code: ')
#     print(format(data[i], '08x'), format(data[i+1], '08x'), format(data[i+2], '08x'),format(data[i+3], '08x'),format(data[i+4], '08x'),format(data[i+5], '08x'))


data.tofile(f)
f.close()