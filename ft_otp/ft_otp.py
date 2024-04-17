import os
import sys
import re
import time
import hashlib

def gen_otp(key):
        t = int(time.time() // 10) #Retourne la division entiere entre le temps et 30 donc le resultat change toutes les 30sec
        time_counter_bytes = t.to_bytes(t.bit_length(), 'big') #Convertir le nombre en binaire en big endian
        sha256_hash = hashlib.sha256()
        sha256_hash.update(key.encode())
        sha256_hash.update(time_counter_bytes) #On encode la key avec le temps donc pendant 30sec c'est tjr le meme temps donc le m^ code
        hmac_digest = sha256_hash.digest()
        offset = int(t % 8) # Genere un nombre pseudo aleatoire entre 0 et 15
        code = int.from_bytes(hmac_digest[offset:offset + 8], 'big') # On selectionne une plage de bytes en focntion de offset sur le hash et on le transofrme en int
        print("totp:", code % 1000000) #On affiche les 6 derniers chiffre du code

def store_hash_key(key):
        f = open("ft_otp.key", "w")
        sha256_hash = hashlib.sha256()
        sha256_hash.update(key.encode())
        f.write(sha256_hash.hexdigest())

def check_arg(arguments, key):
        if "-g" in arguments and len(arguments) == 3:
                if os.path.exists(arguments[arguments.index("-g") + 1]) == True and os.access(arguments[arguments.index("-g") + 1], os.R_OK) == True:
                        f = open(arguments[arguments.index("-g") + 1])
                        key = f.read()
                else:
                        key = arguments[arguments.index("-g") + 1]
                if len(key) >= 64 and re.match(r"^[0-9a-fA-F]+$", key) != None:
                        try:
                                store_hash_key(key)
                        except Exception as e:
                                print(e)
                else:
                        print("Invalid key")
        elif "-k" in arguments and len(arguments) == 3:
                if os.path.exists(arguments[arguments.index("-k") + 1]) == True and os.access(arguments[arguments.index("-k") + 1], os.R_OK) == True:
                        f = open(arguments[arguments.index("-k") + 1])
                        key = f.read()
                else:
                        key = arguments[arguments.index("-k") + 1]
                gen_otp(key)
        else:
                print("Bad using")

def main():
    arguments = sys.argv
    key: str = ""
    check_arg(arguments, key)
    
        
if __name__ == "__main__":
        main()