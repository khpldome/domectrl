def V(n):
p=range
r=print
W=str
I=list
e=sorted
S=len
 a=[0]*n
 for i in p(n):
  a[i]=i
 a[1]=0
 m=2 
 while m<n: 
  if a[m]!=0: 
   j=m*2 
   while j<n:
    a[j]=0 
    j=j+m 
  m+=1
 b=[]
 for i in a:
  if a[i]!=0:
   b.append(a[i])
 del a
 return b
V=V(1000)
r(V)
def J(num):
 O=W(num)
 f=I(O)
 return e(f)
def E(num_cnt):
 i=1
 for ip in p(0,num_cnt):
  i=i*V[ip]
 return i
r(W(E(5)))
def v(num_cnt):
 i=1
 for n in p(1,num_cnt+1):
  i=i*n
 return i
r(W(v(5)))
def w():
 for a in p(1,10000):
  for b in p(S(V)):
   x=v(a)
   P=E(b)
   if J(x)==J(P):
    r(a,J(x),b,J(P))
w()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

