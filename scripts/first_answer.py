# coding: utf-8
# Your code here!
import random
import time
import numpy as np
import logging

class Ad_map:
    #数字の意味　0→左に操作 1→上に操作 2→右に操作 3→下に操作
    MAX_MAP=10**4
    def __init__(self,N,pos):
        self.pos=pos
        self.N=N
        self.expand=[]
        self.R=[]
        self.happies=[]

        self.results_gen=[0,0]
        
        for i,(x,y,r) in enumerate(pos):
            self.expand.append(np.zeros(4,dtype=int))
            self.R.append(r)
            self.happies.append(self._calc_happy(i))

    def sampling(self):
        #randomに選ぶ
        target=random.randint(0,self.N-1)

        dire=random.randint(0,3)
        high,low=self.MAX_MAP,0

        while high-low>1:
            middle=(high+low)//2
            diff_pos=self._expand_diff_pos(dire,target,middle)

            if self._run_check(target,diff_pos):
                low=middle
            else:
                high=middle

        logging.error(f"{high},{low}")
        diff_pos=self._expand_diff_pos(dire,target,low)
        self.expand[target]+=diff_pos
        self.happies[target]=self._calc_happy(target)
        
        if low!=0:
            return 0
        else:             
            return 1
    
    def _slide_diff_pos(self,order,target):
        
        x,y,_=self.pos[target]
        
        if order==0:# to left
            trans_amount=max(-self.expand[target][2],-x)
            diff_pos=np.array([trans_amount,0,-trans_amount,0],dtype=int)
        elif order==1:
            trans_amount=max(self.expand[target][3],y)
            diff_pos=np.array([0,trans_amount,0,-trans_amount],dtype=int)
        elif order==2:
            trans_amount=min(-self.expand[target][0],self.MAX_MAP-x)
            diff_pos=np.array([-trans_amount,0,trans_amount,0],dtype=int)
        elif order==3:
            trans_amount=min(-self.expand[target][1],self.MAX_MAP-y)
            diff_pos=np.array([0,-trans_amount,0,trans_amount],dtype=int)
        elif order==4:
            raise Exception("invalid direction.")
        
        return diff_pos

    def _expand_diff_pos(self,order,target,size=10):
        
        x,y,_=self.pos[target]
               
        if order==0:
            diff_pos=np.array([-size,0,0,0],dtype=int)
        elif order==1:
            diff_pos=np.array([0,-size,0,0],dtype=int)
        elif order==2:
            diff_pos=np.array([0,0,size,0],dtype=int)
        elif order==3:
            diff_pos=np.array([0,0,0,size],dtype=int)
        else:
            raise Exception("invalid direction.")
            
        return diff_pos

    def _make_vertexs(self,target,diff_pos=np.zeros(4,dtype=int)):
        x,y,_=self.pos[target]
        vertexs=np.array([x,y,x+1,y+1],dtype=int)+self.expand[target]+diff_pos

        return vertexs

    def _calc_happy(self,target,diff_pos=np.zeros(4,dtype=int)):
        x1,y1,x2,y2=self._make_vertexs(target,diff_pos)
        r=self.R[target]
        s=(x2-x1)*(y2-y1)

        return 1-(1-min(s,r)/max(s,r))**2

    def _run_check(self,target,diff_pos):
        return self._check_over(target,diff_pos) and self._check_overrange(target,diff_pos)

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
        logging.error(vertexs)
        for vertex in vertexs:
            if vertex<0 or vertex>self.MAX_MAP:
                return False
        
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
    logging.error(f"{test.results_gen}")

    test.answer()


if __name__=="__main__":
    solve()