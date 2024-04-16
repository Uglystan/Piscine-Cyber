import os
import sys
import re
import pyotp
import time
from cryptography.fernet import Fernet

def encode_key(key):
        f = open("ft_otp.key", "w")
        key.replace("1", "3")
        print(key)

def check_arg(arguments, key):
        if "-g" in arguments and len(arguments) == 3:
                if os.path.exists(arguments[arguments.index("-g") + 1]) == True and os.access(arguments[arguments.index("-g") + 1], os.R_OK) == True:
                        f = open(arguments[arguments.index("-g") + 1])
                        key = f.read()
                else:
                        key = arguments[arguments.index("-g") + 1]
                if len(key) >= 64 and re.match(r"^[0-9a-fA-F]+$", key) != None:
                        try:
                                encode_key(key)
                        except Exception as e:
                                print(e)
                else:
                        print("Invalid key")
        elif "-k" in arguments and len(arguments) == 3:
                print("K")
        else:
                print("Bad using")

def main():
    arguments = sys.argv
    key: str = ""
    check_arg(arguments, key)
    
        
if __name__ == "__main__":
        main()