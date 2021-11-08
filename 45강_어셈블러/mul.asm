# 곱셈을 수행하는 어셈블리어입니다
# 0x00 번지부터 시작되지만
	JMP $F9
# 프로그램 시작 주소는 100번지
	.org $100
	DATA r1, $1f
	DATA r0, $2d
	DATA r3, $01000000
	DATA r5, $1
	DATA r6, $80
	XOR  r2, r2
	NOP
	NOP
	NOP
	NOP
# 다음 비트로 이동하기
NEXTBIT:
	CLF
	SHR r0
	BRC GOADD
	JMP SKIPADD
# 더해주기
GOADD:
115	CLF
	ADD r1, r2
# 덧셈 건너뛰기
SKIPADD:
	CLF
	ST r6, r2
	ADD r5, r6
	CLF
	SHL r1
	SHL r3
	BRC BYEBYE
	JMP NEXTBIT
# 프로그램 종료하기
BYEBYE:
	HLT
