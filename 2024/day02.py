# read input
with open("input02", "r") as f:
    inp = f.read().splitlines()

#make integer
ipt = [[int(n) for n in row.split()] for row in inp]


# how many safe
safe = 0 #counter for how many safe rows we have

#for row in ipt:
#    l = len(row)
#    # calculate all differences
#    difs = [(row[i]-row[i-1]) for i in range(1, l)]
#    # if not strictly increasing or decreasing, discard
#    if not (all(n<0 for n in difs) or all(n>0 for n in difs)):
#        next
#    # if any <1 or >3, discard #important: elif, not if!
#    elif (any(abs(n)<1 for n in difs) or any(abs(n)>3 for n in difs)):
#        next
#    else:
#        safe += 1

# part2: make a function and run on omitting one number each (brute force I know)
def is_safe(row):
    l = len(row)
    # calculate all differences
    difs = [(row[i]-row[i-1]) for i in range(1, l)]
    # if not strictly increasing or decreasing, discard
    if not (all(n<0 for n in difs) or all(n>0 for n in difs)):
        return False
    # if any <1 or >3, discard #important: elif, not if!
    elif (any(abs(n)<1 for n in difs) or any(abs(n)>3 for n in difs)):
        return False
    else:
        return True

for row in ipt:
    if is_safe(row):
        safe += 1
    else:
        # check omitting allone by one
        for i in range(len(row)):
            if is_safe(row[:i]+row[i+1:]):
                safe += 1
                break #not next: we need to break inner loop to exit into outer loop
        

if __name__=="__main__":
    print(safe)
