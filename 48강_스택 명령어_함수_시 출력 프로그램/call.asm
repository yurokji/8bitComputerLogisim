	movi sp, $ffff
	movi r2, $200
	movi r3, $100
	movi r4, $400
	call SUBX
	st r2, r4
	adi r2, $1
	call SUBX
	st r2, r4
	NOP
	HLT
	.org $100
SUBX:
	clf
	sub r3, r4
	ret
