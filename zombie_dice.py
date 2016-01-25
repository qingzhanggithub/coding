import copy
import numpy as np
import math
from scipy.misc import comb
class zombie_dice:
    def __init__(self):
        self.green = [3./6, 2./6, 1./6] # brain, foot, shot
        self.yellow = [1./3, 1./3, 1./3]
        self.red = [1./6, 2./6, 3./6]
        self.probas = [self.green, self.yellow, self.red]
        self.n_green = 6
        self.n_yellow = 4
        self.n_red = 3
        self.n = 13
    
    def predict(self, cur) :
        
        # cur is current outcome, including the color and surface, it is such a table        
        #       brain foot shot
        # green
        # red
        # yellow
       
        BRAIN = 0
        FOOT = 1
        SHOT = 2

        GREEN = 0
        YELLOW = 1
        RED = 2

        n_brain = np.sum(cur[:, BRAIN])
        n_foot = np.sum(cur[:, FOOT])
        n_shot = np.sum(cur[:, SHOT])
        
        n_green = np.sum(cur[GREEN :])
        n_yellow = np.sum(cur[YELLOW :])
        n_red = np.sum(cur[RED :])
        
        foot = cur[:, FOOT]

        n_need = 3 - n_foot
        print 'need to draw ', n_need
        paths =[]
        self.draw(n_need, 0, [0,0,0], paths)
        
        suf_paths = []
        print 'drawing suf..\n\n'
        self.draw(3, 0, [0,0,0], suf_paths)
        
        proba_states = np.zeros(len(suf_paths))

        ns = [self.n_green - n_green, self.n_yellow - n_yellow, self.n_red - n_red]

        for p in paths:
            
            # compute the proba of getting this particular draw
            p_draw = self.prob_draw(ns, p)
            print '### p_draw : ', p_draw
            new_p = np.asarray(p) + foot
            print '### path\t', new_p
            t = [] # creating dice table
            for i in range(3) :
                for k in range(new_p[i]):
                    t.append(self.probas[i])
                    print 'appending to t ', self.probas[i]
            tt = np.asarray(t) # column is surface
            proba_states  += p_draw * self.suf_proba(suf_paths, tt) # proba of all possible surfaces configs within this draw
            
        for i in range(len(suf_paths)):
            print suf_paths[i], '\t:\t', proba_states[i]

    def suf_proba(self, suf_paths, dice_table) :
        proba_all =[]
        for p in suf_paths :
            p_state = 0
            assns = []
            print 'getting assignment for suf_path ', p
            self.assign_dice_to_surface([-1,-1,-1], 0, copy.copy(p), assns)
            for assign in assns :
                proba = 1
                for i in range(3):
                    proba *= dice_table[i,assign[i]]
                p_state += proba
            print 'proba of surface assignment ',p, '\t:\t', p_state
            proba_all.append(p_state)
            
        #print 'proba_all of suf_paths\n', proba_all, '\n--\n'
        return np.asarray(proba_all)


    def assign_dice_to_surface(self, dices, i, surf_path_tmp, assns) :
        if i == 3  and sum(surf_path_tmp) == 0 :
            print 'an assignment ', dices
            assns.append(copy.copy(dices))
            return
        if i==3 or sum(surf_path_tmp)==0:
            return
        
        for j in range(3): # assgn the dice to one of the surface
            if surf_path_tmp[j] != 0:
                dices[i] = j
                surf_path_tmp[j] -= 1
                self.assign_dice_to_surface(dices, i+1, surf_path_tmp, assns)
                surf_path_tmp[j] += 1
                    
               
    def simple_draw(self , k, i, path, paths) :
        if i >2 and k >0:
            return
        if k==0 :
            paths.append(copy.copy(path))
            return

        self.simple_draw(k, i+1, path, paths)
        path[i]=1
        self.simple_draw(k-1, i+1, path, paths)
        path[i]=0
        
        

    def prob_draw(self, ns, path):
        print 'ns:', ns, '\tpath\t',path
        total = sum(ns)
        enu = 0
        for i in range(3):
            if ns[i]  < path[i] :
                return 0
            enu += comb(ns[i], path[i])
            
        deno = comb(total, sum(path))
        print 'enu\t', enu, '\tdeno\t', deno
        return enu * 1.0 / deno

            
    def draw(self, n, i, path, paths):
        if i > 2 and n != 0: # run output of boundary, but not yet distributed all the quota
            return
        if n == 0:
            print path
            paths.append(copy.copy(path))
            return
        for k in xrange(n+1) :
            path[i]= k
            self.draw(n-k, i+1, path, paths)
            path[i]=0

zd = zombie_dice()
cur = np.asarray([[1,0,0],[1,0,0], [1,0,0]])
zd.predict(cur)        
