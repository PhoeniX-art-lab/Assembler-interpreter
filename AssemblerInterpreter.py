class AssemblerInterpreter:

    def __init__(self, text):
        self.text = text.split('\n')
        self.offset = 0
        self.end_point = False
        self.stack = []
        self.out = ''
        self.registers = {}
        self.labels = {}
        # Not equal, equal, grower or equal, grower, lower or equal, lower flags
        self.flags = {'ne': False, 'e': False, 'ge': False, 'g': False, 'le': False, 'l': False}
        while self.text.count(''):
            self.text.remove('')

    def mov(self, *args):  # args[0] - register, args[1] - register or value
        x = args[0].replace(',', '')
        self.registers[x] = self.registers[args[1]] if args[1] in self.registers else int(args[1])
        self.offset += 1

    def semicolon(self, *args):
        self.offset += 1

    def inc(self, *args):  # args[0] - register
        self.registers[args[0]] += 1
        self.offset += 1

    def dec(self, *args):  # args[0] - register
        self.registers[args[0]] -= 1
        self.offset += 1

    def add(self, *args):  # args[0] - register, args[1] - register or value
        x = args[0].replace(',', '')
        self.registers[x] += self.registers[args[1]] if args[1] in self.registers else int(args[1])
        self.offset += 1

    def sub(self, *args):
        x = args[0].replace(',', '')
        self.registers[x] -= self.registers[args[1]] if args[1] in self.registers else int(args[1])
        self.offset += 1

    def mul(self, *args):
        x = args[0].replace(',', '')
        self.registers[x] *= self.registers[args[1]] if args[1] in self.registers else int(args[1])
        self.offset += 1

    def div(self, *args):
        x = args[0].replace(',', '')
        self.registers[x] //= self.registers[args[1]] if args[1] in self.registers else int(args[1])
        self.offset += 1

    def jmp(self, *args):  # args[0] - label
        self.offset = self.labels[args[0]] + 1

    def cmp(self, *args):
        x = args[0].replace(',', '')
        x = self.registers[x] if x in self.registers else int(x)
        y = self.registers[args[1]] if args[1] in self.registers else int(args[1])
        for key in self.flags:
            self.flags[key] = False
        if x <= y:
            self.flags['le'] = True
        if x < y:
            self.flags['l'] = True
        if x != y:
            self.flags['ne'] = True
        if x == y:
            self.flags['e'] = True
        if x >= y:
            self.flags['ge'] = True
        if x > y:
            self.flags['g'] = True

        self.offset += 1

    def flag_jmp(*args):
        flag = args[0]  # flag

        def wrapper(self, *args):  # args[0] - label
            nonlocal flag
            if self.flags[flag]:
                self.offset = self.labels[args[0]] + 1
                for key in self.flags:
                    self.flags[key] = False
            else:
                self.offset += 1
            return None

        return wrapper

    def call(self, *args):
        self.stack.append(self.offset + 1)  # write current position to stack
        self.offset = self.labels[args[0]] + 1

    def ret(self, *args):
        self.offset = self.stack.pop(-1)

    def msg(self, *args):
        message = ' '.join(args)
        for i in range(len(message)):       # deleting comments
            if message[i] == ';':
                message = message[:i]
                break
        i = 0
        i_start = 0
        message_list = []
        while i < len(message):
            if message[i] == "'":
                i_start = i
                i += 1
                while message[i] != "'":
                    i += 1
                message_list.append(message[i_start:i + 1])
            else:
                i_start = i
                while i < len(message) and message[i] != "'":
                    i += 1
                message_list.append(message[i_start:i])
                i -= 1
            i += 1
        for i in range(len(message_list)):
            if "'" not in message_list[i]:
                message_list[i] = message_list[i].replace(',', '').replace(' ', '')
        for element in message_list:
            if element.replace(' ', '') in self.registers:
                self.out += str(self.registers[element.replace(' ', '')])
            else:
                self.out += element.replace("'", "")

        self.offset += 1

    def end(self, *args):
        self.end_point = True

    commands = {';': semicolon, 'mov': mov, 'inc': inc, 'dec': dec, 'add': add, 'sub': sub, 'mul': mul, 'div': div,
                'jmp': jmp, 'cmp': cmp, 'jne': flag_jmp('ne'), 'je': flag_jmp('e'), 'jge': flag_jmp('ge'),
                'jg': flag_jmp('g'), 'jle': flag_jmp('le'), 'jl': flag_jmp('l'), 'call': call, 'ret': ret, 'msg': msg,
                'end': end}

    def main_loop(self):
        for i in range(len(self.text)):
            arguments = self.text[i].split()
            if arguments[0] not in self.commands and arguments[0][-1] == ':':
                self.labels[arguments[0].replace(':', '')] = i
        while self.offset < len(self.text):
            arguments = self.text[self.offset].split()
            try:
                self.commands[arguments[0]](self, *arguments[1:])
            except KeyError:
                self.offset += 1
            if self.end_point:
                return self.out

        return -1
