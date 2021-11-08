    MOVI SP, $FFFF
    MOVI R2, @MY_STR
    MOVI R4, $0101
    MOV R4, R6
    MOVI R5, $D
    MOVI R7, $9
    MOVI R9, $3
    CALL @OUT_TEXT
    HLT

OUT_TEXT:
    MOV R2, R0
OUTEXT__LOOP:
    CLF
    LD R0, R1
    CMP R1, R5
    BRE @NEXTLINE
    CMP R1, R7
    BRE @NEXTTAB
    CALL @OUTCHAR
    ADI R0, $1
    ADI R6, $1
    CLF
    CMP R1, R9
    BRNE @OUTEXT__LOOP
    RET
NEXTLINE:
    ADI R6, $100
    ANI R6, $FF00
    ADI R0, $1
    JPI @OUTEXT__LOOP
NEXTTAB:
    ADI R6, $4
    ADI R0, $1
    JPI @OUTEXT__LOOP

OUTCHAR:                                                                                                                          
    OUTA R6
    OUTD R1
    RET

    .ORG $2000
MY_STR:
    .TEXT @@\t\tThe Waste Land\n\t\t\t  BY T. S. ELIOT\n\n\n  April is the cruellest month,\n   breeding\n\n  Lilacs out of the dead land,\n   mixing\n\n   Memory and desire,\n   stirring\n\n  Dull roots with spring rain.\0