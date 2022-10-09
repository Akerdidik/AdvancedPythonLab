from numpy import sort


def finder(a,b):
    return a in b

def misser(a):
    sort(a)
    res=[]

    for i in range(a[0],a[len(a)-1]+1):

        if not finder(i,a):
            res.append(i)

    return res

def main():
    d = input("Enter the numbers in the array (by spaces): ").split(' ')
    t = []

    for i in d:

        t.append(int(i))
    
    print(misser(t))

if __name__=="__main__":
    main()
        
