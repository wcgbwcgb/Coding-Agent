import math


def poly(xs: list, x: float):
    """
    Evaluates polynomial with coefficients xs at point x.
    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n
    """
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])


def find_zero(xs: list):
    """ xs are coefficients of a polynomial.
    find_zero find x such that poly(x) = 0.
    find_zero returns only only zero point, even if there are many.
    Moreover, find_zero only takes list xs having even number of coefficients
    and largest non zero coefficient as it guarantees
    a solution.
    >>> round(find_zero([1, 2]), 2) # f(x) = 1 + 2x
    -0.5
    >>> round(find_zero([-6, 11, -6, 1]), 2) # (x - 1) * (x - 2) * (x - 3) = -6 + 11x - 6x^2 + x^3
    1.0
    """
    # Try multiple initial guesses for robust convergence
    best_x = 0.0
    best_f = float('inf')
    for guess in [-10.0, -5.0, -1.0, 0.0, 1.0, 5.0, 10.0]:
        x = guess
        for _ in range(200):
            f = poly(xs, x)
            if abs(f) < 1e-6:
                return x
            fprime = sum(i * coeff * (x ** (i - 1)) for i, coeff in enumerate(xs) if i > 0)
            if fprime == 0:
                x += 0.1
            else:
                # Backtracking line search to avoid divergence
                step = f / fprime
                for _ in range(10):
                    new_x = x - step
                    new_f = poly(xs, new_x)
                    if abs(new_f) < abs(f):
                        break
                    step *= 0.5
                else:
                    x = new_x
                    continue
                x = x - step
        f = poly(xs, x)
        if abs(f) < abs(best_f):
            best_f = f
            best_x = x
    # Refine best_x with a few more Newton steps
    x = best_x
    for _ in range(50):
        f = poly(xs, x)
        if abs(f) < 1e-6:
            return x
        fprime = sum(i * coeff * (x ** (i - 1)) for i, coeff in enumerate(xs) if i > 0)
        if fprime == 0:
            x += 0.1
        else:
            x -= f / fprime
    return x
