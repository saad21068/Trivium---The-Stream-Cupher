# function for xoring. I couldn't use the inbuilt function because I'm doing my processing in string form of 0 and 1 and want the output to be in the same format
def xor_(a):
    ans = False
    for i in a:
        ans = ans ^ (i == "1")
    if (ans):
        return "1"
    else:
        return "0"


# function for anding
def and_(a):
    for i in a:
        if i != "1":
            return "0"
    return "1"


class Trivium:

    # The initialization of trivium
    def __init__(self, key, iv):
        self.A = list(key + ("0" * 13))
        self.B = list(iv + ("0" * 4))
        self.C = list(("0" * 108) + ("1" * 3))

        # So while clocking we will have to shift the values to the right which would have taken 288 operations.
        # Instead of shifting the whole values to the right, I'm shifting the index of the last element to the left whose value I'm storing in posA, posB, posC
        # For that I've created getA getB getC functions to correctly get the i-th element from the register.
        self.posA = 92
        self.posB = 83
        self.posC = 110

    # Clocking here
    def clock(self):

        # Calculating Ta, Tb, Tc (or T1, T2, T3)
        Ta = xor_([self.getA(66), self.getA(93)])
        Tb = xor_([self.getB(69), self.getB(84)])
        Tc = xor_([self.getC(66), self.getC(111)])

        # Calculating Zi which I will return in the end
        Z = xor_([Ta, Tb, Tc])

        # Calculating feedback that goes into A (Fa / t3), B (Fb / t1), C (Fc / t2)
        Fa = xor_([Tc, self.getA(69), and_([self.getC(109), self.getC(110)])])
        Fb = xor_([Ta, self.getB(78), and_([self.getA(91), self.getA(92)])])
        Fc = xor_([Tb, self.getC(87), and_([self.getB(82), self.getB(83)])])

        # Setting the last flip flop as Fa, Fb, Fc (the feedbacks) which after cycling them (which I'm doing in the next step) will be the first element
        self.A[self.posA] = Fa
        self.B[self.posB] = Fb
        self.C[self.posC] = Fc

        # Cycling all the flip flops to the right by moving their origin to the left.
        self.posA = (self.posA + len(self.A) - 1) % len(self.A)
        self.posB = (self.posB + len(self.B) - 1) % len(self.B)
        self.posC = (self.posC + len(self.C) - 1) % len(self.C)

        return Z

    # as the clock function returns in binary, this function runs the clock functions to output n bytes
    def clockInHex(self, n):
        ans = ""
        for i in range(n):
            curr_ans = ""
            for j in range(8):
                curr_ans = self.clock() + curr_ans
                # ans = self.clock() + ans
            ans = ans + hex(int(curr_ans, 2))[2:].zfill(2)
        return "0x" + ans.upper()

    # Warming up phase i.e. clocking for 288 * 4 = 1152 times.
    def warmUp(self):
        for i in range(1152):
            self.clock()

    # custom methods to get i-th element in A, B, C considering posA, posB, posC are their last elements.
    def getA(self, i):
        return self.A[(i + self.posA) % len(self.A)]

    def getB(self, i):
        return self.B[(i + self.posB) % len(self.B)]

    def getC(self, i):
        return self.C[(i + self.posC) % len(self.C)]


# Taking the key as input and then removing the 0x in front of it, removeing any spaces in the hexadecimal number and converting the alphabets in lower cases
key = input("Enter Key bits in hexadecimal (starting with 0x) (input the whole number in 1 line please): ").replace(" ",
                                                                                                                    "").lower()
if (key[:2] == "0x"):
    key = key[2:]

# converting the key to binary. Reversing the order of bytes like 0x01 02 becomes 0x02 01 and then converting it to binary i.e. 0000 0010 0000 0001
# For example. 0x0102 will be converted to 1000 0000 0100 0000
bin_key = ""
for i in range(len(key) // 2):
    bin_key = bin(int(key[i * 2: (i + 1) * 2], 16))[2:].zfill(8) + bin_key

# doing the same as done to keys
iv = input("Enter IV bits in hexadecimal (starting with 0x) (input the whole number in 1 line please): ").replace(" ",
                                                                                                                  "").lower()
if (iv[:2] == "0x"):
    iv = iv[2:]

# converting to binary in the similar way as keys
bin_iv = ""
for i in range(len(iv) // 2):
    bin_iv = bin(int(iv[i * 2: (i + 1) * 2], 16))[2:].zfill(8) + bin_iv

# initializing the triving with the key bits and iv bits
trivium = Trivium(bin_key, bin_iv)

# warm up cycle of the trivium. clocking it 1152 times are throwing the key stream generated
trivium.warmUp()

# clocking it for 64 bytes and printing the output
print(trivium.clockInHex(64))