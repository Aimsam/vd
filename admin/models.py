from django.db import models

# Create your models here.
class Node(models.Model):
    #id
    name = models.CharField(max_length = 50)
    
    class Meta:
        db_table = u'node'
    
    def __unicode__(self):
        return self.name    

class Author(models.Model):
    id = models.CharField(max_length = 50, primary_key = True)
    name = models.CharField(max_length = 50)
    weight = models.IntegerField(default=1)
    description = models.CharField(max_length = 255, blank = True)
    avatar = models.CharField(max_length = 255, blank = True)    
    love = models.IntegerField(blank = True, default = 1)
    click = models.IntegerField(blank = True, default = 1)
    type = models.IntegerField(blank = True, default = 1)
    node = models.ForeignKey(Node)

    class Meta:
        db_table = u'author'    

    def __unicode__(self):
        return self.name
      

class Tag(models.Model):
    name = models.CharField(max_length = 50)    
    
    class Meta:
        db_table = u'tag'    

    def __unicode__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.name

class Video(models.Model):
    id = models.CharField(max_length = 50, primary_key = True)
    author = models.ForeignKey(Author)
    user = models.ForeignKey(User, blank = True, default = 1)
    node = models.ForeignKey(Node)
    tags = models.ManyToManyField(Tag, blank = True)
    title = models.CharField(max_length = 255, blank = True)
    thumbnail = models.CharField(max_length = 255, blank = True)
    thumbnail_2 = models.CharField(max_length = 255, blank = True)
    quality = models.CharField(max_length = 10, blank = True)
    duration = models.CharField(max_length = 10, blank = True)
    published = models.DateTimeField()
    description = models.TextField(blank = True)
    remarks = models.TextField(blank = True)
    type = models.IntegerField(blank = True, default = 1)
    love = models.IntegerField(blank = True, default = 1)
    click = models.IntegerField(blank = True, default = 1)

    class Meta:
        db_table = u'video'

    def __unicode__(self):
        return u'%s %s' % (self.id, self.title)



