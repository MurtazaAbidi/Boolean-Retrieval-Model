from operator import itemgetter
import re
import eel

def stopwords(txt):
    txt = txt.lower()
    sw = re.split('\W+', txt)
    return sw

def tokenize(txt, sw):
    txt = txt.lower()
    tokens = re.split('\W+', txt)
    for i in tokens:
    #     if len(i) > 5 and i[-1] == 'g' and i[-2] == 'n' and i[-3] == 'i':
    #         i = i[:-3]
        if i in sw :
            tokens.remove(i)
    return tokens

def intersect (A,B,term, posting_list):
    result = []
    first=0
    second= 0
    flag=0
    for x in range(len(term)):
        if (term[x]==A):
            first=x
            flag+=1
        if (term[x]==B):
            second=x
            flag+=1
        if flag>=2:break
    word1=posting_list[first]
    word2=posting_list[second]
    i=0
    j=0

    while True:
        if (i>=len(posting_list[first]) or j>=len(posting_list[second])):break
        if (word1[i][0]==word2[j][0]):
            result.append(word1[i][0])
            i+=1
            j+=1
        elif word1[i]<word2[j]:
            i+=1
        else:
            j+=1
    result = list(dict.fromkeys(result))
    return result
def intersect2(A,B):
    i=0
    j=0
    res=[]
    while True:
        if (i>=len(A) or j>=len(B)):break
        if (A[i]==B[j]):
            res.append(A[i])
            i+=1
            j+=1
        elif A[i]<B[j]:
            i+=1
        else:
            j+=1
    result = list(dict.fromkeys(res))
    return result

def find_union(A,B,term,posting_list):
    res1=union(A,B,term,posting_list)
    res2=search(A,term,posting_list)
    res3=search(B,term,posting_list)
    res= res1+res2+res3
    result = list(dict.fromkeys(res))
    result.sort()
    return result

def union (A,B,term, posting_list):
    result = []
    first=0
    second= 0
    flag=0
    for x in range(len(term)):
        if (term[x]==A):
            first=x
            flag+=1
        if (term[x]==B):
            second=x
            flag+=1
        if flag>=2:break
    word1=posting_list[first]
    word2=posting_list[second]
    i=0
    j=0
    while True:
        if (i>=len(word1) and j>=len(word2)):break
        if j<len(word2):
            result.append(word2[j][0])
            j+=1
        if i<len(word1):
            result.append(word1[i][0])
            i+=1

    result = list(dict.fromkeys(result))
    return result

def not_of (A,term,posting_list):
    res= []
    temp= []
    flag=0
    for x in range(len(term)):
        if (term[x] == A):
            first= x
            flag += 1
        if flag >= 1: break
    word= posting_list[first]
    for i in range(len(word)):
        temp.append(word[i][0])
    for i in range(len(term)):
        if posting_list[i][1] not in temp:
            res.append(posting_list[i][1])
    return res

def search(A,term,posting_list):
    if A[-1]=='s':
        word1=A[0:-1]
    else:
        word1 = A+'s'
    word2 = A+'ing'
    word3 = A+'er'
    if A[-1] == 's' and A[-2]=='e':
        word4 = A[0:-2]
    else:
        word4 = A+'es'
    result = []
    flag = 0
    for x in range(len(term)):
        if (term[x] == A):
            first=x
            flag += 1
        if flag >= 1: break
    word= posting_list[first]
    ans1 =union(word1,word2,term,posting_list)
    ans2 =union(word3,word4,term,posting_list)
    res=ans1+ans2
    for i in range(len(word)):
        result.append(word[i][0])
    result+=res
    result = list(dict.fromkeys(result))
    result.sort()
    return result

def proximity_search (A,B,term,posting_list,num):
    result= []
    result= proximiti_search (A,B,term,posting_list,num)
    word1=A+'ing'
    word2=A+'s'
    word3=B+'ing'
    word4=B+'s'
    result+=proximiti_search (A,word3,term,posting_list,num)
    result+=proximiti_search (A,word4,term,posting_list,num)
    result+=proximiti_search (word1,B,term,posting_list,num)
    result+=proximiti_search (word1,B,term,posting_list,num)
    result = list(dict.fromkeys(result))
    result.sort()
    return result

def proximiti_search (A,B,term,posting_list,num):
    result = []
    first = 0
    second = 0
    flag = 0
    for x in range(len(term)):
        if (term[x] == A):
            first = x
            flag += 1
        if (term[x] == B):
            second = x
            flag += 1
        if flag >= 2: break
    word1 = posting_list[first]
    word2 = posting_list[second]
    temp= []
    for i in range(len(word2)):
        temp.append(word2[i][0])
    for i in range (len(word1)):
        if (word1[i][0] in temp):
            for j in range(len (word2)):
                if word1[i][0]==word2[j][0]:
                    # print (word1[i][0],word2[j][0],word1[i][1],word2[j][1])
                    temp1=num
                    while(temp1>0):
                        if word1[i][1]==word2[j][1]+temp1:
                            result.append(word1[i][0])
                        if word2[j][1]==word1[i][1]+temp1:
                            result.append(word1[i][0])
                        temp1-=1
    result = list(dict.fromkeys(result))
    result.sort()
    return result

