from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages  
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.models import User,auth

from .forms import *
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.db.models import Count
from .models import *
from django.db.models.functions import Now
from datetime import datetime  # Import the datetime module
# Create your views here.
import openai
import json
import fitz  
import os
import sys
from django.http import JsonResponse

openai.api_key = "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"

def calculate_and_save_quiz_result(etudiant, chapiter):
    # Get all questions for the chapiter
    questions = chapiter.question_set.all()

    # Calculate the total number of questions and correct responses
    total_questions = questions.count()
    correct_responses = Reponse.objects.filter(etudiant=etudiant, question__in=questions, selected_option__is_correct=True).count()

    # Calculate the score as a percentage
    if total_questions > 0:
        score_percentage = (correct_responses / total_questions) * 100
    else:
        score_percentage = 0

    # Round the score to an integer
    score = round(score_percentage)

    # Create or update the ChapiterResult for this chapiter and etudiant
    chapiter_result, created = ChapiterResult.objects.get_or_create(chapiter=chapiter, etudiant=etudiant)
    chapiter_result.score = score
    chapiter_result.save()

    return score


import json
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        user_message = data.get('message', '')
        #here you load chapitre, extractih text nd send it here.
        chapitre = "La programmation est donc l’art de commander à un ordinateur de faire exactement ce que vous voulez, et Python compte pa    rmi les langages qu’il est capable de comprendre pour recevoir vos ordres. Nous allons essayer cela tout de suite avec des ordres très si    mples concernant des nombres, puisque les nombres constituent son matériau de prédilection. Nous allons lui fournir nos premières « instr    uctions », et préciser au passage la définition de quelques termes essentiels du vocabulaire informatique, que vous rencontrerez constamm    ent dans la suite de cet ouvrage.Comme nous l’avons expliqué dans la préface (voir : Versions du langage, page XII), nous avons pris le p    arti d’utiliser dans ce cours la nouvelle version 3 de Python, laquelle a introduit quelques changements syntaxiques par rapport aux vers    ions précédentes. Dans la mesure du possible, nous vous indiquerons ces différences dans le texte, afin que vous puissiez sans problème a    nalyser ou utiliser d’anciens programmes écrits pour Python 1 ou 2"
        question = user_message
        result_string = openai.ChatCompletion.create(model="gpt-3.5-turbo",
        messages=[{"role":"user","content": "#context:chapitre : {}, answer this question {}".format(chapitre, question)}]) 
        print(result_string.choices[0].message.content)

        # Return the result as JSON
        return JsonResponse({'data': result_string.choices[0].message.content})
    else:
        return JsonResponse({'data': 'Invalid request method'})
    
@login_required(login_url="/login_home")
def learning_list(request):
    formations = Formation.objects.all()
    all_tags = Tag.objects.annotate(num_formations=Count('formation'))
    upcoming_formations = Formation.objects.filter(date__gte=Now()).order_by('date')[:3]
    
    context = {
        'upcoming_formations':upcoming_formations,
        'formations': formations,
        'all_tags':all_tags,
    }   
    return render(request,'pages/courses/index.html',context)

@login_required(login_url="/login_home")
def mescourses(request):
    etudiant = Etudiant.objects.get(user=request.user)

    formations = etudiant.formations.all()  
    all_tags = Tag.objects.annotate(num_formations=Count('formation'))
    upcoming_formations = Formation.objects.filter(date__gte=Now()).order_by('date')[:3]
    
    context = {
        'upcoming_formations':upcoming_formations,
        'formations': formations,
        'all_tags':all_tags,
    }   
    return render(request,'pages/courses/index.html',context)

@login_required(login_url="/login_home")
def mycourses(request):
    formateur = Formateur.objects.get(user=request.user)

    formations = Formation.objects.filter(formateur=formateur)  
    all_tags = Tag.objects.annotate(num_formations=Count('formation'))
    upcoming_formations = Formation.objects.filter(date__gte=Now()).order_by('date')[:3]
    
    context = {
        'upcoming_formations':upcoming_formations,
        'formations': formations,
        'all_tags':all_tags,
    }   
    return render(request,'pages/courses/index2.html',context)
@login_required(login_url="/login_home")
def email_application(request,id):
    formation = get_object_or_404(Formation, id=id)
    chapiters = formation.chapiter_set.all()
    etudiant = Etudiant.objects.get(user=request.user)
    etudiant_results = ChapiterResult.objects.filter(etudiant=etudiant, chapiter__in=chapiters)

    chapiter_scores = {}

    for result in etudiant_results:
        chapiter_scores[result.chapiter.id] = result.score

    context = {
        'formation': formation,
        'chapiter_scores': chapiter_scores,
    }
    return render(request,"pages/course/index.html",context)


     
