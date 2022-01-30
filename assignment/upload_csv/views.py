import pprint
from re import template
from django.shortcuts import render
import csv,io
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from matplotlib.style import context
from .models import Csv
from django.contrib import messages
import datetime
# Create your views here.
def upload_csv(request):
    template = "upload_csv.html"

    if request.method == 'GET':
        return render(request,template)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'This is not csv file')
    
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)


    for column in csv.reader(io_string,delimiter='"',quotechar="|"):
        if len(column) == 3:
            d = date = datetime.datetime.strftime((datetime.datetime.strptime(column[2].replace(",",''), '%Y-%m-%d')),'%d-%m-%Y')
            print((d))
            _, created = Csv.objects.update_or_create(
             image_name = column[0].replace(',',''),
             objects_detected = column[1],
             date = datetime.datetime.strftime((datetime.datetime.strptime(column[2].replace(",",''), '%Y-%m-%d')),'%d-%m-%Y')
             )

        elif len(column) == 1:
            new_column = column[0].split(',')
            _, created = Csv.objects.update_or_create(
             image_name = new_column[0],
             objects_detected = new_column[1],
             date = datetime.datetime.strftime((datetime.datetime.strptime(new_column[2].replace(",",''), '%Y-%m-%d')),'%d-%m-%Y')
             )
            
      
    context = {}
    return render (request,template,context)

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.csv")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def view_data(request):
    item = Csv.objects.all()
    context = {'item':item}
    return render(request,'view.html',context)

def filter_data(request):


    if request.method == "POST":
        start = request.POST['start']
        start_date = datetime.datetime.strftime((datetime.datetime.strptime(str(start), '%Y-%m-%d')),'%d-%m-%Y')
        end = request.POST['end']
        end_date = datetime.datetime.strftime((datetime.datetime.strptime(str(end), '%Y-%m-%d')),'%d-%m-%Y')
        print(str(start_date),str(end_date))
        item = Csv.objects.filter(date__range=[str(start_date),str(end_date)])
        pprint.pprint(item)
        context = {'item':item}
 
        return render(request,'filter.html',context)
        
        
    
    return render(request,'filter.html')

def check(request):
    if request.method == "POST":
        start = request.POST['start']
        start_date = datetime.datetime.strftime((datetime.datetime.strptime(str(start), '%Y-%m-%d')),'%d-%m-%Y')
        end = request.POST['end']
        end_date = datetime.datetime.strftime((datetime.datetime.strptime(str(end), '%Y-%m-%d')),'%d-%m-%Y')
        print(str(start_date),str(end_date))
        item = Csv.objects.filter(date__range=[str(start_date),str(end_date)])
        objects = {}
        for i in item:
            
            obj = i.objects_detected.split(',')
            for j in obj:
                if j not in objects:
                    objects[j] = 1
                else:
                    objects[j] += 1
        pprint.pprint(objects)
        with open('report.csv', 'w') as f:
            for key in objects.keys():
                f.write("%s,%s\n"%(key,objects[key]))
                

        context = {'item':item}
 
        return render(request,'final.html',context)
        
        
    
    return render(request,'final.html')
      
    
