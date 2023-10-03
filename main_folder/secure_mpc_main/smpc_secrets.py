import random
from typing import List

def Vandermonde(n):
    """
    NxN Vandermonde matrix
    """
    return [ [1 if  j == 0 else pow(i,j) for j in range(n)] for i in range(1,n+1)]

def P(n,t):
    """
    Projection matrix of size NxN having 1 for i rows and j cols where i == j. Otherwise 0.
    """ 
    return [[1 if i == j and i+1 <= t else 0 for i in range(n)] for j in range(n)]

class RandPoly:
    """
    Random and zero free coefficient polynomial
    """

    def __init__(self, n, name='', R = None, fzc=False, p = 1337):
        self.name = name
        self.n = n
        self.p = p
        self.fzc = fzc # free zero coefficient
        if R:
            self.R = R
            # assert(len(R) == n)
        else: 
            self.R = [0] * (n+1) 
            for t in range(self.n+1):
                if t == 0 and fzc is True:
                    self.R[t] = (t, 0)
                else:
                    r = random.randint(1,self.p)
                    self.R[t] = (t, r)

    def poly(self, x):
        s = 0
        for (n, r) in self.R:
            s += r * x ** n
        return s

    
    def poly_str(self):
        """
        outputs the underlying polynomial
        """
        s = ""
        first_zero = self.R[0][1] == 0
        if first_zero:
            for (i, r) in self.R:
                if i == 0:
                    continue
                elif i == 1:
                    s +=  f"{r}x" 
                else:
                    s += f"+{r}x^{i}"
        else:
            for (i, r) in self.R:
                if i == 0:
                    s += f"{r}"
                elif i == 1:
                    s +=  f"+{r}x" 
                else:
                    s += f"+{r}x^{i}"
        if self.name:
            return f"{self.name}(x)={s}"
        else:
            return s

    def __str__(self):
        return self.poly_str()

    def __repr__(self):
        return self.poly_str()

    def __add__(self, other):
        n = min(len(self.R), len(other.R))
        m = max(len(self.R), len(other.R))
        R = [0] * m
        for i in range(m):
            if i < n:
                R[i] = (i, self.R[i][1] + other.R[i][1])
            elif i < len(self.R):
                R[i]= (i, self.R[i][1])
            elif i < other.R:
                 R[i][1] = (i, other.R[i][1])
        
        return RandPoly(n=self.n, R=R)
        



# TODO:
# overloading __add__ and __mul__
#

class AdditiveSecretSharing:
    def __init__(self, n: int, p: int = 1337):
        """
        n: number of parties
        p: 
        """
        assert(n < p)
        assert(n > 1)
        self.n = n
        self.p = p
        self.shares = [(0,0) for _ in range(n)]


    def generate(self, s: int):
        """
        input:
            s: a secret
        output: 
            a generated list of shares of the input secret s
        """
        r = 0
        for i in range(self.n-1):
            self.shares[i] = (i+1, random.randint(1, self.p))
            r += self.shares[i][1] % self.p
        last_index = self.n-1
        self.shares[self.n-1] = (last_index+1, s - r)
        return self.shares

    def reconstruct(self, shares: List[int]):
        """
        input:
            shares: a list of shares
        output:
            the reconstructed secret from the list of shares
        """
        secret = 0
        assert (len(shares) >= self.n), f"{len(shares)} were provided! Provide at least {self.n} shares"
        for (_, share) in shares:
            secret += share
        return secret



class ShamirSecretSharing:
    def __init__(self, t: int, n: int, p: int = 1337):
        """
        t: threshold
        n: number of parties
        p: 
        """
        assert(t < p and n < p and t <= n)
        assert(n > 1)
        self.t = t
        self.n = n
        self.p = p
        self.shares = [(0,0) for _ in range(n+1)]
        self.R = [0]*(t)

    def generate(self, s: int):
        """
        input:
            s: a secret
        output: 
            a generated list of shares of the input secret s
        """
        f = [0]*(self.n+1)
        f[0] = s
        self.shares[0] = (0, s)
        self.R[0] = (0, s)

        for t in range(1, self.t):
            r = random.randint(1,self.p)
            self.R[t] = (t, r)

        for x in range(1, self.n+1):
            for t in range(self.t):
                if t == 0:
                    f[x] += f[0]
                else:
                    f[x] += self.R[t][1] * x ** t
            self.shares[x] = (x, f[x])
        return self.shares

    def reconstruct(self, shares: List[int]):
        """
        input:
            shares: a list of shares
        output: 
            the reconstructed secret from the list of shares
        """
        s = 0.0
        assert (len(shares) >= self.t), f"{len(shares)} were provided! Provide at least {self.t} shares"
        for (i, share) in shares:
            d = 1.0
            for (j, _) in shares:
                if i != j:
                    d *= (-j)/(i-j)
            s += share * d

        return int(s) 
        
    def _delta(self, i, x):
        """
        computes the delta function used in 
        Lagrange interpolation
        """
        d = 1.0
        for j in range(self.t):
            if i != j:
                d *= (x-j)/(i-j)
        return d

    def poly_str(self):
        """
        outputs the underlying polynomial
        """
        s = ""
        for (i, r) in self.R:
            if i == 0:
                s += str(r)
            elif i == 1:
                s += f"+{r}x"
            else:
                s += f"+{r}x^{i}"
        return s
            
    def poly(self, x):
        s = 0
        for (i, r) in self.R:
            if i == 0:
                s += r
            else:
                s += r*x**i
        return s
    
    def __str__(self):
        return self.poly_str()

    def __repr__(self):
        return self.poly_str()
