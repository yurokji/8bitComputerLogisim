    INPORT $0 #키보드
    OUTPORT $0 #TTY 출력
    MOVI SP, $FFFF
    MOVI R4, $0101
    MOV R4, R6
    MOVI R2, @QUESTION_1
    CALL @OUT_TEXT
    MOVI R10, $EFFF
    CALL @WAIT_INPUT
    MOVI R2, @ANSWER_1
    CALL @OUT_TEXT 
    MOVI R2, $F000
    CALL @OUT_TEXT
BEST_LOOP:
    MOVI R2, @QUESTION_2
    CALL @OUT_TEXT
    MOVI R11, $0
    MOVI R10, $EFFF
    CALL @WAIT_INPUT
    MOVI R0, $F000
    CLF
    LD R0, R1
    CPI R1, $31
    BRE @RONALDO_BEST
    CPI R1, $32
    BRE @MESSI_BEST
    BRNE @WRONG_PLAYER
WRONG_PLAYER:
    CLF
    MOVI R1, $A
    CALL @OUTCHAR
    MOVI R2, @ANSWER_2_3
    CALL @OUT_TEXT   
    JPI @BEST_LOOP
RONALDO_BEST:
    CLF
    MOVI R1, $A
    CALL @OUTCHAR
    MOVI R2, @ANSWER_2_1
    CALL @OUT_TEXT
    JPI @BEST_LOOP   
MESSI_BEST:
    CLF
    MOVI R1, $A
    CALL @OUTCHAR
    MOVI R2, @ANSWER_2_2
    CALL @OUT_TEXT   
MESSI_LOOP:
    MOVI R2, @QUESTION_3
    CALL @OUT_TEXT
    MOVI R11, $0
    MOVI R10, $EFFF
    CALL @WAIT_INPUT
    MOVI R0, $F000
    CLF
    LD R0, R1
    CPI R1, $79
    BRE @DRAW_MESSI
    CPI R1, $6E
    BRE @TERMINATE
    BRNE @WRONG
WRONG:
    CLF
    MOVI R1, $A
    CALL @OUTCHAR
    MOVI R2, @ANSWER_3_3
    CALL @OUT_TEXT   
    JPI @MESSI_LOOP
TERMINATE:
    CLF
    MOVI R1, $A
    CALL @OUTCHAR
    MOVI R2, @ANSWER_3_2
    CALL @OUT_TEXT
    HLT
DRAW_MESSI:
    CLF
    MOVI R1, $A
    CALL @OUTCHAR
    MOVI R2, @ANSWER_3_1
    CALL @OUT_TEXT
    CALL @DRAW
    HLT
DRAW:
    # VGA 그래픽 디스플레이 포트
    OUTPORT $1
    MOVI R2, $1000
    MOV R2, R0
    MOVI R4, $0000
    MOV R4, R6
    MOVI R10, $0
    MOVI R11, $0
    CALL @DRAW_LOOP
DRAW_LOOP:
    CLF
    LD R0, R1
    OUTA R6
    OUTD R1
    ADI R0, $1
    ADI R6, $1
    ADI R10, $1  
    CLF
    CPI R10, $80
    BRE @NEXT_PIXEL_ROW
    JPI @DRAW_LOOP
NEXT_PIXEL_ROW:
    MOVI R10, $0
    ADI R6, $100
    ANI R6, $FF00
    ADI R11, $1
    CLF
    CPI R11, $80
    BRNE @DRAW_LOOP
    HLT

OUT_TEXT:
    MOV R2, R0
OUTEXT__LOOP:
    CLF
    LD R0, R1
    CPI R1, $3
    BRE @END_OF_CHAR
    CALL @OUTCHAR
    ADI R0, $1
    ADI R6, $1
    JPI @OUTEXT__LOOP
END_OF_CHAR:
    RET
OUTCHAR:
    OUTD R1
    RET

WAIT_INPUT:
    CPI R11, $A
    BRNE @WAIT_INPUT
    RET



    .ORG $E000
QUESTION_1:
    .TEXT @@\n\n Tell me your name: \0

    .ORG $E100
ANSWER_1:
    .TEXT @@\n Ok. Your name is \0

    .ORG $E200
QUESTION_2:
    .TEXT @@\n Who is the best foolballer? \n1) Christiano Ronaldo\n2) Lionel Messi\n(1/2):\0

    .ORG $E300
ANSWER_2_1:
    .TEXT @@\n Are you kidding?\n CR7 is not the best.\n Guess again! \n \0

    .ORG $E400
ANSWER_2_2:
    .TEXT @@\n You are right.\n Messi is G.O.A.T! \0

    .ORG $E500
ANSWER_2_3:
    .TEXT @@\n I cannot understand.\n Try again.\n \0


    .ORG $E600
QUESTION_3:
    .TEXT @@\n Do you want to see\n the messi's photo?(y/n): \0

    .ORG $E700
ANSWER_3_1:
    .TEXT @@\n Now Photo is being drawn...\n \0

    .ORG $E800
ANSWER_3_2:
    .TEXT @@\n Bye Bye...\n \0

    .ORG $E900
ANSWER_3_3:
    .TEXT @@\n I cannot understand. Try again.\n \0



#인터럽트 서비스 루틴
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