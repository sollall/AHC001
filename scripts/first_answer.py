# coding: utf-8
# Your code here!
import random
import time
import numpy as np
import logging

class Ad_map:
    #数字の意味　0→左に操作 1→上に操作 2→右に操作 3→下に操作
    SIZE=1
    def __init__(self,N,pos):
        self.pos=pos
        self.N=N
        self.expand=[]
        self.R=[]
        self.happies=[]
        
        for i,(x,y,r) in enumerate(pos):
            self.expand.append(np.zeros(4,dtype=int))
            self.R.append(r)
            self.happies.append(self._calc_happy(i))

    def sampling(self):
        #randomに選ぶ
        target=random.randint(0,self.N-1)

        dire=random.randint(0,3)
        if dire==0:
            diff_pos=np.array([-self.SIZE,0,0,0],dtype=int)
        elif dire==1:
            diff_pos=np.array([0,-self.SIZE,0,0],dtype=int)
        elif dire==2:
            diff_pos=np.array([0,0,self.SIZE,0],dtype=int)
        elif dire==3:
            diff_pos=np.array([0,0,0,self.SIZE],dtype=int)
        else:
            raise Exception("invalid direction.")
        
        if self._check_over(target,diff_pos) and self._check_overrange(target,diff_pos):
            if self._calc_happy(target,diff_pos)>self.happies[target]:
                self.expand[target]+=diff_pos
                self.happies[target]=self._calc_happy(target)

                return 0
            else:
                logging.error(f"幸福度があがらない {self._calc_happy(target,diff_pos),self._calc_happy(target),self.happies[target]}")
                return 1
        else:
            return 2
            

    def _make_vertexs(self,target,diff_pos=np.zeros(4,dtype=int)):
        x,y,_=self.pos[target]
        vertexs=np.array([x,y,x+1,y+1],dtype=int)+self.expand[target]+diff_pos

        return vertexs

    def _calc_happy(self,target,diff_pos=np.zeros(4,dtype=int)):
        x1,y1,x2,y2=self._make_vertexs(target,diff_pos)
        r=self.R[target]
        s=(x2-x1)*(y2-y1)

        return 1-(1-min(s,r)/max(s,r))**2

    def _check_over(self,target:int,diff_pos):
        x,y,_=self.pos[target]

        ax1,ay1,ax2,ay2=self._make_vertexs(target,diff_pos)
        rev=True

        for n in range(self.N):
            if n==target:#自分自身はスキップ
                continue
            else:
                bx1,by1,bx2,by2=self._make_vertexs(n)
                mid_a=(ax1+ax2)/2,(ay1+ay2)/2
                mid_b=(bx1+bx2)/2,(by1+by2)/2
                
                width_a=abs(ax2-ax1)
                height_a=abs(ay2-ay1)
                
                width_b=abs(bx2-bx1)
                height_b=abs(by2-by1)
        
                if abs(mid_a[0]-mid_b[0])<(width_a+width_b)/2 and abs(mid_a[1]-mid_b[1])<(height_a+height_b)/2:
                    rev=False
                    logging.error(f"{target}:{ax1,ay1,ax2,ay2},{n}:{bx1,by1,bx2,by2}")

        return rev

    def _check_overrange(self,target,diff_pos):
        vertexs=self._make_vertexs(target,diff_pos)
        if -1 in vertexs or 10**4+1 in vertexs:
            return False
        else:
            return True
    
    def answer(self):
        for n in range(self.N):
            print(*self._make_vertexs(n))
        return 

def solve():

    start=time.time()

    N=int(input())
    LIMIT=4.8

    pos=[]
    for _ in range(N):
        x,y,r=map(int,input().split())
        pos.append([x,y,r])
        
    test=Ad_map(N,pos)

    results=[0,0,0]
    while time.time()-start<LIMIT:
        result_code=test.sampling()
        results[result_code]+=1
    
    logging.error(f"{results}")

    test.answer()


if __name__=="__main__":
    solve()