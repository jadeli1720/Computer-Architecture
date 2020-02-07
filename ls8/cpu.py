"""CPU functionality."""

import sys

# opcodes
LDI  = 0b10000010
LD   = 0b10000011
JMP  = 0b01010100
JLT  = 0b01011000
JLE  = 0b01011001
JGT  = 0b01010111
MUL  = 0b10100010
JGE  = 0b01011010
JEQ  = 0b01010101
IRET = 0b00010011
INT  = 0b01010010
INC  = 0b01100101
DEC  = 0b01100110
HLT  = 0b00000001 
PRN  = 0b01000111 
POP  = 0b01000110
PUSH = 0b01000101
RET  = 0b00010001
CALL = 0b01010000
ADD  = 0b10100000
SUB  = 0b10100001
DIV  = 0b10100011
CMP  = 0b10100111
JMP  = 0b01010100
JEQ  = 0b01010101
JNE  = 0b01010110
AND  = 0b10101000
OR   = 0b10101010
XOR  = 0b10101011
NOT  = 0b01101001
SHL  = 0b10101100
SHR  = 0b10101101
MOD  = 0b10100100
PRA  = 0b01001000

SP = 7
IM = 5
IS = 6


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        # Add 8 general-purpose registers
        self.reg = [0] * 8
        # Add properties for any internal registers you need --> pc (program counter)
        self.pc = 0
        self.reg[SP] = 0xF4  # Stack Pointer
        self.flag = [0] * 8
        
        self.opcodes =  {}
        self.opcodes[LDI] = self.handle_LDI
        self.opcodes[HLT] = self.handle_HLT
        self.opcodes[PRN] = self.handle_PRN
        self.opcodes[PUSH] = self.handle_PUSH
        self.opcodes[POP] = self.handle_POP
        self.opcodes[CALL] = self.handle_CALL
        self.opcodes[RET]  = self.handle_RET
        self.opcodes[JMP] = self.handle_JMP
        self.opcodes[JEQ] = self.handle_JEQ
        self.opcodes[JNE] = self.handle_JNE
        self.opcodes[PRA] = self.handle_PRA
        # ALU
        self.opcodes[ADD] = self.handle_ADD
        self.opcodes[SUB] = self.handle_SUB
        self.opcodes[MUL] = self.handle_MUL
        self.opcodes[DIV] = self.handle_DIV
        self.opcodes[MOD] = self.handle_MOD
        self.opcodes[INC] = self.handle_INC
        self.opcodes[DEC] = self.handle_DEC
        self.opcodes[CMP] = self.handle_CMP
        self.opcodes[AND] = self.handle_AND
        self.opcodes[NOT] = self.handle_NOT
        self.opcodes[OR] = self.handle_OR
        self.opcodes[XOR] = self.handle_XOR
        self.opcodes[SHL] = self.handle_SHL
        self.opcodes[SHR] = self.handle_SHR

        self.running = True
        self.message = ""

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
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL": # --> multiply two register values
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "INC":
            self.reg[reg_a] += 1
        elif op == "DEC":
            self.reg[reg_a] -= 1
        elif op == "CMP":
            # FL => 0bLGE 
            # self.FL &= 0 # clear all CMP flags
            # L (less) Flag
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag[5] = 1
                self.flag[6] = 0
                self.flag[7] = 0
                # print("L")
            # G (greater) Flag
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag[5] = 0
                self.flag[6] = 1
                self.flag[7] = 0
                # print("G")
            # E (equal)
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.flag[5] = 0
                self.flag[6] = 0
                self.flag[7] = 1
                # print("E")
        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_b]
        elif op == "SHL":
            self.reg[reg_a] <<= self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] >>= self.reg[reg_b] 
        elif op == "MOD":
            if self.reg[reg_b] == 0:
                print('Error cannot find remainder of zero')
                self.handle_HLT()
            remainder = self.reg[reg_a] // self.reg[reg_b] 
            self.reg[reg_a] = remainder
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
        """
        Run the CPU
        """

        while self.running:

            ir = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            num_operands = ir >> 6

            if ir in self.opcodes:
                if num_operands == 0:
                    self.opcodes[ir]()
                elif num_operands == 1:
                    self.opcodes[ir](operand_a)
                elif num_operands == 2:

                    self.opcodes[ir](operand_a, operand_b)
            else:
                print(f"Error, unknown command: {ir}")
                sys.exit(1)
        
        return self.message

    def handle_LDI(self, reg_a, reg_b):
        self.reg[reg_a] = reg_b
        # print(f"Reg A: {reg_a}, Reg B: {reg_b} ")
        self.pc += 3

    def handle_PRN(self, reg_a):
        self.reg[reg_a]
        self.pc += 2
        print(f"{self.reg[reg_a]} in now in the register")
        print("-------------------- \n") 
    
    def handle_HLT(self):
        print("Operations have been halted")
        self.running = False
        self.pc +=1

    def handle_PUSH(self, reg_a):
        val = self.reg[reg_a]

        self.reg[SP] -= 1
        self.ram_write(self.reg[SP], val)
        self.pc +=2

    def handle_POP(self, reg_a):
        val = self.ram[reg_a]
        self.reg[reg_a] = val
        self.reg[SP] += 1
        self.pc += 2
    
    def handle_CALL(self, reg_a):
        return_address = self.pc + 2
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = return_address
        self.pc = self.reg[reg_a]

    def handle_RET(self):
        return_address = self.reg[SP]
        self.pc = self.ram_read(return_address)
        self.reg[SP] += 1
    
    def handle_JMP(self, reg_a):
        self.pc = self.reg[reg_a]
    
    def handle_JEQ(self, reg_a):
        if self.flag[7] == 1:
            self.pc = self.reg[reg_a]
        else:
            self.pc += 2

    def handle_JNE(self, reg_a):
        # if [E] flag is clear
        if self.flag[7] != 1:
            # jump to the address stored in the given register
            self.pc = self.reg[reg_a]
        else:
            self.pc +=2

    # May need to adjust for mining
    def handle_PRA(self, reg_a):
        self.message += chr(self.reg[reg_a])
        self.pc += 2

    # ALU Methods
    def handle_ADD(self, reg_a, reg_b):
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    def handle_SUB(self, reg_a, reg_b):
        self.alu("SUB", reg_a, reg_b)
        self.pc += 3

    def handle_MUL(self, reg_a, reg_b):
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3

    def handle_DIV(self, reg_a, reg_b):
        self.alu("DIV", reg_a, reg_b)
        self.pc += 3

    def handle_INC(self, reg_a, reg_b):
        self.alu("INC", reg_a, reg_b)
        self.pc += 2

    def handle_DEC(self, reg_a, reg_b):
        self.alu("DEC", reg_a, reg_b)
        self.pc += 2

    def handle_CMP(self, reg_a, reg_b):
        self.alu("CMP", reg_a, reg_b)
        # print(self.reg)
        self.pc += 3
    
    def handle_AND(self, reg_a, reg_b):
        self.alu("AND", reg_a, reg_b)
        self.pc += 3

    def handle_OR(self, reg_a, reg_b):
        self.alu("OR", reg_a, reg_b)
        self.pc += 3

    def handle_XOR(self, reg_a, reg_b):
        self.alu("XOR", reg_a, reg_b)
        self.pc += 3

    def handle_NOT(self, reg_a, reg_b):
        self.alu("NOT", reg_a, reg_b)
        self.pc += 3

    def handle_SHL(self, reg_a, reg_b):
        self.alu("SHL", reg_a, reg_b)
        self.pc += 3

    def handle_SHR(self, reg_a, reg_b):
        self.alu("SHR", reg_a, reg_b)
        self.pc += 3

    def handle_MOD(self, reg_a, reg_b):
        self.alu("MOD", reg_a, reg_b)
        # print(self.reg)
        self.pc += 3

