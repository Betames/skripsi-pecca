import random


class Primes:
    def ipow(self, a, b, n):
        """calculates (a**b) % n via binary exponentiation, yielding itermediate
        results as Rabin-Miller requires"""
        A = a = a % n
        yield A
        t = 1
        while t <= b:
            t <<= 1

        # t = 2**k, and t > b
        t >>= 2

        while t:
            A = (A * A) % n
            if t & b:
                A = (A * a) % n
            yield A
            t >>= 1

    def rabin_miller_witness(self, test, possible):
        """Using Rabin-Miller witness test, will return True if possible is
        definitely not prime (composite), False if it may be prime."""
        return 1 not in self.ipow(test, possible - 1, possible)

    smallprimes = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                   47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                   103, 107, 109, 113, 127, 131, 137, 139, 149,
                   151, 157, 163, 167, 173, 179, 181, 191, 193,
                   197, 199, 211, 223, 227, 229, 233, 239, 241,
                   251, 257263, 269, 271, 277, 281, 283, 293,
                   307, 311, 313, 317, 331, 337, 347, 349)

    def default_k(self, bits):
        return max(64, 2 * bits)

    def is_probably_prime(self, possible, k=None):
        if k is None:
            k = self.default_k(possible.bit_length())
        for i in self.smallprimes:
            if possible % i == 0:
                return False
        for i in range(int(k)):
            test = random.randrange(2, possible) | 1
            if self.rabin_miller_witness(test, possible):
                return False
        return True

    def generate_prime(self, bits, k=None):
        """Will generate an integer of b bits that is probably prime
        (after k trials). Reasonably fast on current hardware for
        values of up to around 512 bits."""
        assert bits >= 8

        if k is None:
            k = self.default_k(bits)

        while True:
            possible = random.randrange(2 ** (bits - 1) + 1, 2 ** bits) | 1
            if self.is_probably_prime(possible, k):
                return possible


prime_class = Primes()
