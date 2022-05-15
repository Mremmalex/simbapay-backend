from nanoid import generate


def accountNumberGen():
    nano = generate("1234567890", 10)
    return nano
