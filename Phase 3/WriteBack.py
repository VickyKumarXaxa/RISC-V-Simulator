

        ########## Assumptions ###########
# rd : global variable ; detected in decode stage
# RY is output of stage 4.
            # control : initalised with 0 #####
# is a global variable : it should come from decode stage.
#  it will detect the type of instructon
# control will become 1 for r-type, i-type, u-type, uj-type
register = [] # global list 
for i in range(32):
    register.append(0)

def WriteBack(RY):
    if (Control==1):
        register[rd] = RY