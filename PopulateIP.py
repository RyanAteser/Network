import time

def calculate_subnet_mask(ip_address, cidr):
    # Split IP address to extract CIDR notation
    ip_parts = ip_address.split("/")
    if len(ip_parts) == 1:
        cidr = 32  # Set CIDR to 32 if not provided
    else:
        cidr = int(ip_parts[1]) 

    
    subnet_mask = []

    # Calculate the number of full octets
    
    full_octets = cidr // 8

    # Calculate the number of bits in the last octet
    remainder_bits = cidr % 8

    # Calculate the full octets
    for _ in range(full_octets):
        subnet_mask.append(255)

    # Calculate the last octet
    last_octet = 0
    for i in range(remainder_bits):
        last_octet += 2 ** (7 - i)
    subnet_mask.append(last_octet)

    # Add 0s to complete the subnet mask if necessary
    while len(subnet_mask) < 4:
        subnet_mask.append(0)

    return subnet_mask, cidr


def generate_config_commands(ip_addresses):
    commands = []

    for ip_address in ip_addresses:
        # Check if CIDR notation is present
        if "/" in ip_address:
            ip_parts = ip_address.split("/")
            ip = ip_parts[0]
            cidr = int(ip_parts[1])  # Extract CIDR notation and convert it to an integer
        else:
            continue  # Default CIDR notation if not provided

        # Calculate subnet mask
        subnet_mask, _ = calculate_subnet_mask(ip, cidr)
        subnet_mask_str = ".".join(str(octet) for octet in subnet_mask[:-1])

        # Create the command string
        command = "config firewall address\n"
        command += f"edit \"Zoom-{ip_address}\"\n"
        command += f"set subnet {ip} {subnet_mask_str}\n"
        command += "next\n"
        command += "end\n"

        commands.append(command)

    return commands

def execute_commands(commands):
    with open(r'C:\Users\rcate\IdeaProjects\Network-\outputFortIOS.txt', 'w') as file:
        file.write("Success:\n" + "\n".join(commands))

        

def send_commands_to_terminal(commands):
    # SecureCRT scripting commands
    
    crt.Screen.Synchronous = True

    try:
        for command in commands:
            if command != None:
                crt.Screen.Send(command + "\r")
                crt.Screen.WaitForString("#")
                #Adjust speed 
                time.sleep(1)
                
                with open(r'C:\Users\rcate\IdeaProjects\Network-\outputFortIOS.txt', 'w') as file:
                    file.write("Success Test Check Fortigate Dashboard to See if they have Populated:")

            
                
            
    except Exception as e:
        
        crt.Dialog.MessageBox("Error: Script Shut Down {}\n".format(str(e)))

def main():
    # Open the file and read lines
    with open(r'C:\Users\rcate\IdeaProjects\Network-\ip_address.txt', 'r') as file:
        for line in file:
            # Remove leading/trailing whitespaces and split if multiple IPs are on the same line
            ip_addresses = [ip.strip() for ip in line.split(",")]
            # Generate configuration commands for the IP addresses
            config_commands = generate_config_commands(ip_addresses)
            execute_commands(config_commands)
            # Send configuration commands to the terminal
    
            send_commands_to_terminal(config_commands)

main()
