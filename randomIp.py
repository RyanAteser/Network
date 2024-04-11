import random


def generate_random_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))


# Generate 100 random IP addresses
random_ips = [generate_random_ip() for _ in range(100)]

# Display the list of generated IP addresses
with open('ip_address.txt', 'w') as file:

    for ip in random_ips:
        random_number = random.randint(1, 32)
        file.write(ip + "\n")
        file.write(ip +"/" + str(random_number) + "\n")

