# password_utils.py
import random
import string


def generate_password(simple=True):
    """Generates a random password"""
    if simple:
        # Generate simple but memorable password
        adjectives = ["happy", "clever", "brave", "wise", "gentle",
                      "swift", "bright", "calm", "lucky", "mighty",
                      "noble", "quick", "silent", "smart", "sunny"]
        nouns = ["tiger", "river", "mountain", "forest", "ocean",
                 "desert", "cloud", "star", "eagle", "dragon",
                 "castle", "garden", "island", "melody", "wizard"]
        numbers = [str(random.randint(10, 99)) for _ in range(1)]

        password = random.choice(adjectives) + \
            random.choice(nouns) + random.choice(numbers)
    else:
        # Generate strong random password with special characters
        length = 16
        # Ensure at least one of each character type
        lowercase = random.choice(string.ascii_lowercase)
        uppercase = random.choice(string.ascii_uppercase)
        digit = random.choice(string.digits)
        special = random.choice('!@#$%^&*()-_=+[]{}|;:,.<>?')

        # Fill the rest with random characters
        remaining_length = length - 4
        remaining_chars = ''.join(random.choice(string.ascii_letters + string.digits + '!@#$%^&*()-_=+[]{}|;:,.<>?')
                                  for _ in range(remaining_length))

        # Combine all characters and shuffle
        all_chars = lowercase + uppercase + digit + special + remaining_chars
        char_list = list(all_chars)
        random.shuffle(char_list)
        password = ''.join(char_list)

    return password
