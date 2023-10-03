import random

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
        