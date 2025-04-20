# password_utils.py
import random
import string


def generate_password(simple=True):
    """Generates a random password"""
    if simple:
        # Generate simple but memorable password
        adjectives = ["happy", "clever", "brave",
                      "wise", "gentle", "swift", "bright", "calm"]
        nouns = ["tiger", "river", "mountain", "forest",
                 "ocean", "desert", "cloud", "star"]
        numbers = [str(random.randint(10, 99)) for _ in range(1)]

        password = random.choice(
            adjectives) + random.choice(nouns) + random.choice(numbers)
    else:
        # Generate strong random password with special characters
        length = 16
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))

    return password
