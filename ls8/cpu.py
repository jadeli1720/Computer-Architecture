"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # TODO: Add list of properties to hold 256 bytes of memory -->ram
        self.ram = [0] * 255
        # Add 8 general-purpose registers
        self.reg = [0] * 8
        # Add properties for any internal registers you need --> pc (program counter)
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # TODO: implement this function
        # needs to read the memory address that's stored in the register pc and store that result in ir: Instruction Register
            # local variable can be used
        # some instructions require 2 bytes of data after the pc
        # Read STEP 3 in read me for more details
        # If-elifs, PC+1 and PC+2, operand_a and operand_b, ram_read(), PC needs to be updated
        pass


    # MAR contains the address that IS being read or written to
    # MDR contains the data that WAS read or the data to write

    def ram_read(self, mar): #access' the RAM inside the CPU object
        """
        Accepts the address to read and returns the value stored in memory.
        """
        self.ram[mar]
    

    def ram_write(self, mdr, mar):# access; the RAM inside the CPU object
        """
        Accepts a value to write, and the address to write to
        """
        self.ram[mar] = mdr
