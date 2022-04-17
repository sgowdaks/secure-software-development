p = 100392089237316158323570985008687907853269981005640569039457584007913129640081
q = 90392089237316158323570985008687907853269981005640569039457584007913129640041
e = 65537
d = pow((p-1)*(q-1), -1, e)
n = p * q
string_ = "Scaramouche, Scaramouche, will you do the Fandango? "
string_to_decimal = "83 99 97 114 97 109 111 117 99 104 101 44 32 83 99 97 114 97 109 111 117 99 104 101 44 32 119 105 108 108 32 121 111 117 32 100 111 32 116 104 101 32 70 97 110 100 97 110 103 111 63 32"
new_string = string_to_decimal.split(" ")

encrypted_text = []
for i in new_string:
    encrypted_text.append((int(i) ** e)%n)
print(encrypted_text)

new_decrypt = []
j = 0
for i in encrypted_text:
    new_decrypt.append((i**d)%n)
print(new_decrypt)
