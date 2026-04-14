# fermat_theorem.py

def mod_pow(base, exp, mod):
    """Compute (base^exp) % mod efficiently."""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result

def is_prime_fermat(n, witnesses=None):
    """Test primality using Fermat's Little Theorem."""
    if witnesses is None:
        witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23]  # Common witnesses

    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    steps = []
    for a in witnesses:
        if a >= n:
            break
        steps.append(f"Testing a = {a}")
        if mod_pow(a, n-1, n) != 1:
            steps.append(f"a^(n-1) mod n = {mod_pow(a, n-1, n)} ≠ 1")
            steps.append(f"{n} is composite (Fermat's test failed)")
            return False, steps
        else:
            steps.append(f"a^(n-1) mod n = {mod_pow(a, n-1, n)} = 1 ✓")

    steps.append(f"{n} passes Fermat's test for witnesses {witnesses[:len([s for s in steps if 'Testing a =' in s])]}")
    return True, steps

def fermat_little_theorem_demo(a, p):
    """Demonstrate Fermat's Little Theorem: a^(p-1) ≡ 1 mod p if p is prime and gcd(a,p)=1."""
    if not (1 < a < p):
        return None, "a must be between 1 and p-1"

    steps = []
    steps.append(f"Testing Fermat's Little Theorem: a^(p-1) ≡ 1 mod p")
    steps.append(f"a = {a}, p = {p}")

    # Check if p is prime (simple check)
    if p < 2 or any(p % i == 0 for i in range(2, int(p**0.5)+1)):
        return None, f"p = {p} is not prime"

    # Compute a^(p-1) mod p
    result = mod_pow(a, p-1, p)
    steps.append(f"Computing {a}^({p}-1) mod {p}")
    steps.append(f"Result: {result}")

    if result == 1:
        steps.append("✓ Fermat's Little Theorem holds")
        return True, steps
    else:
        steps.append("✗ Fermat's Little Theorem does not hold")
        return False, steps