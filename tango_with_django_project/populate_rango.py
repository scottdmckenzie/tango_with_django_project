import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django 
django.setup()
from rango.models import Category, Page

def populate():

    python_pages = [
        {'title': 'Official Python Tutorial',
        'url':'http://docs.python.org/3/tutorial/', 'views':10},
        {'title':'How to Think like a Computer Scientist',
        'url':'http://www.greenteapress.com/thinkpython/','views':1},
        {'title':'Learn Python in 10 Minutes',
        'url':'http://www.korokithakis.net/tutorials/python/','views':2} 
    ]

    

    django_pages = [
        {'title':'Official Django Tutorial',
         'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/','views':3},
        {'title':'Django Rocks', 'url':'http://www.djangorocks.com/','views':4},
        {'title':'How to Tango with Django', 'url':'http://www.tangowithdjango.com/','views':5}
    ]

    other_pages = [
        {'title':'Bottle', 'url':'http://bottlepy.org/docs/dev/','views':6},
        {'title':'Flask', 'url':'http://flask.pocoo.org','views':7} 
    ]

    cats = {
        'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
        'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
        'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16} 
    }

    django_cat = add_cat('Django', 64, 32)

    for page_info in python_pages:
        add_page(category=django_cat, title=page_info["title"], url=page_info["url"], views=page_info["views"])

    for cat, cat_data in cats.items():
        c = add_cat(cat, views = cat_data['views'], likes = cat_data['likes'])
        for p in cat_data['pages']: 
            add_page(c, p['title'], p['url'])
        
    for c in Category.objects.all():
        for p in Page.objects.filter(category = c):
            print(f' - {c}: {p}')
    
    printed_categories = set()
    printed_pages = set()

    for c in Category.objects.all():
        if c.id not in printed_categories:
            printed_categories.add(c.id)
            for p in Page.objects.filter(category=c, views__gt=0):
                if p.id not in printed_pages:
                    printed_pages.add(p.id)
                    print(f' - {c}: {p.title} - Views: {p.views}')
    
def add_cat(name, views = 0, likes = 0): 
    c = Category.objects.get_or_create(name = name, views = views, likes = likes)[0]
    c.save()
    return c

def add_page(category, title, url, views=0):
    if views <= 0:
        views = 1 
    page = Page.objects.get_or_create(category=category, title=title)[0]
    page.url = url
    page.views = views
    page.save()
    return page

if __name__ == '__main__':
    print('Starting Rango population script... ')
    populate()