fstopwords = open("Stopword-List.txt", "r")
stopword = fstopwords.read()
stop_words_tokens = stopwords(stopword)
fstopwords.close()
tokens = []

for i in range(449):
    if i == 0:
        continue
    filename = "text files\\" + str(i) + ".txt"
    f = open(filename, "r")
    txt = f.read()
    tokens.append(tokenize(txt, stop_words_tokens))
    f.close()

term_docid = []
for i in range(len(tokens)):
    for j in range(len(tokens[i])):
        temp = []
        temp.append(i + 1)
        temp.append(tokens[i][j])
        temp.append(j)
        term_docid.append(temp)

term_docid = sorted(term_docid, key=itemgetter(1))

@eel.expose
def start(query):
    eel.emptytextarea()
    eel.printthere("Loading . . . . ")
    term = []
    posting_list= []
    # file1 = open("term.txt","r")
    # # while term1=file1.readline():
    # abc=[]
    # term1= file1.readline()
    # term.append(term1)
    # term1= file1.readline()
    # term.append(term1)
    # while term1:
    #     term1= file1.readline()

    #     temp=term1[:-1]
    #     term.append(temp)
    # file1.close()
    # print(len(abc))
    # file2= open("posting_list.txt", "r")
    # postlist= file2.readline() 
    # while postlist:
    #     temp=postlist[:-1]
    #     posting_list.append(temp)
    #     postlist= file2.readline()
        

    # # posting_list1= file2.readlines()
    # file2.close()
    
    # print("\n\n\n\n\n")
    # print(term1)
    # print("\n\n\n\n\n")
    
    posting_temp= []
    temp = []
    # print("\n\n\n\n\n\n")
    # print(posting_list1)
    for i in range (len(term_docid)):
        if term_docid[i][1] not in term:
            term.append(term_docid[i][1])
    # print (term_docid[2349][1])
    
    j=0
    for i in term:
        if (j>=len(term_docid)):break
        posting_temp= []
        while (term_docid[j][1] == i):
            if(term_docid[j][1]==i):
                # print (term_docid[j][1]," ",i)
                temp= []
                temp.append(term_docid[j][0])
                temp.append(term_docid[j][2])
                posting_temp.append(temp)
                j+=1
            else:
                j+=1
                break
            if(j>=len(term_docid)):break

        posting_list.append(posting_temp)
        posting_temp=[]
    # for i in range(len(posting_list)):
    #   print (term[i],"---->",posting_list[i])
    print ("length of Total distinct term : ", len(term))
    trm = open("term.txt", "w")
    for ele in term:
        trm.write(ele+"\n")
        # print(ele+"\n")
    # trm.write(str(term))
    trm.close()
    pl = open("posting_list.txt", "w")
    for ele in posting_list:

        pl.write(str(ele))
        pl.write("\n")
        # print(ele)
        # print("\n")
    # pl.write(str(posting_list))
    pl.close()
    # query_tokens
    # term
    # posting_list

    # query = input ("Enter Query: ")
    query_tokens = query.split()



    ans= []
    if (len(query_tokens)==1):
        ans=search(query_tokens[0],term,posting_list)
    elif (len(query_tokens)==2):
        if (query_tokens[0]=='NOT'):
            ans=not_of(query_tokens[1],term,posting_list)
    elif (len(query_tokens)==3):
        if query_tokens[1]=='AND':
            ans= intersect(query_tokens[0],query_tokens[2],term,posting_list)
        elif query_tokens[1]=='OR':
            ans=find_union(query_tokens[0],query_tokens[2],term,posting_list)
        elif query_tokens[-1][0]=='/':
            ans=proximity_search(query_tokens[0],query_tokens[1],term,posting_list,int(query_tokens[-1][1])+1)

    elif (len(query_tokens) > 3):
        if query_tokens[1]=='AND':
            ans= intersect(query_tokens[0],query_tokens[2],term,posting_list)
            if (query_tokens[3]=='OR'):
                ans+=search(query_tokens[4],term,posting_list)
                ans = list(dict.fromkeys(ans))
                ans.sort()
            elif (query_tokens[3]=='AND'):
                ans1=search(query_tokens[4],term,posting_list)
                ans=intersect2(ans,ans1)


        elif query_tokens[1]=='OR':
            ans=find_union(query_tokens[0],query_tokens[2],term,posting_list)
            if (query_tokens[3]=='OR'):
                ans+=search(query_tokens[4],term,posting_list)
                ans = list(dict.fromkeys(ans))
                ans.sort()
            elif (query_tokens[3]=='AND'):
                ans1 = search(query_tokens[4], term, posting_list)
                ans = intersect2(ans, ans1)
    print("\n_____________________________________________________")
    print ("Documents which satisfy this Boolean query are: ")
    eel.emptytextarea()
    eel.printthere("Documents Retrieved for this Query (<b>"+query+"</b>) are: <br><br>")
    for i in range(len(ans)):
        print (str(ans[i])+".txt", end="  ")
        eel.printthere(str(ans[i])+".txt &nbsp;")
    print("\n_____________________________________________________")

eel.init("web")
eel.start("index.html")