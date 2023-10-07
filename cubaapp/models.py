from django.db import models
from django.contrib.auth.models import User


# Model for Formateur
class Formateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='formateur_images/')
    job = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    description = models.TextField()

    def __str__(self):
        return self.user.username
    
# Model for Tag
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
# Model for Formation
class Formation(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='formation_images/')
    formateur = models.ForeignKey(Formateur, on_delete=models.CASCADE)
    date = models.DateField()
    tags = models.ManyToManyField(Tag, blank=True)
    is_for_kids = models.BooleanField(default=False)  

    def __str__(self):
        return self.title
    
# Model for Etudiant
class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='etudiant_images/')
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    formations = models.ManyToManyField(Formation, blank=True)  
    def __str__(self):
        return self.user.username






    
# Model for Chapiter
class Chapiter(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    # Use either FileField for PDF/video uploads or URLField for external links
    file = models.FileField(upload_to='chapiter_files/')
    text = models.TextField(default="")
    # Example of using a URLField for external links
    # video_link = models.URLField()

    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.title

# Model for Question
class Question(models.Model):
    chapiter = models.ForeignKey(Chapiter, on_delete=models.CASCADE)
    question_text = models.TextField()
    difficulty = models.CharField(max_length=10, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ])

    def __str__(self):
        return self.question_text

# Model for ReponseOption (Response)
class ReponseOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reponse_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.reponse_text
    
class Reponse(models.Model):
    etudiant = models.ForeignKey('Etudiant', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    selected_option = models.ForeignKey('ReponseOption', on_delete=models.CASCADE)

    def __str__(self):
        return f"Response by {self.etudiant.user.username} to question: {self.question}"

class ChapiterResult(models.Model):
    chapiter = models.ForeignKey(Chapiter, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    # You can add additional fields as needed

    def __str__(self):
        return f"{self.etudiant} - Chapiter {self.chapiter.id} Result"

# Model for Comment
class Comment(models.Model):
    etudiant = models.ForeignKey('Etudiant', on_delete=models.CASCADE)
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.etudiant.user.username} on {self.formation.title}"
