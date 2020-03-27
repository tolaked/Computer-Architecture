"""CPU functionality."""

import sys
HLT = 0b00000001
MUL = 0b10100010
LDI = 0b10000010
PRN = 0b01000111
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000


sp = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
         # 8 general-purpose registers
        self.reg = [0] * 8

        # hold 256 bytes of memory
        self.ram = [0] * 256
        self.pc = 0
        self.pc = 0
        self.halted = False

        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        self.branchtable[CALL] = self.handle_call
        self.branchtable[RET] = self.handle_ret
        self.branchtable[ADD] = self.handle_add
        self.reg[7] = 0xF4


    def handle_hlt(self):
        self.halted = True
    
    def handle_ldi(self):
        reg_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[reg_num] = value
        self.pc += 3
    
    def handle_prn(self):
        reg_num = self.ram_read(self.pc + 1)
        print(self.reg[reg_num])
        self.pc += 2
    
    def handle_mul(self):
        num_1 = self.ram_read(self.pc + 1)
        num_2 = self.ram_read(self.pc + 2)
        self.alu(MUL, num_1, num_2)
        self.pc +=3
    
    def handle_push(self):
        # setup
        reg_num = self.ram_read(self.pc + 1)
        value = self.reg[reg_num]

        # push
        self.reg[sp] -= 1
        self.ram[self.reg[sp]] = value
        self.pc += 2
    
    def handle_pop(self):
        # setup
        reg_num = self.ram_read(self.pc + 1)
        value = self.ram[self.reg[sp]]

        # pop
        self.reg[reg_num] = value
        self.reg[sp] += 1
        self.pc += 2
    def handle_call(self):
        reg_num = self.ram_read(self.pc + 1)
        self.reg[sp] -= 1
        self.ram[self.reg[sp]] = self.pc + 2
        self.pc = self.reg[reg_num]
    
    def handle_ret(self):
        self.pc = self.ram[self.reg[sp]]
        self.reg[sp] += 1

    def handle_add(self):
        num_1 = self.ram_read(self.pc + 1)
        num_2 = self.ram_read(self.pc + 2)
        self.alu(ADD, num_1, num_2)
        self.pc += 3

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
        while  not self.halted:
            ir = self.ram[self.pc]

            if ir == 0 or None:
                print("I did not understand this command")
                sys.exit(1)

            self.branchtable[ir]()

print(sys.argv[1])