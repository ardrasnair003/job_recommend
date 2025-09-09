from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
import pickle
import pandas as pd
from nltk.corpus import wordnet
from django.contrib.auth.hashers import make_password


import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors


def home(request):
    return render(request, 'tem/index.html')


def register_admin(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mgn = Registration.objects.all()
        for w in mgn:
            if  w.user_role == 'user':
                messages.success(request, 'You are not allowed to be registered as admin')
                return redirect('register_admin')
        psw = request.POST.get('psw')
        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect("register_admin")
        user= User.objects.create_user(username = user_name, email = email, password=psw, first_name = first_name,last_name=last_name)
        user.save()
        reg = Registration()
        reg.password =psw
        reg.user_role ='admin'
        reg.user = user
        reg.save()
        messages.success(request, 'you have successfully registered as admin')
        return redirect('home')
    return render(request, 'reg_admin.html')


def register_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mgn = Registration.objects.all()
        for w in mgn:
            if  w.user.email == email and w.user_role == 'user':
                messages.success(request, 'You are not allowed to be registered as user')
                return redirect('register_user')
        psw = request.POST.get('psw')
        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect("register_user")
        user= User.objects.create_user(username = user_name, email = email, password=psw, first_name = first_name,last_name=last_name)
        user.save()
        reg = Registration()
        reg.password =psw
        reg.user_role ='user'
        reg.user = user
        reg.save()
        messages.success(request, 'you have successfully registered as user')
        return redirect('home')
    return render(request, 'reg_user.html')


def register_recruiter(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mgn = Registration.objects.all()
        for w in mgn:
            if  w.user.email == email and w.user_role == 'user':
                messages.success(request, 'You are not allowed to be registered as user')
                return redirect('register_recruiter')
        psw = request.POST.get('psw')
        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect("register_recruiter")
        user= User.objects.create_user(username = user_name, email = email, password=psw, first_name = first_name,last_name=last_name)
        user.save()
        reg = Registration()
        reg.password =psw
        reg.user_role ='recruiter'
        reg.user = user
        reg.save()
        messages.success(request, 'you have successfully registered as recruiter')
        return redirect('home')
    return render(request, 'reg_recruiter.html')


def update_pr_usr(request):
    bb = Registration.objects.get(id = request.session['logg'])
    rfy = bb.user.pk
    um = User.objects.get(id = rfy)
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pasw = request.POST.get('psw')
        user_name = request.POST.get('user_name')
        inp_skill = request.POST.get('inp_skill')
        m = User.objects.all().exclude(username = um.username)

        for t in m:
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('update_pr_usr')


        passwords = make_password(pasw)
        u = User.objects.get(id = rfy)
        u.password = passwords
        u.username = user_name
        u.email = email
        u.first_name = f_name
        u.last_name = l_name
        u.save()

        user = auth.authenticate(username = user_name, password = pasw)
        auth.login(request, user)


        b = bb.id
        m = int(b)
        request.session['logg'] = m

        bb.password = pasw
        bb.input_skill = inp_skill
        bb.user = u
        bb.save()
        messages.success(request, 'Updated successfully')
        return redirect('user_home')
    return render(request, 'update_pr_usr.html', {'bb': bb,'um':um})




def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')
        auth.login(request, user)
        if Registration.objects.filter(user = user).exists():
            logs = Registration.objects.filter(user = user)
            for value in logs:
                user_id = value.id
                usertype = value.user_role
                request.session['logg'] = user_id
                if usertype == 'admin':
                    return redirect('admin_home')
                elif usertype == 'user':
                    return redirect('user_home')
                elif usertype == 'recruiter':
                    return redirect('recruiter_home')
                else:
                    messages.error(request, 'Your access to the website is blocked. Please contact admin')
                    return redirect('login')
        messages.error(request, 'Username or password entered is incorrect')
        return redirect('login')
    return render(request, 'login.html')
     

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="home")
def admin_home(request):
    return render(request, 'admin_home.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="home")
def user_home(request):
    return render(request, 'user_home.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="home")
def recruiter_home(request):
    return render(request, 'recruiter_home.html')


def predict_job_usr(request):
    kmk = Registration.objects.get(id = request.session['logg'])
    if not kmk.input_skill:
        messages.success(request,'Please update profile with skills')
        return redirect('user_home')
    skill = str(kmk.input_skill)

    file_path = r"F:\DESKTOPP_FROM_21_08_2023\College_projects_django\UC_college\MACHINE_LEARNING\Ardra_S_nair\Job\air_qua\airq\Jobs - Jobs.csv"
    df = pd.read_csv(file_path)

    # Text preprocessing function
    def preprocess_text(df):
        """Preprocesses job descriptions by merging text fields and converting to lowercase."""
        df = df.copy()
        df[['title', 'description', 'skills_desc']] = df[['title', 'description', 'skills_desc']].astype(str)
        df['text'] = (df['title'] + ' ' + df['description'] + ' ' + df['skills_desc']).str.lower()
        return df

    # Preprocess data
    df = preprocess_text(df)

    # Load model, knn, and embeddings
    model_path = r"F:\DESKTOPP_FROM_21_08_2023\College_projects_django\UC_college\MACHINE_LEARNING\Ardra_S_nair\Job\air_qua\airq\job_recc_ardra.pkl"
    with open(model_path, "rb") as file:
        model, knn, job_embeddings = pickle.load(file)

    # Recommendation function
    def get_recommendations(job_input, df, model, knn, job_embeddings, num_recommendations=5,
                            similarity_threshold=0.35):
        """Retrieves job recommendations based on BERT embeddings and cosine similarity."""
        if df.empty or not job_input.strip():
            return [], 0, 0

        def expand_skills(skills):
            """Expands skills by finding synonyms using WordNet."""
            expanded_skills = set(skills.split())
            for word in skills.split():
                for syn in wordnet.synsets(word):
                    for lemma in syn.lemmas():
                        expanded_skills.add(lemma.name().replace('_', ' '))
            return ' '.join(expanded_skills)

        expanded_input = expand_skills(job_input.lower())
        input_embedding = model.encode([expanded_input], convert_to_numpy=True)
        distances, indices = knn.kneighbors(input_embedding)

        recommendations = []
        similarity_scores = 1 - distances[0]  # Convert distances to similarity scores

        filtered_indices_scores = [
            (i, round(similarity_scores[idx], 4))
            for idx, i in enumerate(indices[0])
            if similarity_scores[idx] > similarity_threshold
        ]

        for i, score in filtered_indices_scores[:num_recommendations]:
            job = df.iloc[i]
            recommendations.append({
                "title": job.get('title', 'N/A'),
                "company": job.get('company_id', 'N/A'),
                "location": job.get('location', 'N/A'),
                "description": job.get('description', 'N/A')[:500] + "...",
                "work_type": job.get('formatted_work_type', 'N/A'),
                "similarity_score": score
            })

        scores_only = [score for _, score in filtered_indices_scores]
        mean_similarity = round(np.mean(scores_only), 4) if scores_only else 0
        median_similarity = round(np.median(scores_only), 4) if scores_only else 0

        return recommendations, mean_similarity, median_similarity

    recommendations, mean_similarity, median_similarity = get_recommendations(skill, df, model, knn,
                                                                              job_embeddings)

    if recommendations:
        print("\n\033[1mTop Matching Jobs (Similarity > 35%):\033[0m")
        for idx, job in enumerate(recommendations, start=1):
            print(f"\n\033[1;34mJob {idx}:\033[0m")
            print("\033[1mTitle:\033[0m", job['title'])
            print("\033[1mCompany ID:\033[0m", job['company'])
            print("\033[1mLocation:\033[0m", job['location'])
            print("\033[1mWork Type:\033[0m", job['work_type'])
            print("\033[1mSimilarity Score:\033[0m", job['similarity_score'])
            print("\033[1mDescription:\033[0m", job['description'])

            hyh = Job_prediction()
            hyh.input_skill = skill
            hyh.rec_job_title = job['title']
            hyh.rec_company = job['company']
            hyh.rec_location = job['location']
            hyh.rec_work_type = job['work_type']
            hyh.rec_similarity_score = job['similarity_score']
            hyh.rec_description = job['description']
            hyh.prd_reg = kmk
            hyh.save()

        print(f"\n\033[1;32mMean Similarity Score:\033[0m {mean_similarity}")
        print(f"\n\033[1;33mMedian Similarity Score:\033[0m {median_similarity}")

        jyj = Job_prediction.objects.filter(prd_reg = kmk)
        return render(request, 'predict_job_usr.html',{'jyj':jyj})
    else:
        print("\n\033[1;31mNo matching jobs found with similarity > 35%.\033[0m")
        messages.success(request,'No recommendations predicted')
        return redirect('user_home')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="home")
def job_posts_recr(request):
    gtg = Job_post.objects.all()
    return render(request,'job_posts_recr.html',{'gtg':gtg})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="home")
def add_job_recr(request):
    if request.method == 'POST':
        jyj = Registration.objects.get(id = request.session['logg'])
        desg = request.POST.get('desg')
        city = request.POST.get('city')
        a_r = request.POST.get('a_r')
        skills = request.POST.get('skills')
        gh = Job_post()
        gh.designation = desg
        gh.city = city
        gh.age_range = a_r
        gh.skills_needed = skills
        gh.pst_reg = jyj
        gh.save()
        messages.success(request, 'Job added successfully')
        return redirect('job_posts_recr')
    return render(request,'add_job_recr.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="home")
def logout(request):
    auth.logout(request)
    return redirect('home')

        
