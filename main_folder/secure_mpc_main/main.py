
from secrets import AdditiveSecretSharing, ShamirSecretSharing
from typing import List

def additive(secret, n):
    additive_sharing = AdditiveSecretSharing(n=n)
    all_shares = additive_sharing.generate(s=secret)
    s = additive_sharing.reconstruct(shares=all_shares)
    print(f"secret: {secret}, n={n}")
    print(f"all shares: {all_shares}")
    print(f"reconstructed: {s}")

def shamir(secret, n, t):
    shamir = ShamirSecretSharing(n=n, t=t)
    all_shares = shamir.generate(s=secret)
    ts = t+2
    shares = all_shares[2:ts]
    s = shamir.reconstruct(shares=shares)
    print(f"secret: {secret}, n={n}, t={t}")
    print(f"all shares: {all_shares}")
    print(f"shares: {shares}")
    print(f"reconstructed: {s}")
    print(f"poly: {shamir.poly()}")

def main():
    print("-------- Additive Secret Sharing ---------")
    additive(secret=22, n=5)

    print("\n-------- Shamir Secret Sharing ---------")
    shamir(secret=20, n=7, t=4)


if __name__ == '__main__':
    main()
