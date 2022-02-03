#!/usr/bin/env python
import sys
from code_writer import CodeWriter, CommandType

ARITHMETIC_COMMAND = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]


class Parser:
    def __init__(self):
        #self.file_path = sys.argv[1]
        self.read_path = "FunctionCalls/SimpleFunction/SimpleFunction.vm"
        file_path_components = self.read_path.split("/")
        output_file_name = file_path_components[-1]
        file_path_components[-1] = output_file_name
        output_file_paths = "/".join(file_path_components)
        self.code_writer = CodeWriter(output_file_paths)

    def parse(self):
        with open(self.read_path) as f:
            for line in f.readlines():
                line = self.pre_process(line)
                if self.is_deletable(line):
                    continue
                command_type = self.command_type(line)
                converted = self.code_writer.convert(line, command_type)
                self.code_writer.write(converted)

    @staticmethod
    def command_type(line) -> CommandType:
        command = line.split()[0]
        if command in ARITHMETIC_COMMAND:
            return CommandType.C_ARITHMETIC
        elif command == "push":
            return CommandType.C_PUSH
        elif command == "pop":
            return CommandType.C_POP
        elif command == "label":
            return CommandType.C_LABEL
        elif command == "goto":
            return CommandType.C_GOTO
        elif command == "if-goto":
            return CommandType.C_IF
        elif command == "call":
            return CommandType.C_CALL
        elif command == "function":
            return CommandType.C_FUNCTION
        elif command == "return":
            return CommandType.C_RETURN

    @staticmethod
    def pre_process(line) -> str:
        i = line.find("//")
        if i > -1:
            line = line[0:i]
        line = line.strip()
        return line

    @staticmethod
    def is_deletable(line) -> bool:
        return line == "" or line[0:2] == "//"


if __name__ == '__main__':
    p = Parser()
    p.parse()
