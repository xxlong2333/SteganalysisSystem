import random
import re

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.shortcuts import *
from utils.getChartData import *
from utils.getPublicData import *
from myApp.models import *
from recommend.goRecommend import *
from predict.goPredict import *
from django.core.paginator import Paginator
import json
import numpy as np
from PIL import Image
import torch
from torchvision import transforms
from .steganalysis.model import SteganNet  # 假设您的模型在这个位置

# Create your views here.


def home(request):
    if request.method == 'GET':
        return render(request, 'index.html', {
        })

def index(request):
    return render(request, 'index.html')

def login(request):

    if request.method == 'GET':
        return render(request, 'login.html', {
        })
    else:
        return HttpResponseRedirect('/myApp/home/')
        # username = request.POST['username']
        # password = request.POST['password']
        # print(username, password)
        # try:
        #     user = User.objects.get(username=username, password=password)
        #     request.session['username'] = username
        #     return HttpResponseRedirect('/myApp/home/')
        # except:
        #     messages.error(request,'请输入正确的用户名和密码')
        #     return HttpResponseRedirect('/myApp/login/')
        # return render(request, 'login.html', {})

#
# def salaryChar(request):
#     if request.method == 'GET':
#         uname = request.session.get('username')
#         userInfo = User.objects.get(username=uname)
#         typeSalaryList = list(gettypeSalary())
#         typeSalaryX = [x[0] for x in typeSalaryList]
#
#         # 其他类似处理
#         typeSalaryY1 = [0 if x is None else x for x in typeSalaryList[0][1:]]
#         typeSalaryY2 = [0 if x is None else x for x in typeSalaryList[1][1:]]
#         typeSalaryY3 = [0 if x is None else x for x in typeSalaryList[2][1:]]
#         typeSalaryY4 = [0 if x is None else x for x in typeSalaryList[3][1:]]
#         typeSalaryY5 = [0 if x is None else x for x in typeSalaryList[4][1:]]
#         typeSalaryY6 = [0 if x is None else x for x in typeSalaryList[5][1:]]
#         typeSalaryY7 = [0 if x is None else x for x in typeSalaryList[6][1:]]
#         typeSalaryY8 = [0 if x is None else x for x in typeSalaryList[7][1:]]
#         typeSalaryY9 = [0 if x is None else x for x in typeSalaryList[8][1:]]
#
#         # averageTypeList = list(getaverageType())
#         # averageTypeData = []
#         # for i in averageTypeList:
#         #     averageTypeData.append({
#         #         'name':i[0],
#         #         'value':float(round(i[1], 1))
#         #     })
#         # print(averageTypeData)
#
#         return render(request, 'index.html', {
#             'userInfo': userInfo,
#             'typeSalaryX': typeSalaryX,
#             'typeSalaryY1': typeSalaryY1,
#             'typeSalaryY2': typeSalaryY2,
#             'typeSalaryY3': typeSalaryY3,
#             'typeSalaryY4': typeSalaryY4,
#             'typeSalaryY5': typeSalaryY5,
#             'typeSalaryY6': typeSalaryY6,
#             'typeSalaryY7': typeSalaryY7,
#             'typeSalaryY8': typeSalaryY8,
#             'typeSalaryY9': typeSalaryY9,
#             # 'averageTypeData': averageTypeData
#         })
#
#
# def educationChar(request):
#     if request.method == 'GET':
#         uname = request.session.get('username')
#         userInfo = User.objects.get(username=uname)
#
#         averageExperienceList = list(getaverageExperience())
#         averageExperienceX = [x[0] for x in averageExperienceList]
#         averageExperienceY1 = [round(x[1], 1) for x in averageExperienceList]
#         averageExperienceY2 = [x[2] for x in averageExperienceList]
#         print(averageExperienceX, averageExperienceY1, averageExperienceY2)
#
#         educationCountList = list(geteducationCount())
#         educationData = []
#         for i in educationCountList:
#             educationData.append({
#                 'name': i[0],
#                 'value':i[1],
#                 'unit':'人'
#             })
#
#         return render(request, 'educationChar.html', {
#             'userInfo': userInfo,
#             'averageExperienceX': averageExperienceX,
#             'averageExperienceY1': averageExperienceY1,
#             'averageExperienceY2': averageExperienceY2,
#             'educationData': educationData
#
#         })
#
#
#
# def industryChar(request):
#     if request.method == 'GET':
#         uname = request.session.get('username')
#         userInfo = User.objects.get(username=uname)
#
#         typeCountList = list(gettypeCount())
#         typeCountX = [x[0] for x in typeCountList]
#         typeCountY = [x[1] for x in typeCountList]
#
#         typeMaxList = list(gettypeMax())
#         typeMaxData = []
#         for i in typeMaxList:
#             typeMaxData.append({
#                 'name': i[0],
#                 'value':i[1],
#             })
#
#         print(typeMaxData, typeCountX, typeCountY)
#
#         return render(request, 'industryChar.html', {
#             'userInfo': userInfo,
#             'typeCountX': typeCountX,
#             'typeCountY': typeCountY,
#             'typeMaxData': typeMaxData,
#         })
#
#
# def cityChar(request):
#     if request.method == 'GET':
#         uname = request.session.get('username')
#         userInfo = User.objects.get(username=uname)
#
#         citySalaryList = list(getcitySalary())
#         cityPeopleList = list(getcityPeople())
#         selectList = [x[0] for x in citySalaryList]
#         defaultCity = request.GET.get('city') or '广州'
#         print(defaultCity)
#         print(selectList)
#
#         citySalaryX=['0-5000','5000-7000','7000-10000','10000-20000','20000以上',]
#         # 执行查询
#         citySalaryY = list(query_hive('select * from citySalary where city=%s', [defaultCity], 'select')[0])[1:]
#         # 将 None 值替换为 0
#         citySalaryY = [0 if item is None else item for item in citySalaryY]
#
#         cityPeopleData = list(query_hive('select * from cityPeople where city=%s', [defaultCity], 'select')[0])[1:]
#         cityPeopleData = [ 0 if item is None else item for item in cityPeopleData]
#         cityPeopleReal =[
#             {
#                 'name': '0-10人',
#                 'value': cityPeopleData[0],
#             },
#             {
#                 'name': '10-50人',
#                 'value': cityPeopleData[1],
#             },
#             {
#                 'name': '50-150人',
#                 'value': cityPeopleData[2],
#             },
#             {
#                 'name': '150-500人',
#                 'value': cityPeopleData[3],
#             },
#             {
#                 'name': '500-1000人',
#                 'value': cityPeopleData[4],
#             },
#             {
#                 'name': '1000人以上',
#                 'value': cityPeopleData[5],
#             }
#         ]
#
#         print(cityPeopleReal,citySalaryX, citySalaryY )
#         return render(request, 'cityChar.html', {
#             'userInfo': userInfo,
#             'selectList': selectList,
#             'defaultCity': defaultCity,
#             'citySalaryX': citySalaryX,
#             'citySalaryY': citySalaryY,
#             'cityPeopleReal': cityPeopleReal,
#         })
#
# def logOut(request):
#     request.session.clear()
#     return redirect('login')
#


