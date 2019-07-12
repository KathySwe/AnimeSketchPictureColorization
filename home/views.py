from django.shortcuts import render,HttpResponse
from django.core.files.storage import FileSystemStorage

from home.genimg import hex_to_rgb
from home.genimg import create_colorimg
from home.colorize import act,actbycolor


# Create your views here. #for each page is just method
def home(request):
   context={}
   
   # return HttpResponse('Home page!')
   if request.method=='POST':
      uploaded_pic=request.FILES['document']
      print(uploaded_pic.name)
      print(uploaded_pic.size)
      fs=FileSystemStorage()
      name=fs.save(uploaded_pic.name,uploaded_pic)
      context['url']=fs.url(name)
      print(fs.url(name))
      firstcolor=request.POST['ficol']
      seccolor=request.POST['scol']
      thirdcolor=request.POST['tcol']
      fourthcolor=request.POST['focol']
      a=hex_to_rgb(firstcolor)
      b=hex_to_rgb(seccolor)
      c=hex_to_rgb(thirdcolor)
      d=hex_to_rgb(fourthcolor)
      create_colorimg(a,b,c,d)
      context['colorimg']='/media/immm.jpg'
      # act(context['colorimg'].strip('/'),context['url'].strip('/'))
      actbycolor([a,b,c,d],context['url'].strip('/'))
      context['result'] = '/media/result.jpg'
      context['comresult']='/media/compareresult.jpg'
      return render(request,'result.html',context)
   return render(request,'upload/uploadpic.html',context)