@login_required(login_url="/login_home")
def quiz(request,id,chapiter):
    if request.method == "POST":
        etudiant = Etudiant.objects.get(user=request.user)
        # Process the form submission
        chapiter = Chapiter.objects.get(id=chapiter)
        for question in chapiter.question_set.all():
            print(f'rdo-ani{question.id}-{chapiter.id}')
            response_id = request.POST.get(f'rdo-ani{question.id}-{chapiter.id}')
            print(response_id)
            if response_id:
                selected_response = ReponseOption.objects.get(id=response_id)
                print(selected_response)
                Reponse.objects.create(
                    etudiant=etudiant,
                    question=question,
                    selected_option=selected_response
                )

        calculate_and_save_quiz_result(etudiant, chapiter)
        return redirect('email_application',id=chapiter.formation.id) 
    formation = get_object_or_404(Formation, id=id)
    chapiter = get_object_or_404(Chapiter,id=chapiter)
    context = {
        'formation': formation,
        'chapiter':chapiter
    }
    return render(request,"pages/course/index2.html",context)


@login_required(login_url="/login_home")
def result(request,id,chapiter):
    formation = get_object_or_404(Formation, id=id)
    chapiter = get_object_or_404(Chapiter, id=chapiter)
    etudiant = request.user.etudiant  # Assuming you have a OneToOneField relationship between User and Etudiant

    questions = chapiter.question_set.all()

    # Create a dictionary to store information about each question
    question_info = []

    for question in questions:
        response = Reponse.objects.filter(etudiant=etudiant, question=question).first()

        question_data = {
            'question_text': question.question_text,
            'choices': question.reponseoption_set.all(),
            'correct_answer': None,
            'user_response': None,
        }

        # Get the correct answer
        correct_answer = question.reponseoption_set.filter(is_correct=True).first()
        if correct_answer:
            question_data['correct_answer'] = correct_answer.reponse_text

        # Get the user's response
        if response:
            question_data['user_response'] = response.selected_option.reponse_text

        question_info.append(question_data)

    context = {
        'formation': formation,
        'chapiter': chapiter,
        'question_info': question_info,
    }

    return render(request, "pages/course/index3.html", context)


@login_required(login_url="/login_home")
def results(request,id,chapiter):
    formation = get_object_or_404(Formation, id=id)
    chapiter = get_object_or_404(Chapiter, id=chapiter)

    questions = chapiter.question_set.all()

    context = {
        'formation': formation,
        'chapiter': chapiter,
        'question_info': questions,
    }

    return render(request, "pages/details/index4.html", context)


@login_required(login_url="/login_home")
def addcourse(request):
    if request.method == 'POST':
        # Get the form data directly from the request
        title = request.POST['title']
        file = request.FILES['file']
        date = request.POST['date']
        tags_ids = request.POST.getlist('tags')
        is_for_kids = 'kids' in request.POST  # Check if the 'kids' checkbox is selected
        try:
            input_date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
        except ValueError:
            # Handle invalid date format here if needed
            pass
        # Create a new Formation object
        formateur = Formateur.objects.get(user=request.user)
        new_formation = Formation(
            title=title,
            image=file,
            date=input_date,
            is_for_kids=is_for_kids,
            formateur=formateur
        )
        new_formation.save()

        # Add tags to the new Formation object
        tags = Tag.objects.filter(id__in=tags_ids)
        new_formation.tags.set(tags)

        return redirect('mycourses')
    tags = Tag.objects.all()
    context = {
        'tags':tags
    }   
    return render(request,'pages/course/addcourse.html',context)

