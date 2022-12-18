import aes128
import shared

aes128.encrypt_aes128("54776F204F6E65204E696E652054776F",
                      "5468617473206D79204B756E67204675")
print(shared.ciphertext)
# print(aes128.decrypt_aes128(counter1, ciphertext1, "5468617473206D79204B756E67204675"))

# print(aes128.apply_main_transformations("29C3505F571420F6402299B31A02D73A", 'decrypt'))
