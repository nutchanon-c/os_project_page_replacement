# add comment for push
from os import replace
import re
from typing import Sequence, final
from django.shortcuts import render
from django.http import HttpResponse
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
import secrets
from django.utils.safestring import mark_safe
from django.db import models

global fifofinalList, fifofinalstr, fifofault, fifohit, fiforatio
global lrufinalList, lrufinalstr, lrufault, lruhit, lruratio
global a, n, m
global optfinalList, optfinalstr, optfault, opthit, optratio


def transpose(l1, num):
    for i in l1:
        while(len(i) < num):
            i.append("-")      



    l2 = list(zip(*l1))
    #print(l1)
    #print(l2)
    return l2

def __optimal():
    global optfinalList, optfinalstr, optfault, opthit, optratio
    global a,n,m
    x = 0
    page_faults = 0
    page = []
    FREE = -1
    optallList = []
    for i in range(m):
        page.append(FREE)

    for i in range(n):        
        flag = 0
        for j in range(m):
            if(page[j] == a[i]):
                flag = 1 #hit
                temp = page[:]
                break
            
        if flag == 0:
            # look for an empty one
            faulted = False
            new_slot = FREE
            for q in range(m):
                if page[q] == FREE: #has empty
                    faulted = True
                    new_slot = q
            
            if not faulted:
                # find next use farthest in future
                max_future = 0
                max_future_q = FREE
                for q in range(m):
                    if page[q] != FREE:
                        found = False
                        for ii in range(i, n):
                            if a[ii] == page[q]:
                                found = True
                                if ii > max_future:
                                    # print "\n\tFound what will be used last: a[%d] = %d" % (ii, a[ii]),
                                    max_future = ii #ii is index in index in sequence
                                    max_future_q = q #q is index in frames (page)

                                break
                        
                        if not found:
                            # print "\n\t%d isn't used again." % (page[q]),
                            max_future_q = q
                            break

                faulted = True
                new_slot = max_future_q
            
            page_faults += 1
            #print(page)
            page[new_slot] = a[i]
        
            
            temp = page[:]
            temp[temp.index(a[i])] = 'red' + str(a[i])
        temp = list(reversed(temp))
        temp = [str(n) for n in temp]

        for jj in range(len(temp)):
            if temp[jj] == '-1':
                temp[jj] = '-'

        optallList.append(temp)
        #print(optallList)
    optfinalList = transpose(optallList, m)

    #optfinalList = [list(map(str, i)) for i in optfinalList]
    #print(optfinalList)


    optfinalstr = ''
    for lists in optfinalList:
        optfinalstr += '<tr>'
        for attr in lists:
            if 'red' in attr:
                optfinalstr += '<td style="padding: 20px;background-color:#f44336;text-align: center;">'+attr[3:]+'</td>'
            else:
                optfinalstr += '<td style="padding: 20px;text-align: center;">'+attr+'</td>'
        optfinalstr+='</tr>\n'
    optfault = page_faults
    opthit = n - page_faults
    optratio = 100.0*opthit/n
        #print(temp)

           # print("\n%d ->" % (a[i]))
            # for j in range(m):
            #     if page[j] != FREE:
            #         print(page[j])
            #     else:
            #         print("-")
        # else:
        #     print("\n%d -> No Page Fault" % (a[i]))
            
    #print("\n Total page faults : %d." % (page_faults))

def fifo(sequence, frameAmt):
    global fifofinalList, fifofinalstr, fifofault, fifohit, fiforatio
    fifoallList = []
    sequenceList = sequence
    frames = []
    hit = 0
    miss = 0
    replaceIndex = 0
    temp = []
    #fifo algorithm
    for s in sequenceList:     
        if s in frames:
            hit += 1
            if 'red' in temp[replaceIndex - 1]: #removing old "red" value
                temp[replaceIndex - 1] = temp[replaceIndex - 1][3:]

        else:
            miss += 1
            if len(frames) == frameAmt:
                frames[replaceIndex] = s
                
            else:
                frames.append(s)
            temp = frames[:] #copying the list by value
            temp[replaceIndex] = 'red'+temp[replaceIndex] #adding "red" to the new value that is replaced
            #print(temp)
            replaceIndex = (replaceIndex + 1) % frameAmt
            
        
        fifoallList.append(temp[:])

    fifofinalList = transpose(fifoallList, frameAmt) #transpose for display on the screen
    #print(fifofinalList)


    fifofinalstr = ''
    
    #adding html tags
    for lists in fifofinalList:
        fifofinalstr += '<tr>'
        for attr in lists:
            if 'red' in attr:
                fifofinalstr += '<td style="padding: 20px;background-color:#f44336;text-align: center;">'+attr[3:]+'</td>'
            else:
                fifofinalstr += '<td style="padding: 20px;text-align: center;">'+attr+'</td>'
        fifofinalstr+='</tr>\n'
    fifofault = miss
    fifohit = hit
    fiforatio = 100.0*hit/(len(sequenceList))
    #print(markdown2.markdown(fifofinalstr))
    
    
        
                
    #print(f"---FIFO---\nHit: {hit}, Miss: {miss}")


