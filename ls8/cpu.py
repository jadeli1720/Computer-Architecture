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
        
        # depending on value of opcode --> HLT, LDI, and PRN
        # perform the actions needed for the instruction per LS-8 spec --> look at what the opcode does
        # if-elif cascade? --> look at Brady's example
        # print(LDI)

        while running:
            # Execute instructions

            # needs to read the memory address that's stored in register PC, and store that result in IR
            ir = self.ram_read(self.pc)
            # ir = self.ram[self.pc]
        
            # Use ram_read to read the bytes at PC + 1 and PC + 2 from ram variables operand_a -->Position of R0 (register and index 0) is 0b00000000 == to  operand_b 

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print("while statement", ir)

            if ir == LDI: # --> Set the value of a register to an integer.
                # print("LDI statement", LDI )
                print('operands a',operand_a, self.ram[operand_a]  ) # 0
                print('operands b',operand_b, self.ram[operand_b] )
                # print('operands',operand_a  )
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == PRN: # --> /Print to the console the decimal integer value that is stored in the given register(ir).
                reg = self.ram_read(self.pc + 1)
                self.reg[reg]
                print(f"You are printing {self.reg[reg]}") 
                self.pc += 2

            elif ir == HLT: # Halt --> similar to what we did with Brady?
                # halt operations
                print("Halt conditional")
                running = False
                self.pc +=1

            else:
                print(f"Error, unknown command {ir}")
                sys.exit(1)

        # After running code for any particular instruction, the PC needs to be updated to point to the next instruction for the next iteration of the loop in run(). The number of bytes an instruction uses can be determined from the two high bits (bits 6-7) of the instruction opcode. See the LS-8 spec for details.

    
