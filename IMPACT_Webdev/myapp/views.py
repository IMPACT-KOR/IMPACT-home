from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
import random

nextId = 4
topics = [
    {'id': 1, 'title': 'routing', 'body': 'Routing is...'},
    {'id': 2, 'title': 'view', 'body': 'View is...'},
    {'id': 3, 'title': 'Model', 'body': 'Model is...'}
]

def HTMLTemplate(articleTag, id=None):
    global topics
    contextUI = ''
    if id is not None:
        contextUI = f"""
            <li>
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>
            <li>
                <a href="/update/{id}">update</a>
            </li>
        """

    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    
    return f'''
    <html>
    <body>
        <h1><a href="/">Django</a></h1>
        <ol>
            {ol}    
        </ol>
        {articleTag}
        <ul>
            <li>>>> <a href="/homepage/">Move to homepage</a> <<<</li>
            <li><a href="/create/">Create</a></li>
            {contextUI}
        </ul>
        <hr>
        <ul>
            <li><a href="/investment/login/">Go to Investment</a></li>  <!-- Investment로 가는 링크 -->
            <li><a href="/guestbook/">Go to Guestbook</a></li>  <!-- Guestbook으로 가는 링크 추가 -->
        </ul>
    </body>
    </html>
    '''

# Create your views here.
def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello, Django. We're IMPACT_SITE_TEAM!
    This is DEV BRANCH!!!  <!-- 여기서 dev branch의 내용을 유지합니다 -->
    '''
    return HttpResponse(HTMLTemplate(article))

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
            break
    return HttpResponse(HTMLTemplate(article, id))

@csrf_exempt
def create(request):
    global nextId
    if request.method == "GET":
        article = '''
        <form action="/create/" method="post"> 
            <p><input type='text' name='title' placeholder='title'></p>
            <p><textarea name='body' placeholder='body'></textarea></p>
            <p><input type='submit'></p>
        </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {"id": nextId, "title": title, "body": body}
        topics.append(newTopic)
        nextId += 1
        return redirect(f'/read/{newTopic["id"]}')

@csrf_exempt
def update(request, id):
    global topics
    if request.method == 'GET':
        topic = next((topic for topic in topics if topic['id'] == int(id)), None)
        if topic:
            article = f'''
            <form action="/update/{id}" method="post">
                <p><input type='text' name='title' value='{topic["title"]}'></p>
                <p><textarea name='body'>{topic["body"]}</textarea></p>
                <p><input type='submit' value='Update'></p>
            </form>
            '''
            return HttpResponse(HTMLTemplate(article, id))
        else:
            return HttpResponse('Topic not found')
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body
                break
        return redirect(f'/read/{id}')

@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST['id']
        topics = [topic for topic in topics if topic['id'] != int(id)]
        return redirect('/')
    
def homepage_view(request):
    return render(request, "homepage/homepage.html")

def homepage_contact(request):
    return render(request, "homepage/contact.html")