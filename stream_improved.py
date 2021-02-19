from collections import deque

def lfsr(p,s):
    n=0
    sl = len(s) - 1
    for i in p:
        n += s[sl-i]
    c=s.popleft()
    s.append(n%2)
    return c,s

def encrypt(file, fileout, key):
    arr=[]
    for i in key:
        arr.append([i >> p & 1 for p in range(8)][::-1])

    k=sum(arr[1:], start=arr[0])
    W=deque(k[0:16])
    U=deque(k[16:33])
    V=deque(k[33:64])
    p=[1,2,4,15]
    q=[2,16]
    r=[2,30]

    with open(file, 'rb') as file, open(fileout, 'wb') as fileout:
        while byte := file.read(1):
            bitchar = map(int, f'{byte[0]:08b}')
            outstring=[]
            for char in bitchar:
                b1, W= lfsr(p,W)
                b2, U= lfsr(q,U)
                b3, V= lfsr(r,V)
                num=char ^ (b3*b1+(1-b3)*b2)%2
                outstring.append(str(num))
            fileout.write(bytes([int(''.join(outstring), 2)]))


if __name__ == '__main__':
    import sys
    from time import perf_counter

    iters = 10

    start = perf_counter()

    for i in range(iters):
        file, fileout, kfile = sys.argv[1:4]

        with open(kfile, 'rb') as kfile:
            key=kfile.read()

        encrypt(file, fileout, key)

    print(f'Encrypted in {(perf_counter() - start) / iters}s')
