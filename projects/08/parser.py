#!/usr/bin/env python
import sys
import glob
from code_writer import CodeWriter, CommandType

ARITHMETIC_COMMAND = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]


class Parser:
    def __init__(self):
        self.input = sys.argv[1]
        if self.input[-3:] == ".vm":
            self.read_files = [self.input]
            directory_path = self.input.split("/")[:-1]
            self.code_writer = CodeWriter("/".join(directory_path))
        else:
            self.read_files = glob.glob("{}/*.vm".format(self.input))
            self.code_writer = CodeWriter(self.input, True)

    def parse(self):
        for read_file in self.read_files:
            with open(read_file) as f:
                for line in f.readlines():
                    line = self.pre_process(line)
                    if self.is_deletable(line):
                        continue
                    command_type = self.command_type(line)
                    file_name = read_file.split("/")[-1].split(".")[0]
                    converted = self.code_writer.convert(line, command_type, file_name)
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
