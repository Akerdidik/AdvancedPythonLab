# Find function to find in which index located char, in this case only lowercase!
def finder(a,b):
    return b.index(a)

# Vigenere cypher mini edition (only lowercase)
def vigenere(text,keys): 
    alph = [chr(i) for i in range(ord('a'),ord('z')+1)]
    lens = len(text)
    dupl = ''
    cnt = 0

    for i in range(lens):

        if cnt  == len(keys):
            cnt=0

        t = finder(text[i],alph)

        if t + keys[cnt]<len(alph):
            dupl+=alph[t+keys[cnt]]
            cnt=cnt+1

        else:
            dupl+=alph[t-(26-keys[cnt])]
            cnt=cnt+1

    return dupl   

def key(str):
    keys=[]
    alph=[chr(i)for i in range(ord('a'),ord('z')+1)]

    for i in str:
        
        keys.append(finder(i,alph))

    return keys

# Main function
def main():
    text = input("Enter your message: ")
    keys = input("Your ciphering key: ")
    print("Your encoded message: " + vigenere(text,key(keys)))

# Runner   
if __name__=="__main__":
    main()
