import math

bo_bits = 0
index_bits = 0
tag_bits = 0
data_copy = 0
cachesize = 0
blocksize = 0
n = 0
SA = {}

Bo = 0                  # Block offset
ind = 0                 # index bits
tag = 0                 # tags

address=0x0FFFFFE8

DataNumHits = 0
DataNumMisses = 0

cachesize=int(input("Enter cache size(in bytes without unit):"))
blocksize=int(input("Enter cache block size(in bytes without unit):"))
n=int(input("Enter number of ways for Set Associative:"))
blocks=cachesize/blocksize
numsets=blocks/n

def Data_cache(address):        # Address will come from ALU
    global bo_bits, index_bits, tag_bits, data_copy, cachesize, blocksize, n, SA
    data_copy = address

    # instruction address sent from BTB or IAG
    # number of bits in instruction adddress

    add_bits=32                           # 32 for risc-v 32 bit ISA
    bo_bits=int(math.log2(blocksize))     # number of bits in block offset
    index_bits=int(math.log2(numsets))    # number of bits in index
    tag_bits=add_bits-bo_bits-index_bits  # number of bits in tag

    Size = int(blocks)//int(n)
    M = [[0, 0] for j in range(Size)]
    SA = {i:M for i in range(int(n))}


#  This part of code is from memory access stage, which is main memory
#  These are global dictionaries
#  I will compare the address with this dictionaries indexes
#  If they will match then the data of that will be stored in the cache
#  .
TextMemory = dict.fromkeys(range(0, 0x00000194, 1), 0)
DataMemory = dict.fromkeys(range(0x10000000, 0x10000194, 1), 0)

#  .

def indexAndTag(data_copy):
    global ind, tag
    if index_bits == 0:
        ind = 0
    elif index_bits == 1:
        ind = data_copy & 1
        tag = data_copy>>1
    elif index_bits == 2:
        ind = data_copy & 3
        tag = data_copy>>2
    elif index_bits == 3:
        ind = data_copy & 7
        tag = data_copy>>3
    elif index_bits == 4:
        ind = data_copy & 15
        tag = data_copy>>4
    elif index_bits == 5:
        ind = data_copy & 31
        tag = data_copy>>5
    elif index_bits == 6:
        ind = data_copy & 63
        tag = data_copy>>6
    elif index_bits == 7:
        ind = data_copy & 127
        tag = data_copy>>7
    elif index_bits == 8:
        ind = data_copy & 255
        tag = data_copy>>8
    elif index_bits == 9:
        ind = data_copy & 511
        tag = data_copy>>9
    elif index_bits == 10:
        ind = data_copy & 1023
        tag = data_copy>>10


def BlockOffSet(data_copy):
    global Bo
    if bo_bits == 0:
        Bo = 0
    elif bo_bits == 1:
        Bo = data_copy & 1
        data_copy = data_copy>>1
    elif bo_bits == 2:
        Bo = data_copy & 3
        data_copy = data_copy>>2
    elif bo_bits == 3:
        Bo = data_copy & 7
        data_copy = data_copy>>3
    elif bo_bits == 4:
        Bo = data_copy & 15
        data_copy = data_copy>>4
    elif bo_bits == 5:
        Bo = data_copy & 31
        data_copy = data_copy>>5
    elif bo_bits == 6:
        Bo = data_copy & 63
        data_copy = data_copy>>6
    elif bo_bits == 7:
        Bo = data_copy & 127
        data_copy = data_copy>>7
    elif bo_bits == 8:
        Bo = data_copy & 255
        data_copy = data_copy>>8
    elif bo_bits == 9:
        Bo = data_copy & 511
        data_copy = data_copy>>9
    elif bo_bits == 10:
        Bo = data_copy & 1023
        data_copy = data_copy>>10
    
    indexAndTag(data_copy)

def SetAssociative():
    global SA, ind, DataMemory, TextMemory, DataNumHits, DataNumMisses
    predict = ""
    for way in SA:
        for index in range(len(SA[way])):
            if index == ind:
                if SA[way][index][0] == tag:
                    predict = "hit"
                    DataNumHits += 1
                    return SA[way][index][1]
                else:
                    predict = "miss"
                    DataNumMisses += 1
                    SA[way][index][0] = tag
                    if 0x0FFFFFE8<=address:
                        SA[way][index][1] = DataMemory[address]
                    else:
                        SA[way][index][1] = TextMemory[address]

Data_cache(address)
BlockOffSet(data_copy)
Inst = SetAssociative()

print("\nData Cache: ")
print("Number of accesess:_____ ", DataNumMisses+DataNumHits)
print("Number of Hits:_____ ", DataNumHits)
print("Number of misses:_____ ", DataNumMisses)
print("\n")
