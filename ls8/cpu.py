"""CPU functionality."""

import sys

# instructions

hlt = 0b00000001 
ldi = 0b10000010 
prn = 0b01000111
mul = 0b10100010
push = 0b01000101
pop = 0b01000110
call = 0b01010000
ret = 0b00010001
add = 0b10100000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.stack_pointer = 256


    def ram_read(self, location):
        return self.ram[location]

    def ram_write(self, value, location):
        self.ram[location] = value
        
    def stack_push(self, value):
        self.stack_pointer -= 1
        self.ram[self.stack_pointer] = value
        
    def stack_pop(self):
        popped_value = self.ram[self.stack_pointer]
        self.stack_pointer += 1
        return popped_value

    def call(self, location):
        # grab pc + 1 and save it in stack
        self.stack_push(self.pc + 2)
        # change pc to location
        self.pc = location

    def ret(self):
        #grab old pc from stack and set pc to it
        self.pc = self.stack_pop()

    def add(self, value1, value2):
        print('add', value1 + value2)
    
    def load(self, name):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        program = []

        with open(name) as f:
            for line in f:
                #remove comment
                split = line.split('#')
                command = split[0].strip()
                try:
                    program.append(int(command, 2))
                except ValueError:
                    pass

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
        running = True

        while running:
            IR = self.ram[self.pc]
            # print(IR)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == hlt:
                sys.exit()

            elif IR == ldi:
                self.ram[operand_a] = operand_b
                self.pc += 3

            elif IR == prn:
                print('print',self.ram[operand_a])
                self.pc += 2

            elif IR == mul:
                print(self.ram[operand_a] * self.ram[operand_b])
                self.pc += 3

            elif IR == push:
                value = self.ram[operand_a]
                self.stack_push(value)
                self.pc += 2

            elif IR == pop:
                print('pop', self.stack_pop())
                self.pc += 2
            
            elif IR == call:
                self.call(self.ram[operand_a])

            elif IR == ret:
                self.ret()

            elif IR == add:
                self.add(self.ram[operand_a], self.ram[operand_b])
                self.pc += 3

            else:
                print('bad IR', IR)
                sys.exit()