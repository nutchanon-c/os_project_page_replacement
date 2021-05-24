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

global fifofinalList, fifofinalstr, fifofault, fifohit, fiforatio
global lrufinalList, lrufinalstr, lrufault, lruhit, lruratio



def transpose(l1, num):
    for i in l1:
        while(len(i) < num):
            i.append("-")      



    l2 = list(zip(*l1))
    #print(l1)
    #print(l2)
    return l2


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
                fifofinalstr += '<td style="padding: 7px;color:red;">'+attr[3:]+'</td>'
            else:
                fifofinalstr += '<td style="padding: 7px;">'+attr+'</td>'
        fifofinalstr+='</tr>\n'
    fifofault = miss
    fifohit = hit
    fiforatio = 100.0*hit/(len(sequenceList))
    
    
        
                
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
            temp1 = frames[:]
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
                lrufinalstr += '<td style="padding: 7px;color:red;">'+attr[3:]+'</td>'
            else:
                lrufinalstr += '<td style="padding: 7px;">'+attr+'</td>'
        lrufinalstr+='</tr>\n'
    lrufault = miss
    lruhit = hit
    lruratio = 100.0*hit/(len(sequenceList))

        
    #print(f"---LRU---\nHit: {hit}, Miss: {miss}")


def opt(sequence, frameAmt):
    return

def main(sequenceString, frameAmtString):
    sequenceList = sequenceString.split()
    frameAmount = int(frameAmtString)
    fifo(sequenceList, frameAmount)
    lru(sequenceList, frameAmount)
    opt(sequenceList, frameAmount)


class EntryForm(forms.Form):
    seq = forms.CharField(label=mark_safe("Sequence"))
    frames = forms.CharField(label=mark_safe("<br/><br/>Number of Frames"))
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
    global finalList, finalstr,fifofault, fifohit, fiforatio
    global lrufinalList, lrufinalstr, lrufault, lruhit, lruratio
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            sequenceString = form.cleaned_data["seq"]
            frameAmtString = form.cleaned_data["frames"] 
            main(sequenceString, frameAmtString)
        #print(finalList)
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
        })
    return HttpResponse("resultpage")