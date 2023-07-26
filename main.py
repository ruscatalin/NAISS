from ecdsa import SigningKey, NIST256p
import rsa
import time
import matplotlib.pyplot as plt

def generate_key(algorithm):
    """
    Generates and returns a private key using the NIST256p EC curve.
    """
    if algorithm == "EC":
        pk = SigningKey.generate(curve=NIST256p)
        public_key = pk.get_verifying_key()
        return (public_key, pk)
    elif algorithm == "RSA":
        return rsa.newkeys(3072, poolsize=8)
    
def get_signature(input, private_key, algorithm):
    """
    Returns the deterministic signature of an input using the private key.

    Parameters:
        input (bytes or str): The input to sign.
        private_key (ecdsa.SigningKey): The private key to use for signing.
    Returns:
        str: The deterministic signature of the input, represented with hexadecimal characters.
    """
    if type(input) != bytes:
        input = input.encode('utf-8')

    if algorithm == "EC":
        return private_key.sign_deterministic(input).hex()
    elif algorithm == "RSA":
        return rsa.sign(input, private_key, 'SHA-256').hex()
    

def verify_signature(input, signature, public_key, algorithm):
    """
    Verifies the signature of an input using the public key.

    Parameters:
        input (bytes or str): The input to verify.
        signature (str): The signature to verify.
        public_key (ecdsa.VerifyingKey): The public key to use for verification.
    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    if type(input) != bytes:
        input = input.encode('utf-8')

    if algorithm == "EC":
        try:
            return public_key.verify(bytes.fromhex(signature), input)
        except:
            return False
    elif algorithm == "RSA":
        try:
            return rsa.verify(input, bytes.fromhex(signature), public_key)
        except:
            return False



if __name__ == "__main__":
    start_time = time.time()
    iterations = 1000

    # record the time it takes to generate a key pair

    time_now = time.time()
    EC_keys = []
    for i in range(iterations):
        EC_keys.append(generate_key("EC"))
    time_EC = time.time() - time_now
    time_EC_gen = round(time_EC/iterations, 4)
    print("EC key generation DONE")

    time_now = time.time()
    RSA_keys = []
    for i in range(iterations):
        RSA_keys.append(generate_key("RSA"))
    time_RSA = time.time() - time_now
    time_RSA_gen = round(time_RSA/iterations, 4)
    print("RSA key generation DONE")

    # record the time it takes to sign a file
    file_data = None
    with open("logo.png", "rb") as f:
        file_data = f.read()

    time_now = time.time()
    EC_signatures = []
    for i in range(iterations):
        EC_signatures.append(get_signature(file_data, EC_keys[i][1], "EC"))
    time_EC = time.time() - time_now
    time_EC_sign = round(time_EC/iterations, 4)
    print("EC signing DONE")

    time_now = time.time()
    RSA_signatures = []
    for i in range(iterations):
        RSA_signatures.append(get_signature(file_data, RSA_keys[i][1], "RSA"))
    time_RSA = time.time() - time_now
    time_RSA_sign = round(time_RSA/iterations, 4)
    print("RSA signing DONE")

    # record the time it takes to verify a file

    time_now = time.time()
    for i in range(iterations):
        verify_signature(file_data, EC_signatures[i], EC_keys[i][0], "EC")
    time_EC = time.time() - time_now
    time_EC_verify = round(time_EC/iterations, 4)
    print("EC verification DONE")

    time_now = time.time()
    for i in range(iterations):
        verify_signature(file_data, RSA_signatures[i], RSA_keys[i][0], "RSA")
    time_RSA = time.time() - time_now
    time_RSA_verify = round(time_RSA/iterations, 4)
    print("RSA verification DONE")

    # Print out the summary of the results
    print("All this took " + str(round(time.time() - start_time, 3)) + " seconds")
    print(".........SUMMARY..........")
    print("EC key generation time:   " + str(time_EC_gen))
    print("RSA key generation time:  " + str(time_RSA_gen))
    print("EC signing time:          " + str(time_EC_sign))
    print("RSA signing time:         " + str(time_RSA_sign))
    print("EC verification time:     " + str(time_EC_verify))
    print("RSA verification time:    " + str(time_RSA_verify))
    print(".......TOTAL TIMES........")
    print("EC total time:            " + str(time_EC_gen + time_EC_sign + time_EC_verify))
    print("RSA total time:           " + str(time_RSA_gen + time_RSA_sign + time_RSA_verify))

    plt.figure(figsize=(20, 5))
    plt.subplot(1, 3, 1)
    plt.bar(["EC", "RSA"], [time_EC_gen, time_RSA_gen], color=["#005BBB", "#FFD500"])
    for i in range(2):
        plt.text(i, [time_EC_gen, time_RSA_gen][i] + 0.0005, str([time_EC_gen, time_RSA_gen][i]), ha="center", va="bottom", fontdict={"fontweight": "bold"})
    plt.title("Key generation")
    plt.ylabel("Time (s)")

    plt.subplot(1, 3, 2)
    plt.bar(["EC", "RSA"], [time_EC_sign, time_RSA_sign], color=["#005BBB", "#FFD500"])
    for i in range(2):
        plt.text(i, [time_EC_sign, time_RSA_sign][i] + 0.0005, str([time_EC_sign, time_RSA_sign][i]), ha="center", va="bottom", fontdict={"fontweight": "bold"})
    plt.title("Signing")
    plt.ylabel("Time (s)")

    plt.subplot(1, 3, 3)
    plt.bar(["EC", "RSA"], [time_EC_verify, time_RSA_verify], color=["#005BBB", "#FFD500"])
    for i in range(2):
        plt.text(i, [time_EC_verify, time_RSA_verify][i], str([time_EC_verify, time_RSA_verify][i]), ha="center", va="bottom", fontdict={"fontweight": "bold"})
    plt.title("Verification")
    plt.ylabel("Time (s)")

    plt.savefig("nasiss_speed.pdf")

