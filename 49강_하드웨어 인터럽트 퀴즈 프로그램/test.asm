    INPORT $0
    OUTPORT $0
    MOVI SP, $FFFF
    MOVI R4, $0101
    MOV R4, R6
    MOVI R2, @QUESTION_1
    CALL @OUT_TEXT
    MOVI R10, $EFFF
    CALL @WAIT_INPUT
    


OUT_TEXT:
    MOV R2, R0
OUTEXT__LOOP:
    CLF
    LD R0, R1
    CPI R1, $3
    BRE @END_OF_CHAR
    OUTD R1
    ADI R0, $1
    ADI R6, $1
    JPI @OUTEXT__LOOP
END_OF_CHAR:
    RET


WAIT_INPUT:
    CPI R11, $A
    BRNE @WAIT_INPUT
    HLT

    .ORG $E000
QUESTION_1:
    .TEXT @@\n\n Tell me your name: \0


.ORG $FFE0
KBD_INT_SVC:
    ADI R10, $1
    CLF
    IND R11 
    CPI R11, $A
    BRE @END_CHAR
NO_END_CHAR:
    OUTD R11
    ST R10, R11
    RETI
END_CHAR:
    MOVI R12, $3
    ST R10, R12
    RETI

