// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(LOOP)
    @LOOP
    @SCREEN
    D=A
    @position
    M=D
    @KBD
    D=M
    @UNFILLING
    D;JEQ
(FILLING)
    @position
    D=M
    @8192
    D=D-A
    @SCREEN
    D=D-A
    @DONE
    D;JEQ
    @position
    A=M
    M=-1
    @position
    M=M+1
    @FILLING
    0;JMP
(UNFILLING)
    @position
    D=M
    @8192
    D=D-A
    @SCREEN
    D=D-A
    @DONE
    D;JEQ
    @position
    A=M
    M=0
    @position
    M=M+1
    @UNFILLING
    0;JMP    
(DONE)
    @LOOP
    0;JMP