#
# def registry(request):
#     if request.method == 'GET':
#         return render(request, 'registry.html', {
#         })
#     else:
#         uname = request.POST.get('username')
#         password = request.POST.get('password')
#         ckPasssword = request.POST.get('ckPassword')
#         print(uname, password, ckPasssword)
#         try:
#             User.objects.get(username=uname)
#             message = '用户名已存在'
#         except:
#             if not uname or not password or not ckPasssword:
#                 message = '注册信息不能为空'
#                 messages.error(request, message)
#                 return HttpResponseRedirect('/myApp/registry/')
#             elif password != ckPasssword:
#                 message = '两次密码不一致'
#                 messages.error(request, message)
#                 return HttpResponseRedirect('/myApp/registry/')
#             else:
#                 User.objects.create(
#                     username=uname,
#                     password=password
#                 )
#                 messages.success(request,'注册成功')
#                 return HttpResponseRedirect('/myApp/login/')
#         return render(request, 'registry.html', {})
#
#
#
# def tableData(request):
#     if request.method == 'GET':
#         uname = request.session.get('username')
#         userInfo = User.objects.get(username=uname)
#
#         tableData = list(getjobData())
#
#
#         return render(request, 'tableData.html', {
#             'userInfo': userInfo,
#             'tableData': tableData
#
#         })
#
#
# def addHistory(request, jobId):
#
#     uname = request.session.get('username')
#     userInfo = User.objects.get(username=uname)
#
#     print(jobId)
#
#     addHistoryData(userInfo, jobId)
#     return HttpResponseRedirect('/myApp/collectData')
#
#
# def delHistory(request, jobId):
#
#     uname = request.session.get('username')
#     userInfo = User.objects.get(username=uname)
#
#     data = History.objects.filter(jobId = jobId)
#     data.delete()
#     return HttpResponseRedirect('/myApp/collectData')
#
#
#
# def collectData(request):
#     if request.method == 'GET':
#         uname = request.session.get('username')
#         userInfo = User.objects.get(username=uname)
#
#         getUserHistory(userInfo)
#         jobList = getUserHistory(userInfo)
#
#
#         return render(request, 'collectData.html', {
#             'userInfo': userInfo,
#             'jobList': jobList
#
#
#         })
#
#
#
#
# def changeInfo(request):
#     uname = request.session.get('username')
#     userInfo = User.objects.get(username=uname)
#
#     if request.method == 'POST':
#         print(request.POST)
#         res = changePwd(userInfo, request.POST)
#         if res != None:
#             messages.error(request, res)
#             return HttpResponseRedirect('/myApp/changeInfo/')
#
#         userInfo = User.objects.get(username=uname)
#         messages.success(request, '密码修改成功')
#
#
#     return render(request, 'changeInfo.html', {
#         'userInfo': userInfo,
#
#     })
#
#
#
#
#
# def titleCloud(request):
#     uname = request.session.get('username')
#     userInfo = User.objects.get(username=uname)
#
#     return render(request, 'titleCloud.html', {
#         'userInfo': userInfo,
#     })
#
#
#
#
# def tagCloud(request):
#     uname = request.session.get('username')
#     userInfo = User.objects.get(username=uname)
#
#     return render(request, 'tagCloud.html', {
#         'userInfo': userInfo,
#     })
#
#
#
# def recommendPage(request):
#     if request.method == 'GET':
#         uname = request.session.get('username')
#         userInfo = User.objects.get(username=uname)
#
#         dataList = list(History.objects.filter(user=userInfo).order_by('-count'))
#         jobIdList = []
#         for i in dataList:
#             jobIdList.append(i.jobId)
#         realJob = query_hive('select title from jobData where id = %d', [int(jobIdList[0])], 'select')[0][0]
#         print(realJob)
#
#         try:
#             recommend_title = get_recommendations(realJob)[:20]
#         except:
#             recommend_title = get_recommendations('java开发实习生[中关村]')[:20]
#
#         idList = []
#         for i in recommend_title:
#             idList.append(i[1])
#
#         recommendList = []
#         for i in idList:
#             x = list(query_hive('select * from jobData where id = %d', [int(i)],'select')[0])
#             recommendList.append(x)
#
#         if len(recommendList) > 12:
#             recommendList = random.sample(recommendList,12)
#
#         return render(request, 'recommendPage.html', {
#             'userInfo': userInfo,
#             'recommendList': recommendList
#         })
#
#
#
# def predict(request):
#     if request.method == 'GET':
#         uname = request.session.get('username')
#         userInfo = User.objects.get(username=uname)
#         jobDataList = list(getjobData())
#         cityList = list(set(x[12] for x in jobDataList))
#         expList = list(set(x[5] for x in jobDataList))
#         eduList = list(set(x[6] for x in jobDataList))
#         print(cityList, eduList, expList)
#         return render(request, 'predict.html', {
#             'userInfo': userInfo,
#             'cityList': cityList,
#             'eduList': eduList,
#             'expList': expList,
#         })
#     else:
#         uname = request.session.get('username')
#         userInfo = User.objects.get(username=uname)
#         jobDataList = list(getjobData())
#         cityList = list(set(x[12] for x in jobDataList))
#         expList = list(set(x[5] for x in jobDataList))
#         eduList = list(set(x[6] for x in jobDataList))
#         print(cityList, eduList, expList)
#
#         defaultCity = request.POST.get('city')
#         defaultExp = request.POST.get('workExp')
#         defaultEdu = request.POST.get('education')
#
#         print(defaultCity, defaultExp, defaultEdu)
#
#         predicted_salary = pred_salary(defaultCity, defaultExp, defaultEdu)
#         return render(request, 'predict.html', {
#             'userInfo': userInfo,
#             'cityList': cityList,
#             'eduList': eduList,
#             'expList': expList,
#             'defaultCity': defaultCity,
#             'defaultEdu': defaultEdu,
#             'defaultExp': defaultExp,
#             'predicted_salary': predicted_salary,
#         })
#
# def steganalysis_home(request):
#     return render(request, 'steganalysis_home.html')
#
# def steganalysis_about(request):
#     return render(request, 'steganalysis_about.html')
#
# def steganalysis_history(request):
#     page = request.GET.get('page', 1)
#     history_list = SteganalysisResult.objects.all().order_by('-analysis_time')
#     paginator = Paginator(history_list, 10)  # 每页显示10条记录
#
#     history_items = paginator.get_page(page)
#
#     context = {
#         'history_items': history_items,
#         'current_page': int(page),
#         'has_previous': history_items.has_previous(),
#         'has_next': history_items.has_next(),
#     }
#
#     return render(request, 'steganalysis_history.html', context)
#
# def analyze_image(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': '只支持POST请求'}, status=405)
#
#     if 'image' not in request.FILES:
#         return JsonResponse({'error': '未找到上传的图片'}, status=400)
#
#     image_file = request.FILES['image']
#
#     try:
#         # 1. 保存图片并创建分析记录
#         result = SteganalysisResult(
#             image=image_file,
#             filename=image_file.name,
#             file_size='计算中...',
#             confidence=0.0,
#             feature_analysis={},
#             algorithm_analysis={}
#         )
#         result.save()
#         result.file_size = result.get_file_size_display()
#
#         # 2. 加载和预处理图片
#         image = Image.open(result.image.path).convert('RGB')
#         transform = transforms.Compose([
#             transforms.Resize((224, 224)),
#             transforms.ToTensor(),
#             transforms.Normalize(mean=[0.485, 0.456, 0.406],
#                               std=[0.229, 0.224, 0.225])
#         ])
#         image_tensor = transform(image).unsqueeze(0)
#
#         # 3. 加载模型并进行预测
#         model = SteganNet()  # 加载您的模型
#         model.eval()
#
#         with torch.no_grad():
#             features, stego_prob = model(image_tensor)
#
#             # 获取隐写检测结果
#             has_stego = stego_prob.item() > 0.5
#             confidence = stego_prob.item() if has_stego else 1 - stego_prob.item()
#
#             # 提取特征分析结果
#             feature_names = ['颜色分布', '纹理特征', '频域特征', '统计特征', '空间特征']
#             feature_values = features[0].tolist()[:5]  # 假设模型输出5个主要特征
#
#             # 生成算法识别结果
#             algorithm_probs = {
#                 'LSB': 0.4,
#                 'DCT': 0.3,
#                 'DWT': 0.2,
#                 'PVD': 0.1
#             }
#
#             # 更新分析记录
#             result.has_stego = has_stego
#             result.confidence = confidence * 100
#             result.feature_analysis = {
#                 'names': feature_names,
#                 'values': feature_values
#             }
#             result.algorithm_analysis = [
#                 {'name': k, 'probability': v * 100}
#                 for k, v in algorithm_probs.items()
#             ]
#             result.save()
#
#             # 返回分析结果
#             return JsonResponse({
#                 'hasStego': has_stego,
#                 'confidence': confidence,
#                 'features': [
#                     {'name': name, 'value': value}
#                     for name, value in zip(feature_names, feature_values)
#                 ],
#                 'algorithms': [
#                     {'name': k, 'probability': v * 100}
#                     for k, v in algorithm_probs.items()
#                 ]
#             })
#
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)
#
# def analysis_detail(request, analysis_id):
#     try:
#         result = SteganalysisResult.objects.get(id=analysis_id)
#         context = {
#             'result': result,
#             'feature_analysis': json.dumps(result.feature_analysis),
#             'algorithm_analysis': json.dumps(result.algorithm_analysis)
#         }
#         return render(request, 'steganalysis_detail.html', context)
#     except SteganalysisResult.DoesNotExist:
#         return JsonResponse({'error': '未找到指定的分析记录'}, status=404)
