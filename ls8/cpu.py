"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # TODO: Add list of properties to hold 256 bytes of memory -->ram
        self.ram = [0] * 256
        # Add 8 general-purpose registers
        self.reg = [0] * 8
        # Add properties for any internal registers you need --> pc (program counter)
        self.pc = 0
        # Any other internal registers needed?


    def load(self, filename):
        """Load a program into memory."""
        print("Loading", filename)

        try:
            address = 0

            # open file: save appropriate data to RAM
            with open(filename) as f:
                # read the contents line by line:
                for line in f:
                    # ignore the comments
                    comment_split = line.split('#')
                    # print("Comment split", comment_split)
                    # use .strip() to get rid of any spaces
                    num = comment_split[0].strip()
                    # print("num", int(num, 2))
                    # ignore blank lines
                    if num == "":
                        continue
                    
                    value = int(num, 2) # Base 10, but ls-8 is base 2
                    # # save/write appropriate data to RAM
                    print('saving value + address', self.ram_write(address, value))
                    self.ram_write(address, value)
                    address += 1

        except FileNotFoundError:
            print(f"{sys.arg[0]}: {filename} not found")

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

    # MAR contains the address that IS being read or written to
    # MDR contains the data that WAS read or the data to write

    def ram_read(self, mar): #access' the RAM inside the CPU object
        """
        Accepts the address to read and returns the value stored in memory.
        """
        return self.ram[mar]

    

    def ram_write(self, mar, mdr):# access; the RAM inside the CPU object
        """
        Accepts a value to write, and the address to write to
        """
        self.ram[mar] = mdr
        

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001 

        running = True
        
        while running:
            # Execute instructions

            # needs to read the memory address that's stored in register PC, and store that result in IR
            ir = self.ram_read(self.pc)
        
            # Use ram_read to read the bytes at PC + 1 and PC + 2 from ram variables operand_a and operand_b which are equivalent to each other 
            # operand_a: 00000000 --> R0 (register at index 0 in memory) is equal to
            # operand_b: 00001000 --> The value 8


            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print("while statement", ir)

            if ir == LDI: # --> Set the value of a register to an integer.
                # print("LDI statement", LDI )
                                                                        #        R0    LDI
                # print('operands a',operand_a, self.ram[operand_a]  )    # prints 0 and 130
                #                                                         #      value    R0
                # print('operands b',operand_b, self.ram[operand_b] )     # prints 8  and 0
                # print('operands',operand_a  )
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == PRN: # --> /Print to the console the decimal integer value that is stored in the given register(ir).
                reg = self.ram_read(self.pc + 1)
                self.reg[reg]
                print(f"{self.reg[reg]} in now in the register") 
                self.pc += 2

            elif ir == HLT: # Halt --> similar to what we did with Brady?
                # halt operations
                print("Operations have been halted")
                running = False
                self.pc +=1

            else:
                print(f"Error, unknown command {ir}")
                sys.exit(1)

    
