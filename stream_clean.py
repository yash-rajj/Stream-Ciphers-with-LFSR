from collections import deque

def lfsr(p,s):
    n=0
    for i in p:
        n=n+s[len(s)-i-1]
    c=s.popleft()
    s.append(n%2)
    return c,s

if __name__ == '__main__':
    import sys
    from time import perf_counter

    start = perf_counter()
    file, fileout, kfile = sys.argv[1:4]

    with open(kfile, 'rb') as kfile:
        key=kfile.read()

    arr=[]
    for i in key:
        arr.append([i >> p & 1 for p in range(8)][::-1])
    k=arr[0]+arr[1]+arr[2]+arr[3]+arr[4]+arr[5]+arr[6]+arr[7]
    W=deque(k[0:16])
    U=deque(k[16:33])
    V=deque(k[33:64])
    p=[1,2,4,15]
    q=[2,16]
    r=[2,30]

    with open(file, "rb") as file, open(fileout,"wb") as fileout:
        while byte := file.read(1):
            bitchar=[]
            bitchar = list(map(int, list("{0:08b}".format(byte[0]))))
            outstring=[]
            for y in range(len(bitchar)):
                b1, W= lfsr(p,W)
                b2, U= lfsr(q,U)
                b3, V= lfsr(r,V)
                ri=(b3*b1+(1-b3)*b2)%2
                num=bitchar[y]^ri
                outstring.append(str(num))
            fileout.write(bytes([int(''.join(outstring), 2)]))

    print(f'Encrypted in {perf_counter() - start}s')
