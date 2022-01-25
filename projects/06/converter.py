class Converter:
    @staticmethod
    def number(num_str):
        binary = ""
        num = int(num_str)
        for i in range(14, -1, -1):
            divider = 2 ** i
            binary += str(num // divider)
            num = num % divider
        return binary

    @staticmethod
    def dest(mnemonic) -> str:
        if mnemonic == "null" or mnemonic == "0":
            return "000"
        elif mnemonic == "M":
            return "001"
        elif mnemonic == "D":
            return "010"
        elif mnemonic == "MD":
            return "011"
        elif mnemonic == "A":
            return "100"
        elif mnemonic == "AM":
            return "101"
        elif mnemonic == "AD":
            return "110"
        elif mnemonic == "AMD":
            return "111"

    @staticmethod
    def comp(mnemonic) -> str:
        if mnemonic == "null":
            return "0000000"
        elif mnemonic == "0":
            return "0101010"
        elif mnemonic == "1":
            return "0111111"
        elif mnemonic == "-1":
            return "0111010"
        elif mnemonic == "D":
            return "0001100"
        elif mnemonic == "A":
            return "0110000"
        elif mnemonic == "!D":
            return "0001101"
        elif mnemonic == "!A":
            return "0110001"
        elif mnemonic == "-D":
            return "0001111"
        elif mnemonic == "-A":
            return "0110011"
        elif mnemonic == "D+1":
            return "0011111"
        elif mnemonic == "A+1":
            return "0110111"
        elif mnemonic == "D-1":
            return "0001110"
        elif mnemonic == "A-1":
            return "0110010"
        elif mnemonic == "D+A":
            return "0000010"
        elif mnemonic == "D-A":
            return "0010011"
        elif mnemonic == "A-D":
            return "0000111"
        elif mnemonic == "D&A":
            return "0000000"
        elif mnemonic == "D|A":
            return "0010101"
        elif mnemonic == "M":
            return "1110000"
        elif mnemonic == "!M":
            return "1110001"
        elif mnemonic == "-M":
            return "1110011"
        elif mnemonic == "M+1":
            return "1110111"
        elif mnemonic == "M-1":
            return "1110010"
        elif mnemonic == "D+M":
            return "1000010"
        elif mnemonic == "D-M":
            return "1010011"
        elif mnemonic == "M-D":
            return "1000111"
        elif mnemonic == "D&M":
            return "1000000"
        elif mnemonic == "D|M":
            return "1010101"

    @staticmethod
    def jump(mnemonic) -> str:
        if mnemonic == "null":
            return "000"
        elif mnemonic == "JGT":
            return "001"
        elif mnemonic == "JEQ":
            return "010"
        elif mnemonic == "JGE":
            return "011"
        elif mnemonic == "JLT":
            return "100"
        elif mnemonic == "JNE":
            return "101"
        elif mnemonic == "JLE":
            return "110"
        elif mnemonic == "JMP":
            return "111"
