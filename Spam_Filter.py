# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 10:17:16 2016

@author: Yudi Dong
"""
##############################################################################
'''
Training Phase: training set contains 11,835 hams and 17,546 spams 
'''
##############################################################################
#The  occurrence probability of very word in the ham
import time
import re
import glob

start_time1 = time.time()

ham = glob.glob('training_data/ham/*/*')


##########

words_pr_ham = {}
for item in ham:
    mail = open(item).read()
    seg = re.findall('[A-Za-z]+',str.lower(mail))
    seg = list(set(seg))
    for word in seg:
        words_pr_ham[word] = words_pr_ham.get(word, 0) + 1
keys = list(words_pr_ham.keys())
for key in keys:
    nu = re.search('\d+',key)
    if nu or len(key)<3 or words_pr_ham[key]<3 or len(key)>20:
        del  words_pr_ham[key] 
            
for key in words_pr_ham.keys():
    words_pr_ham[key]=float(words_pr_ham[key])/len(ham)
    
    
#The  occurrence probability of very word in the spam
spam = glob.glob('training_data/spam/*/*')

words_pr_spam = {}
for item in spam:
    mail = open(item).read()
    seg = re.findall('[A-Za-z]+',str.lower(mail))
    seg = list(set(seg))
    for word in seg:
        words_pr_spam[word] = words_pr_spam.get(word, 0) + 1
keys = list(words_pr_spam.keys())
for key in keys:
    nu = re.search('\d+',key)
    if nu or len(key)<3 or words_pr_spam[key]<3 or len(key)>20:
        del  words_pr_spam[key]
            
for key in words_pr_spam.keys():
    words_pr_spam[key]=float(words_pr_spam[key])/len(spam)

##############################################################################################
'''
Testing Phase: Utilize Naive Bayes algorithm. Testing set contains 9,232 hams and 14,215 spams
'''
##############################################################################################
start_time2 = time.time()

# Test set
TEST_MAIL = "testing_data/spam/*/*"
test_set = glob.iglob(TEST_MAIL)

COUNT = 0
prediction =[]
for mail in test_set:
    COUNT = COUNT +1
    # suppose that prior probability of ham and spam are all 50%
    P_Spam = 0.5
    P_Ham = 0.5
    #Extract the word in the test mail
    test_mail = open(mail).read()
    word_list = re.findall('[A-Za-z]+',str.lower(test_mail))
    for item in word_list:
        nu = re.search('\d+',item)
        if nu or len(item)==1 or len(item)==2:
            word_list.remove(item)

    P_Spam_Word ={}
    for word in word_list:
        if words_pr_ham.has_key(word) and words_pr_spam.has_key(word):
            P_Spam_Word[word] = (words_pr_spam[word]*P_Spam)/(words_pr_spam[word]*P_Spam + words_pr_ham[word]*P_Ham)
        if not words_pr_ham.has_key(word) and words_pr_spam.has_key(word):
            P_Spam_Word[word] = (words_pr_spam[word]*P_Spam)/(words_pr_spam[word]*P_Spam + 0.01*P_Ham)
        if words_pr_ham.has_key(word) and not words_pr_spam.has_key(word):
            P_Spam_Word[word] = (0.01*P_Spam)/(0.01*P_Spam + words_pr_ham[word]*P_Ham)
        if not words_pr_ham.has_key(word) and not words_pr_spam.has_key(word):
            P_Spam_Word[word] = 0.4

    # Sort the P_Spam_Word and extract 
    P_Spam_Word_sorted = sorted(P_Spam_Word.items(), key=lambda e:e[1], reverse=True)
    
    if len(P_Spam_Word_sorted ) < 15:
        P_Spam_Word_fit =[]
        for i in range(len(P_Spam_Word_sorted )):
            P_Spam_Word_fit.append(P_Spam_Word_sorted[i][1])
        #Caulate the joint probability of these 15 words
        mult1 = 1
        mult2 = 1
        for item in P_Spam_Word_fit:
            mult1 = mult1 * item
            mult2 = mult2 * (1-item)
        P = mult1 / (mult1+mult2)
        if P == 1.0:
            prediction.append("Spam")
        else:
            prediction.append("Ham")
        
    else:
        # Extract the 15 words which have the higher probability
        P_Spam_Word_15 =[]
        for i in range(15):
            P_Spam_Word_15.append(P_Spam_Word_sorted[i][1])
    
        #Caulate the joint probability of these 15 words
        mult1 = 1
        mult2 = 1
        for item in P_Spam_Word_15:
            mult1 = mult1 * item
            mult2 = mult2 * (1-item)
        P = mult1 / (mult1+mult2)
        if P == 1.0:
            prediction.append("Spam")
            p = "Spam"
        else:
            prediction.append("Ham")
            p = "Ham"
        
        
        print "Test %d : "%COUNT + p
        
ham_count = 0
spam_count = 0
for item in prediction:
            if item =="Ham":
                ham_count = ham_count + 1
            else:
                spam_count = spam_count + 1
#CR = (1-float(spam_count)/(ham_count+spam_count))*100
CR = (float(spam_count)/(ham_count+spam_count))*100
                
print "Ham number: %d"%ham_count + "\n"+ "Spam number: %d"%spam_count + "\n"+ "Correct rate: %.2f"%CR+"%" 
   
print("Training Phase spends %.2f s"%(start_time2-start_time1) + "\n" + "Testing Phase spends %.2f s"%(time.time()-start_time2))    

        
        
            
        
