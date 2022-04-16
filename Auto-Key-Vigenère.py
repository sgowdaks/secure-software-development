sentence = "TAKEACOPYOFYOURPOLICYTONORMAWILCOXONTHETHIRDFLOOR"
key = "ciphertext"
key = key.upper()
n = len(key)
#print(key)
j = 0
new_ = ""
for i, val in enumerate(sentence):
    if i > n - 1:
        #print(ord(val), ord(new_[j]))
        k =  ord(val) - 65 +  ord(new_[j]) - 65
        j = j + 1 
        #print(k)
        if k > 25:
            k = k % 25
            #print(k)
        new_ += chr(k+65)
    else:
        new_ = new_ + key[i]
        
print(new_)
        
