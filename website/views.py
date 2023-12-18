from django.shortcuts import render,redirect
from django.contrib import messages
import openai
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import SignUpForm
from .models import Code
from django.http import JsonResponse

#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
# Create your views here.
def home(request):
    our_list=[ 'basic', 'c', 'clike', 'cobol', 'coffeescript', 'cpp','csharp', 'cshtml', 'css', 'csv', 'dart', 'git', 'go', 'html', 'java', 'javascript', 'json', 'kotlin', 'markup-templating', 'matlab', 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'rust', 'sass', 'scala', 'solidity', 'sql', 'swift', 
'typescript', 'vbnet']
    if request.method=='POST':
       
        code=request.POST['code']
        lang=request.POST['lang']
        #check to make sure they pick a language
        if lang =="Select Programming Language":
            messages.success(request,"Hey!! You forgot to select a programming language")
            return render(request,'home.html',{'our_list':our_list,'code':code,'lang':lang})
        else:
            openai.api_key="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"
            #create openai instance 
            openai.Model.list()
            #make an openapi request
            try:
                response=openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=f"Respond only with  code. Fix this {lang} code:{code}",
                    temperature=0,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
            )
                #PArse the response 
                response=(response["choices"][0]["text"]).strip()
                # Save To Database
                record = Code(question=code, code_answer=response, language=lang, user=request.user)
                record.save()
               

                return render(request,'home.html',{'our_list':our_list,'response':response,'lang':lang})
            except Exception as e:
                return render(request,'home.html',{'our_list':our_list,'code':e,'lang':lang})

        
    

    return render(request,'home.html',{'our_list':our_list})
            
        
        #openai!!
def suggest(request):
    our_list=[ 'basic', 'c', 'clike', 'cobol', 'coffeescript', 'cpp','csharp', 'cshtml', 'css', 'csv', 'dart', 'git', 'go', 'html', 'java', 'javascript', 'json', 'kotlin', 'markup-templating', 'matlab', 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'rust', 'sass', 'scala', 'solidity', 'sql', 'swift', 
'typescript', 'vbnet']
    if request.method=='POST':
        code=request.POST['code']
        lang=request.POST['lang']
        #check to make sure they pick a language
        if lang =="Select Programming Language":
            messages.success(request,"Hey!! You forgot to select a programming language")
            return render(request,'suggest.html',{'our_list':our_list,'code':code,'lang':lang})
        else:
            openai.api_key="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"
            #create openai instance 
            openai.Model.list()
            #make an openapi request
            try:
                response=openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=f"Respond only with  code.{code}",
                    temperature=0,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
            )
                #PArse the response 
                response=(response["choices"][0]["text"]).strip()
                # Save To Database
                record = Code(question=code, code_answer=response, language=lang, user=request.user)
                record.save()
                
                
                return render(request,'suggest.html',{'our_list':our_list,'response':response,'lang':lang})
            except Exception as e:
                return render(request,'suggest.html',{'our_list':our_list,'code':e,'lang':lang})

        
    

    return render(request,'suggest.html',{'our_list':our_list})
def login_user(request):
    if request.method=="POST":
        username=request.POST['username']
        password= request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have been logged in!!")
            return redirect('home')
        else:
            messages.success(request,"Error Logginng In. Please Try Again...")
            return redirect('home')
    else:
         return render(request,'home.html',{})
def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out...")
    return redirect('home')
def register_user(request):
    if request.method =='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"You have been registered!!")
        return redirect('home')
    else:
        form=SignUpForm
    return render(request,'register.html',{'form':form})
def past(request):
    if request.user.is_authenticated:
         code=Code.objects.filter(user_id=request.user.id)
         return render(request,'past.html',{"code":code})
    else:
        messages.success(request,"You MUST be logged in to view this page")
        return redirect('home')

   
    
def delete_past(request, Past_id):
	past = Code.objects.get(pk=Past_id)
	past.delete()
	messages.success(request, "Deleted Successfully...")
	return redirect('past')

# to run the code

import requests

def run_code(code, language_id):
    url = "https://api.judge0.com/submissions/"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": "YOUR_API_KEY",  # Replace with your Judge0 API key
    }

    data = {
        "source_code": code,
        "language_id": language_id,
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        submission_token = response.json()["token"]
        return get_submission_result(submission_token)
    else:
        return {"error": f"Failed to submit code. Status code: {response.status_code}"}


def get_submission_result(submission_token):
    url = f"https://api.judge0.com/submissions/{submission_token}"
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return {"error": f"Failed to get submission result. Status code: {response.status_code}"}

def execute_code(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        language_id = request.POST.get('language_id', '')

        if code and language_id:
            result = run_code(code, language_id)
            return JsonResponse(result)
        else:
            return JsonResponse({"error": "Code and language_id are required."})

    return JsonResponse({"error": "Invalid request method."})