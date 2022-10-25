from timeit import repeat
from django.shortcuts import render
from django.http import JsonResponse
from api.models import User, Course
from django.contrib import auth
from django.contrib.auth.decorators import login_required

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


@login_required
def profile(request):
    if request.method == 'GET':
        return render(request, 'profile.html')
    elif request.method == 'POST':
        try:
            username = request.user
            level = request.POST.get("level")
            skills = request.POST.get("skills")
            language = request.POST.get("language")
            profile = User.objects.get(username=username)
            profile.level = level
            profile.skills = skills
            profile.language = language
            profile.save()
            return JsonResponse({"msg": "Change successfully!"})
        except Exception as e:
            print(repr(e))
            return JsonResponse({"msg": repr(e)})


def course(request, course_id):
    if request.method == "GET":
        course_detail = getCourseDetail(int(course_id))
        return render(request, 'course.html', course_detail)
    # for test
    # course_details = getCourseDetails(course_id)
    # return JsonResponse({"msg": course_details})


@login_required
def recommendation(request):
    if request.method == "GET":
        username = request.user
        user = User.objects.get(username=username)
        reco_course_ids = user.reco_course_ids
        course_details = []
        for id in reco_course_ids:
            course_details.append(getCourseDetail(id))
        return render(request, 'recommendation.html', course_details)


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
    for id in course.reco_course_id:
        reco_course = {}
        course = Course.objects.get(course_id=id)
        reco_course["course_id"] = course.course_id
        reco_course["course_name"] = course.course_name
        reco_course["course_link"] = course.course_link
        reco_course["course_image"] = course.course_image
        reco_course_details.append(reco_course)
    course_detail["reco_course_details"] = reco_course_details
    return course_detail
