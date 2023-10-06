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
    return render(request,'pages/courses/index.html',context)
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
        return redirect('email_application',id=chapiter.id) 
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
    context = {}
    return render(request,"pages/default/index.html",context)


@login_required(login_url="/login_home")
def indexl(request):
    context = {}
    redirect('index')


@login_required(login_url="/login_home")
def courseanalyse(request):
    context = {}
    return render(request,"pages/user-cards/user-cards.html",context)
    
