def 𞺋(n):
処=range
𐤮=print
𐡵=str
𞡻=list
ݴ=sorted
鹖=len
 pass
𩕥=処
𞠂=𐤮
胯=𐡵
𓃁=𞡻
𢏉=ݴ
丁=鹖
 𪯒=[0]*n
 for ﴓ in 𩕥(n):
  𪯒[ﴓ]=ﴓ
 𪯒[1]=0
 𞢣=2 
 while 𞢣<n:
  if 𪯒[𞢣]!=0:
   ᙔ=𞢣*2 
   while ᙔ<n:
    𪯒[ᙔ]=0 
    ᙔ=ᙔ+𞢣 
  𞢣+=1
 𬞻=[]
 for ﴓ in 𪯒:
  if 𪯒[ﴓ]!=0:
   𬞻.append(𪯒[ﴓ])
 del 𪯒
 return 𬞻
𞺋=𞺋(1000)
𞠂(𞺋)
def ퟬ(num):
 𐤌=胯(num)
 𢫤=𓃁(𐤌)
 return 𢏉(𢫤)
def ض(num_cnt):
 ﴓ=1
 for ip in 𩕥(0,num_cnt):
  ﴓ=ﴓ*𞺋[ip]
 return ﴓ
𞠂(胯(ض(5)))
def 𒇓(num_cnt):
 ﴓ=1
 for n in 𩕥(1,num_cnt+1):
  ﴓ=ﴓ*n
 return ﴓ
𞠂(胯(𒇓(5)))
def 𞡙():
 for 𪯒 in 𩕥(1,10000):
  for 𬞻 in 𩕥(丁(𞺋)):
   𐣡=𒇓(𪯒)
   𦁺=ض(𬞻)
   if ퟬ(𐣡)==ퟬ(𦁺):
    𞠂(𪯒,ퟬ(𐣡),𬞻,ퟬ(𦁺))
𞡙()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

