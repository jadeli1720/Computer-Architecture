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
        self.sp = 7 # Stack Pointer
        self.flag = [0] * 8

    

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
                    
                    # Convert binary string to integer
                    value = int(num, 2) # Base 10, but ls-8 is base 2

                    #  save/write appropriate data to RAM
                    self.ram_write(address, value)

                    # Increment address'
                    address += 1

        except FileNotFoundError:
            print(f"{sys.arg[0]}: {filename} not found")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        self.flag[5] # L
        self.flag[6] # G
        self.flag[7] # E

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL": # --> multiply two register values
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP": # Flags = FL they are internal registers
            # FL     0b00000LGE 
            #               |||
            # CMP == 0b10100111 The last three 1's are the flags
            # print(f'A:{self.reg[reg_a]}, B:{self.reg[reg_b]}')
            # if regA < regB: set Less [L] flag to 1 (True)
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag[5] = 1
                self.flag[6] = 0
                self.flag[7] = 0
                #           LGE
                # self.flag = 0b00000100
                # print(f'L Flag : {self.flag[5]}')
            # if regA = regB: set Equal [E] flag to 1 (True)
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.flag[5] = 0
                self.flag[6] = 0
                self.flag[7] = 1
                #           LGE
                # print(f'E Flag : {self.flag[7]}')
                
            # if regA > regB: set Greater [G] flag to 1 (True)
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag[5] = 0
                self.flag[6] = 1
                self.flag[7] = 0
                #           LGE
                # print(f'G Flag : {self.flag[6]}')
            else:
                pass
                # self.flag = 0b00000000
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
        # opcodes
        LDI  = 0b10000010
        PRN  = 0b01000111
        HLT  = 0b00000001 
        MUL  = 0b10100010
        ADD  = 0b10100000
        POP  = 0b01000110
        PUSH = 0b01000101
        CALL = 0b01010000
        RET  = 0b00010001
        CMP  = 0b10100111  
        JMP  = 0b01010100
        JEQ  = 0b01010101
        JNE  = 0b01010110

        running = True
        
        while running:
            # Execute instructions
            # needs to read the memory address that's stored in register PC, and store that result in IR
            ir = self.ram_read(self.pc)
            SP = self.sp
            # FL = self.flag
            
            # Use ram_read to read the bytes at PC + 1 and PC + 2 from ram variables operand_a and operand_b which are equivalent to each other 
            # operand_a: 00000000 --> R0 (register at index 0 in memory) is equal to
            # operand_b: 00001000 --> The value 8

            operand_a = self.ram_read(self.pc + 1) # --> First argument
            operand_b = self.ram_read(self.pc + 2) # --> Second argument
            # print("while statement", ir)
            if ir == LDI: # --> Set the value of a register to an integer.
                # print("LDI statement", LDI )
                                                                          #        R0    LDI
                # print('operands a',operand_a, self.ram[operand_a]  )    # prints 0 and 130
                #                                                         #      value    R0
                # print('operands b',operand_b, self.ram[operand_b] )     # prints 8  and 0
                # print('operands',operand_a  )
                self.reg[operand_a] = operand_b
                # print(f'{self.reg[operand_a]} is in R{operand_a}' )
                # print(f'Binary: {bin(operand_b)}')
                self.pc += 3

            elif ir == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3

            elif ir == MUL: # --> Multiply the values  using ALU
                #use ALU --> what arguments does it take
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif ir == PRN: # --> /Print to the console the decimal integer value that is stored in the given register.
                reg = operand_a
                self.reg[reg]
                print(f"{self.reg[reg]} in now in the register")
                print("-------------------- \n") 
                self.pc += 2

            elif ir == HLT: # Halt --> halt operations
                print("Operations have been halted")
                running = False
                self.pc +=1

            elif ir == PUSH:
                # reg == 1st argument
                reg = operand_a
                # grab the values we are putting on the reg
                val = self.reg[reg]
                # Decrement the SP.
                self.reg[SP] -= 1
                # Copy/write value in given register to address pointed to by SP. ram_write(mar, mdr)
                self.ram_write(self.reg[SP], val)
                # Increment PC by 2
                self.pc += 2

            elif ir == POP:
                # reg == 1st argument
                reg = operand_a
                # grab values we are putting on the reg
                val = self.ram[self.reg[SP]]
                self.reg[reg] = val
                # # Increment SP.
                self.reg[SP] += 1
                # # Increment PC by 2
                self.pc += 2

            elif ir == CALL:
                # address of instruction directly after CALL is pushed onto stack
                # print(f"PC {self.pc} ")
                val = self.pc + 2
                # PC is set to the address stored in the given register
                reg_index = operand_a # --> self.ram_read(self.pc + 1)

                subroutine_address = self.reg[reg_index]
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = val
                
                # print(f"CALLING to address {subroutine_address % 256}") 
                # jump to that location in RAM --> execute the 1st instruction in the subroutine
                self.pc = subroutine_address

            elif ir == RET:
                # return for the subroutine
                return_address = self.reg[SP]
                # Pop the value from the top of the stack and store it in the PC
                self.pc = self.ram_read(return_address)
                # Increment the SP by 1
                self.reg[SP] += 1
                # print(f"RETURNING to address {return_address % 256}")
            
            elif ir == CMP:
                # Compare 2 values (2 arguments: regA & regB)
                # Saw is cheatsheet this can be done in ALU. Use ALU here
                self.alu("CMP", operand_a, operand_b)
                # print("Register in CMP", self.reg)
                # print(f"Flag: {self.flag}")
                # print("--------------------")
                
                self.pc += 3

            elif ir == JMP:
                # Jump to the address stored in the given register
                print(f'JMP Register Address {operand_a}')
                # set the PC to the address stored in the given register
                self.pc = self.reg[operand_a]
                print(f'JMP PC address {self.pc}')
                # print("--------------------")
            elif ir == JEQ:
                
                # print(f"CMP: {CMP}, E: {E}")
                # if [E] flag is true:
                if self.flag[7] == 1:
                    self.pc = self.reg[operand_a]
                    # print(f'JEQ PC address {self.pc}')
                else:
                    print("Else statement")
                    self.pc += 2

            elif ir == JNE:
                # if [E] flag is clear
                if self.flag[7] != 1:
                    # jump to the address stored in the given register
                    self.pc = self.reg[operand_a]
                    # print(f'JNE PC address {self.pc}')
                else:
                    self.pc +=2
        
            else:
                print(f"Error, unknown command {ir}")
                sys.exit(1)

    
