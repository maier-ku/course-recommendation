from ast import Not
from tqdm import tqdm
import torch
from sentence_transformers import SentenceTransformer, util
from timeit import repeat
from django.shortcuts import render
from django.http import JsonResponse
from api.models import User, Course
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import numpy as np


# Create your views here.


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == 'POST':
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            print(username, password)
            user_obj = auth.authenticate(username=username, password=password)
            if not user_obj:
                return JsonResponse({"status": 1, "msg":
                                     "Username does not exist or password is wrong!"})
            else:
                auth.login(request, user_obj)
                return JsonResponse({"status": 0, "msg": "Log in successfully!"})
        except Exception as e:
            print(repr(e))
            return JsonResponse({"status": 1, "msg": repr(e)})


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            repeat_password = request.POST.get("repeat_password")
            if password != repeat_password:
                return JsonResponse({"status": 1, "msg": "The two passwords do not match!"})
            print(username, password)
            User.objects.create_user(
                username=username, password=password)
            user_obj = auth.authenticate(username=username, password=password)
            auth.login(request, user_obj)
            return JsonResponse({"status": 0, "msg": "Register successfully!"})
        except Exception as e:
            print(repr(e))
            return JsonResponse({"status": 1, "msg": "Username has been registered!"})


def logout(request):
    auth.logout(request)
    return JsonResponse({"msg": "Log out successfully!"})


@login_required(login_url='/login/')
def profile(request):
    if request.method == 'GET':
        return render(request, 'profile.html')
    elif request.method == 'POST':
        try:
            username = request.user
            user_level = request.POST.get("level")
            user_skills = []
            for i in range(5):
                skill = request.POST.get("skills"+str(i+1))
                print(skill)
                if skill != "" and skill != None:
                    user_skills.append(skill)
            user_skills = ", ".join(user_skills)
            user_language = request.POST.get("language")
            user_university = request.POST.get("university")
            print(user_skills)
            reco_course_id = calculateSimilarity(
                user_university, user_level, user_language, user_skills)
            profile = User.objects.get(username=username)
            profile.level = user_level
            profile.skills = user_skills
            profile.language = user_language
            profile.reco_course_id = reco_course_id
            profile.save()
            return JsonResponse({"status": 0, "msg": "Save successfully!"})
        except Exception as e:
            print(repr(e))
            return JsonResponse({"status": 1, "msg": repr(e)})


def course(request, course_id):
    if request.method == "GET":
        course_detail = getCourseDetail(int(course_id))
        return render(request, 'course.html', course_detail)
    # for test
    # course_details = getCourseDetail(course_id)
    # return JsonResponse({"msg": course_details})


@login_required
def recommendation(request):
    if request.method == "GET":
        username = request.user
        user = User.objects.get(username=username)
        reco_course_id = user.reco_course_id.split(" ")
        course_details = []
        for id in reco_course_id:
            course_details.append(getCourseDetail(id))
        return render(request, 'recommendation.html', {"course_details": course_details})


def getCourseDetail(course_id):
    course = Course.objects.get(course_id=course_id)
    course_detail = {}
    course_detail["course_id"] = course.course_id
    course_detail["course_name"] = course.course_name
    course_detail["university_name"] = course.university_name
    course_detail["course_language"] = course.course_language
    course_detail["course_rating"] = course.course_rating
    course_detail["course_level"] = course.course_level
    course_detail["course_detail"] = course.course_detail
    course_detail["course_skills"] = course.course_skills
    course_detail["course_link"] = course.course_link
    course_detail["course_image"] = course.course_image
    reco_course_details = []
    reco_course_id = course.reco_course_id.split(" ")
    for id in reco_course_id:
        reco_course = {}
        course = Course.objects.get(course_id=int(id))
        reco_course["course_id"] = course.course_id
        reco_course["course_name"] = course.course_name
        reco_course["course_link"] = course.course_link
        reco_course["course_image"] = course.course_image
        reco_course["course_detail"] = course.course_detail
        reco_course_details.append(reco_course)
    course_detail["reco_course_details"] = reco_course_details
    return course_detail


def calculateSimilarity(user_university, user_level, user_language, user_skills):
    courses = Course.objects.all()
    similarity_list = np.zeros(len(courses))
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    corpus = list(courses.values_list("course_skills", flat=True))
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
    query = user_skills
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    cos_scores = cos_scores.cpu().detach().numpy()*0.6
    for i, course in enumerate(courses):
        if course.university_name == user_university:
            similarity_list[i] += 0.1
        if course.course_language == user_language:
            similarity_list[i] += 0.1
        if course.course_level == 'Beginner':
            if user_level == 'Beginner':
                similarity_list[i] += 0.1
            elif user_level == 'Intermediate':
                similarity_list[i] += 0.05
        if course.course_level == 'Intermediate':
            if user_level == 'Beginner':
                similarity_list[i] += 0.05
            elif user_level == 'Intermediate':
                similarity_list[i] += 0.1
            elif user_level == 'Advanced':
                similarity_list[i] += 0.05
        if course.course_level == 'Advanced':
            if user_level == 'Intermediate':
                similarity_list[i] += 0.05
            elif user_level == 'Advanced':
                similarity_list[i] += 0.1
        rating = course.course_rating
        if rating == 'Not Calibrated':
            similarity_list[i] += 0
        else:
            similarity_list[i] += (float(rating) - 4) * 0.1
    # for i in range(len(courses)):

    similarity_list += cos_scores
    # 反转数组，变成从大到小排序
    sorted_similarity_list = np.argsort(similarity_list)[::-1]
    topk = 10
    reco_course_id = sorted_similarity_list[0:topk]
    return " ".join(str(i) for i in reco_course_id)
