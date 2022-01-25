#!/usr/bin/env python
import sys
from enum import Enum, auto
from converter import Converter
from symbol_table import SymbolTable


class CommandType(Enum):
    A_COMMAND = auto()
    C_COMMAND = auto()
    L_COMMAND = auto()


class Parser:
    def __init__(self):
        self.file_path = sys.argv[0]
        file_name = self.file_path.split("/")[-1]
        open(file_name, "w")
        self.symbol_table = SymbolTable()

    def resolve_symbol(self):
        with open(self.file_path) as f:
            line_num = 0
            for line in f.readlines():
                line = self.pre_process(line)
                if self.is_deletable(line):
                    continue
                command_type = self.command_type(line)
                if command_type == CommandType.L_COMMAND:
                    symbol = self.symbol(line, command_type)
                    self.symbol_table.add_entry(symbol, line_num)
                    continue
                line_num += 1


    def parse(self):
        with open(self.file_path) as f:
            for line in f.readlines():
                line = self.pre_process(line)
                if self.is_deletable(line, True):
                    continue
                command_type = self.command_type(line)
                parsed = ""
                if command_type == CommandType.A_COMMAND:
                    parsed += "0"
                    symbol = self.symbol(line, command_type)
                    if symbol.isdigit():
                        parsed += Converter.number(symbol)
                    else:
                        self.symbol_table.resolve(symbol)
                        address = self.symbol_table.get_access(symbol)
                        parsed += Converter.number(address)
                else:
                    parsed += "111"
                    comp_mnemonic = self.comp(line)
                    parsed += Converter.comp(comp_mnemonic)
                    dest_mnemonic = self.dest(line)
                    parsed += Converter.dest(dest_mnemonic)
                    jump_mnemonic = self.jump(line)
                    parsed += Converter.jump(jump_mnemonic)
                self.add(parsed + "\n")

    def add(self, line):
        with open(self.file_name, "a") as f:
            f.write(line)

    @staticmethod
    def command_type(line) -> CommandType:
        if line[0] == "(":
            return CommandType.L_COMMAND
        elif line[0] == "@":
            return CommandType.A_COMMAND
        else:
            return CommandType.C_COMMAND

    @staticmethod
    def symbol(line, command_type) -> str:
        if command_type == CommandType.A_COMMAND:
            return line[1:]
        else:
            return line[1:-1]

    @staticmethod
    def dest(line) -> str:
        position = line.find("=")
        if position == -1:
            return "null"
        return line[0:position]

    @staticmethod
    def comp(line) -> str:
        position = line.find(";")
        if position > 0:
            return line[0:position]
        position = line.find("=")
        if position == -1:
            return "null"
        return line[position+1:]

    @staticmethod
    def jump(line) -> str:
        position = line.find(";")
        if position == -1:
            return "null"
        return line[position+1:]

    @staticmethod
    def pre_process(line) -> str:
        i = line.find("//")
        if i > -1:
            line = line[0:i]
        line = line.strip()
        return line

    @staticmethod
    def is_deletable(line, is_parse=False) -> bool:
        if is_parse:
            return line == "" or line[0] == "(" or  line[0:2] == "//"
        return line == "" or line[0:2] == "//"


if __name__ == '__main__':
    p = Parser()
    p.resolve_symbol()
    p.parse()

