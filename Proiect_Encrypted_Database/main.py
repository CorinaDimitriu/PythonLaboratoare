import time

import aes128

if __name__ == "__main__":
    counter, cipher = aes128.encrypt_aes128("54776F204F6E65204E696E652054776F",
                                            "5468617473206D79204B756E67204675")
    print(cipher)
    print(aes128.decrypt_aes128(counter, cipher, "5468617473206D79204B756E67204675"))