def login_home(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
       
        if form.is_valid():
       
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                if 'next' in request.GET:
                    nextPage = request.GET['next']
                    return HttpResponseRedirect(nextPage)
                return redirect("index")
            else:
                messages.error(request,"Wrong credentials")
                return redirect("login_home")
        else:
            messages.error(request,"Wrong credentials")
            return redirect("login_home")

    else:
        form =AuthenticationForm()

       
    return render(request,'main-login.html',{"form":form,})


def logout_view(request):
    logout(request)
    return redirect('login_home')



def signup_home(request):
    if request.method=='GET':
        return render(request,'signup.html') 
    else:
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        phone=request.POST['phone']
        birth=request.POST['birth']
        user=User.objects.filter(email=email).exists()
        if user:  
            raise Exception('Something went wrong')
        new_user=User.objects.create_user(username=username,email=email,password=password)
        new_user.save()
        Etudiant.objects.create(user=new_user,phone=phone,date_of_birth=birth)
        return redirect('index')
        

@login_required(login_url="/login_home")
def index(request):
    try:
        etudiant = request.user.etudiant  
        return redirect('learning_list')
    except Etudiant.DoesNotExist:
        pass
    context = {}
    return render(request,"pages/default/index.html",context)


@login_required(login_url="/login_home")
def indexl(request):
    context = {}
    return redirect('index')


@login_required(login_url="/login_home")
def courseanalyse(request):
    context = {}
    return render(request,"pages/user-cards/user-cards.html",context)
    
@login_required(login_url="/login_home")
def analyse(request,id):
    tags = Chapiter.objects.filter(formation_id=id)
    formation = Formation.objects.get(id=id)
    context = {
        'all_tags':tags,
        'formation':formation
    }
    return render(request,"pages/analyse/index.html",context)


def summarize(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        text_content = file.read()
        result = openai.ChatCompletion.create(model="gpt-3.5-turbo",
        messages=[{"role":"user","content": " summarize this lesson. output language must be the same as input language. text input: : {} ".format(text_content)}])
        # print(result.choices[0].message.content)

    return result.choices[0].message.content  


@login_required(login_url="/login_home")
def details(request,id):
    tags = Chapiter.objects.filter(formation_id=id)
    formation = Formation.objects.get(id=id)

    if request.method == 'POST':
        # Get the data from the request
        title = request.POST.get('title')
        file = request.FILES.get('file')

        # Create a new Chapiter instance and associate it with the Formation
        chapiter = Chapiter(formation=formation, title=title, file=file,is_active=True)
        chapiter.save()

        pdf_file = os.getcwd()+"/media/"+str(chapiter.file)

        # Create an "extracted" folder if it doesn't exist
        output_folder = f"extracted\\{sys.argv[1]}"
        os.makedirs(output_folder, exist_ok=True)

        # Initialize a PDF document object
        pdf_document = fitz.open(pdf_file)
        metadata = pdf_document.metadata
        file_name = metadata.get("Title", "Unknown")
        # Create a text file to store the extracted text
        text_filename = f"{file_name}_extracted_text.txt"
        text_file = open(text_filename, "w", encoding="utf-8")

        # Loop through each page in the PDF
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]

            # Get the images on the page as a list of image objects
            images = page.get_images(full=True)

            for img_index, img_info in enumerate(images):
                xref = img_info[0]
                base_image = pdf_document.extract_image(xref)
                image_data = base_image["image"]

                # Generate a filename with the page name and image number
                image_filename = os.path.join(output_folder, f"page{page_number+1}_image{img_index+1}.jpg")
                with open(image_filename, "wb") as img_file:
                    img_file.write(image_data)

            # Extract text from the page and write it to the text file
            page_text = page.get_text("text")
            text_file.write(page_text)
            text_file.write("\n\n")  # Add some separation between pages

            context = page_text
        # Close the text file
        text_file.close()

        # Close the PDF document
        pdf_document.close()
        openai.api_key = "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"
        #context = ""  # Ajouter le contenu de cette partie
        result = openai.ChatCompletion.create(model="gpt-3.5-turbo",
            messages=[{"role":"user","content": "Generate for us a high quality SCQ with maximum of questions in json form (question, responses, correct_resp_index). The MCQ language must be the same as the content language. content :{} ".format(context)}])


        input = json.loads(result.choices[0].message.content)
        if type(input) != list:
            input = input[list(input.keys())[0]]

            #input contains the array of json

        for entry in input:
            question = entry['question']
            ques = Question.objects.create(chapiter=chapiter,question_text=question,difficulty='medium')
            responses = entry['responses']
            correct_index = entry['correct_resp_index']

            for i,rep in enumerate(responses):
                option = ReponseOption.objects.create(question=ques,reponse_text=rep)
                if i == correct_index:
                    option.is_correct = True 
                    option.save()

        chapiter.text = summarize(text_filename)
        chapiter.save()


    context = {
        'all_tags':tags,
        'formation':formation
    }
    return render(request,"pages/details/index.html",context)


@login_required(login_url="/login_home")
def user(request,id):
    context = { }
    return render(request,"pages/social/social.html",context)