def lru(sequence, frameAmt):
    global lrufinalList, lrufinalstr, lrufault, lruhit, lruratio
    sequenceList = sequence
    frames = []
    lruallList = []
    hit = 0
    miss = 0
    temp = []

    #lru algorithm
    for s in sequenceList:
        if s not in frames:
            miss += 1
            #temp1 = frames[:]
            if len(frames) == frameAmt:
                frames.remove(frames[0])
                frames.append(s)
                temp = frames[:]
                temp[-1] = 'red'+temp[-1]
                #temp[0], temp[-1] = temp[-1], temp[0]

            else:
                frames.append(s)
                temp = frames[:]
                temp[-1] = 'red'+temp[-1]
            
            
            
        
        else:
            hit += 1
            frames.remove(s)
            frames.append(s)
            temp = frames[:]
            #temp[0], temp[-1] = temp[-1], temp[0]
            

        lruallList.append(temp)
    lrufinalList = transpose(lruallList, frameAmt)

    #adding html tags
    lrufinalstr = ''
    for lists in lrufinalList:
        lrufinalstr += '<tr>'
        for attr in lists:
            if 'red' in attr:
                lrufinalstr += '<td style="padding: 20px;background-color:#f44336; text-align: center;">'+attr[3:]+'</td>'
            else:
                lrufinalstr += '<td style="padding: 20px; text-align: center;">'+attr+'</td>'
        lrufinalstr+='</tr>\n'
    lrufault = miss
    lruhit = hit
    lruratio = 100.0*hit/(len(sequenceList))

        
    #print(f"---LRU---\nHit: {hit}, Miss: {miss}")



def main(sequenceString, frameAmtString):
    global a, n, m
    sequenceList = sequenceString.split()
    frameAmount = int(frameAmtString)
    fifo(sequenceList, frameAmount)
    lru(sequenceList, frameAmount)
    #opt(sequenceList, frameAmount)

    #for optimal
    #a = [int(n) for n in sequenceString.split()]
    a = sequenceString.split()
    m = frameAmount
    n = len(a)
    __optimal()




class EntryForm(forms.Form):
    seq = forms.CharField(label=mark_safe("Sequence"))
    frames = forms.CharField(label=mark_safe("Frame Size"))
    #submit = forms.CharField(label="Submit")




# Create your views here.
def index(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        
        sequenceString = form.cleaned_data["seq"]
        frameAmtString = form.cleaned_data["frames"]
        #print("from forms", sequenceString, frameAmtString)
    return render(request, "replacement/index.html",
    {
        "form": EntryForm()
    })

def result(request):
    global fifofinalList, fifofinalstr,fifofault, fifohit, fiforatio
    global lrufinalList, lrufinalstr, lrufault, lruhit, lruratio
    global optfinalList, optfinalstr, optfault, opthit, optratio
    if request.method == "POST":
        
        # form = EntryForm(request.POST)
        # #val = request.POST['sTest'] 
        # #print(val)
        # if form.is_valid():
        #     sequenceString = form.cleaned_data["seq"]
        #     frameAmtString = form.cleaned_data["frames"] 
        #     main(sequenceString, frameAmtString)
        #print(finalList)
        sequenceString = request.POST["seq"]
        frameAmtString = request.POST["fsize"]
        main(sequenceString, frameAmtString)
        #print(sequenceString, frameAmtString)
        """
        for s in finalList:
            print(s)
        """
        #print(fifofinalList)
        return render(request, "replacement/result.html",{
            "form": EntryForm(),
            "sequence": sequenceString.split(),
            "frameAmount": frameAmtString,
            "fifofinalList": fifofinalList,
            "fifofinalstr": fifofinalstr,
            "fifomdstring": markdown2.markdown(fifofinalstr), #markdown for html
            "fifofault": fifofault,
            "fifohit": fifohit,
            "fiforatio": round(fiforatio,2),
            "length": len(sequenceString.split()),
            "lrufinalList": lrufinalList,
            "lrufinalstr": lrufinalstr,
            "lrumdstring": markdown2.markdown(lrufinalstr), #markdown for html
            "lrufault": lrufault,
            "lruhit": lruhit,
            "lruratio": round(lruratio,2),
            "optfinalList": optfinalList,
            "optfinalstr": optfinalstr,
            "optfault": optfault,
            "opthit": opthit,
            "optratio": round(optratio,2),
            "optmdstring": markdown2.markdown(optfinalstr), #markdown for html
        })
    return HttpResponse("resultpage")