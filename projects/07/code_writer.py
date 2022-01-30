from enum import Enum, auto


class CommandType(Enum):
    C_ARITHMETIC = auto()
    C_PUSH = auto()
    C_POP = auto()
    C_LABEL = auto()
    C_GOTO = auto()
    C_IF = auto()
    C_FUNCTION = auto()
    C_RETURN = auto()
    C_CALL = auto()


class CodeWriter:
    def __init__(self, file_name):
        self.output_file = file_name.split(".")[0] + ".asm"
        self.label = 0
        open(self.output_file, "w")

    def write(self, line):
        with open(self.output_file, "a") as f:
            f.write(line)

    def convert(self, line, command_type) -> str:
        args = line.split()
        converted = ""
        if command_type == CommandType.C_ARITHMETIC:
            converted = self.convert_arithmetic(args)
        elif command_type == CommandType.C_PUSH or command_type == CommandType.C_POP:
            converted = self.convert_push_pop(args)
        return converted

    def convert_arithmetic(self, args) -> str:
        command = args[0]
        asm = ""
        if command in ["add", "sub", "eq", "lt", "gt", "and", "or"]:
            asm = self.binary_arithmetic_operator(asm)
            if command == "add":
                asm += "M=D+M\n"
            elif command == "sub":
                asm += "M=M-D\n"
            elif command == "and":
                asm += "M=M&D\n"
            elif command == "or":
                asm += "M=M|D\n"
            elif command in ["eq", "lt", "gt"]:
                asm = self.comparison_operator(asm, command)
            asm = self.decrease_stack_pointer(asm)
        elif command in ["neg", "not"]:
            asm = self.unary_arithmetic_operator(asm)
            if command == "neg":
                asm += "M=-M\n"
            elif command == "not":
                asm += "M=!M\n"
        return asm

    @staticmethod
    def decrease_stack_pointer(asm) -> str:
        asm += "@SP\n"
        asm += "M=M-1\n"
        return asm

    @staticmethod
    def unary_arithmetic_operator(asm) -> str:
        asm += "@SP\n"
        asm += "A=M-1\n"
        return asm

    @staticmethod
    def binary_arithmetic_operator(asm) -> str:
        asm += "@SP\n"
        asm += "A=M-1\n"
        asm += "D=M\n"
        asm += "A=A-1\n"
        return asm

    def comparison_operator(self, asm, command) -> str:
        asm += "D=M-D\n"
        asm += "@TRUE_{}\n".format(self.label)
        if command == "eq":
            asm += "D;JEQ\n"
        elif command == "lt":
            asm += "D;JLT\n"
        elif command == "gt":
            asm += "D;JGT\n"
        asm += "@SP\n"
        asm += "A=M-1\n"
        asm += "A=A-1\n"
        asm += "M=0\n"
        asm += "@END_{}\n".format(self.label)
        asm += "0;JMP\n"
        asm += "(TRUE_{})\n".format(self.label)
        asm += "@SP\n"
        asm += "A=M-1\n"
        asm += "A=A-1\n"
        asm += "M=-1\n"
        asm += "(END_{})\n".format(self.label)
        self.label += 1
        return asm

    @staticmethod
    def convert_push_pop(args) -> str:
        asm = ""
        (command, memory_segment, number) = (args[0], args[1], args[2])
        if command == "push":
            asm = CodeWriter.push(asm, memory_segment, number)
        if command == "pop":
            asm = CodeWriter.pop(asm, memory_segment, number)
        return asm

    @staticmethod
    def push(asm, memory_segment, number) -> str:
        base_point = CodeWriter.get_base_point(memory_segment)
        if memory_segment == "constant":
            asm += "@{}\n".format(number)
            asm += "D=A\n"
        else:
            asm += "@{}\n".format(base_point)
            asm += "A=M\n"
            for i in range(0, int(number)):
                asm += "A=A+1\n"
            asm += "D=M\n"
        asm += "@SP\n"
        asm += "A=M\n"
        asm += "M=D\n"
        asm += "@SP\n"
        asm += "M=M+1\n"
        return asm

    @staticmethod
    def pop(asm, memory_segment, number) -> str:
        base_point = CodeWriter.get_base_point(memory_segment)
        asm += "@SP\n"
        asm += "A=M-1\n"
        asm += "D=M\n"
        asm += "@{}\n".format(base_point)
        asm += "A=M\n"
        for i in range(0, int(number)):
            asm += "A=A+1\n"
        asm += "M=D\n"
        asm = CodeWriter.decrease_stack_pointer(asm)
        return asm

    @staticmethod
    def get_base_point(memory_segment) -> str:
        if memory_segment == "constant":
            return "SP"
        elif memory_segment == "local":
            return "LCL"
        elif memory_segment == "argument":
            return "ARG"
        elif memory_segment == "this":
            return "THIS"
        elif memory_segment == "that":
            return "THAT"
        elif memory_segment == "temp":
            return "R5"
