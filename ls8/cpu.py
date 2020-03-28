"""CPU functionality."""

import sys
HLT = 0b00000001
MUL = 0b10100010
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
         # 8 general-purpose registers
        self.reg = [0] * 8

        # hold 256 bytes of memory
        self.ram = [0] * 256
        self.pc = 0
        

    def ram_read(self, address):
        # memory address register
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self,file_name):
        """Load a program into memory."""

        # address = 0
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        try:
            address = 0
            file_name = sys.argv[1]
            with open(file_name) as file:
                for line in file:
                    comment_split = line.split("#")[0]
                    num = comment_split.strip()
                
                    if num == "":
                        continue

                    val = int(num, 2)
                    self.ram[address] = val
                    address += 1
                
        except FileNotFoundError:
            print("file not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
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
        running = True
        while running:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                running = False


            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc +=2
            elif ir == MUL:
                self.alu(ir, operand_a, operand_b)
                self.pc += 3
            else:
                print(f"I did not understand that command")
                sys.exit(1)

print(sys.argv[1])