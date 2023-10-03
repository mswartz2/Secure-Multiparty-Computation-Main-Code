import random
from typing import List


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
        self.shares = [0.0]*n

    def generate(self, s: int):
        """
        input:
            s: a secret
        output: 
            a generated list of shares of the input secret s
        """
        r = 0
        for i in range(self.n-1):
            self.shares[i] = random.randint(1, self.p)
            r += self.shares[i] % self.p
        self.shares[self.n-1] = s - r
        return self.shares

    def reconstruct(self, shares: List[int]):
        """
        input:
            shares: a list of shares
        output:
            the reconstructed secret from the list of shares
        """
        secret = 0
        for i in range(self.n):
            secret += self.shares[i]
        return secret



class ShamirSecretSharing:
    def __init__(self, t: int, n: int, p: int = 1337):
        """
        t: threshold
        n: number of parties
        p: 
        """
        assert(t < p and n < p and t < n)
        assert(n > 1)
        self.t = t
        self.n = n
        self.p = p
        self.shares = [0.0]*(n+1)

    def generate(self, s: int):
        """
        input:
            s: a secret
        output: 
            a generated list of shares of the input secret s
        """
        f = [0]*(self.n+1)
        f[0] = s
        self.shares[0] = s

        for x in range(1, self.n+1):
            for t in range(self.t):
                if t == 0:
                    f[x] += f[0]
                else:
                    r = random.randint(1,self.p)
                    f[x] += r * pow(x, t)
            self.shares[x] = f[x] % self.p
        return self.shares

    def reconstruct(self, shares: List[int]):
        """
        input:
            shares: a list of shares
        output: 
            the reconstructed secret from the list of shares
        """
        s = 0.0
        assert(len(shares) >= self.t)
        for i in range(self.t):
            s += shares[i] * self._delta(i, 0)

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

