from typing import Sequence
from django.shortcuts import render
from django.http import HttpResponse
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
import secrets
from django.utils.safestring import mark_safe


def fifo(sequence, frameAmt):
    sequenceList = sequence
    frames = []
    hit = 0
    miss = 0
    replaceIndex = 0
    for s in sequenceList:     
        if s in frames:
            hit += 1
        else:
            miss += 1
            if len(frames) == frameAmt:
                frames[replaceIndex] = s
                
            else:
                frames.append(s)
            replaceIndex = (replaceIndex + 1) % frameAmt
                
    print(f"---FIFO---\nHit: {hit}, Miss: {miss}")


def lru(sequence, frameAmt):
    sequenceList = sequence
    frames = []
    hit = 0
    miss = 0
    for s in sequenceList:
        if s not in frames:
            miss += 1
            if len(frames) == frameAmt:
                frames.remove(frames[0])
                frames.append(s)
            else:
                frames.append(s)
        
        else:
            hit += 1
            frames.remove(s)
            frames.append(s)    
        
    print(f"---LRU---\nHit: {hit}, Miss: {miss}")


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
        print("from forms", sequenceString, frameAmtString)
    return render(request, "replacement/index.html",
    {
        "form": EntryForm()
    })

def result(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            sequenceString = form.cleaned_data["seq"]
            frameAmtString = form.cleaned_data["frames"] 
            main(sequenceString, frameAmtString)
        return render(request, "replacement/result.html",{
            "form": EntryForm(),
            "sequence": sequenceString,
        })
    return HttpResponse("resultpage")