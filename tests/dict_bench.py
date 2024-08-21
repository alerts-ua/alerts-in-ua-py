"""
Bench dict inversion method
"""
import timeit

# Test setup
original_dict = {str(i): i for i in range(1000)}


# Using dictionary comprehension
def switch_using_comprehension(d):
    return {v: k for k, v in d.items()}


# Using zip()
def switch_using_zip(d):
    return dict(zip(d.values(), d.keys()))


# Timing both approaches
comprehension_time = timeit.timeit(lambda: switch_using_comprehension(original_dict), number=100000)
zip_time = timeit.timeit(lambda: switch_using_zip(original_dict), number=100000)

print(f"Comprehension time: {comprehension_time:.6f}")  # 3.8s
print(f"Zip time: {zip_time:.6f}")  # 2.7s

# NOTE: zip() at least 30% faster
