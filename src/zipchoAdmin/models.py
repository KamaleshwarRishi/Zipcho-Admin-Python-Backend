from django.db import models

class gender(models.Model):
    gender = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.gender)

class interest(models.Model):
    interest = models.CharField(max_length=100)

    def __str__(self):
        return str(self.interest)

class category(models.Model):
    interest = models.ForeignKey(interest, on_delete=models.PROTECT)
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.category)

class language(models.Model):
    language = models.CharField(max_length=150)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.language)

class country(models.Model):
    country = models.CharField(max_length=150)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.country)
