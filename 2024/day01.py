# read input
with open("input01", "r") as f:
    inp = f.read().splitlines()

# make 2 lists, sort them and take the difference (brute force)

l1 = [int(pair.split()[0]) for pair in inp]
l2 = [int(pair.split()[1]) for pair in inp]

l1.sort()
l2.sort()

if __name__=="__main__":
    print(sum([abs(b-a) for b,a in zip(l2,l1)]))
