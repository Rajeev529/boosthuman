from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from . import map, search
import os
import random
import pandas as pd
from django.conf import settings
# Create your views here.


def about(request):
    dic1=map.dic()
    return render(request, 'about.html',{'dic1':dic1.items()})
def wishlist(request):
    dic1=map.dic()
    arr=map.storewish
    
    return render(request, 'wishlist.html', {'dic1':dic1.items(), 'arr':arr})

def blog(request):
    dic1=map.dic()

    csvpath=os.path.join(settings.BASE_DIR,'static/assets/data/ceo.csv')
    df=pd.read_csv(csvpath)
    data=df.to_dict(orient='records')
    arr=map.storewish
    return render(request, 'blog.html', {'ceo':data,'arr':arr, 'dic1':dic1.items()})

def listing(request, string):
    val=string.replace('%20', ' ')
    
    dic1=map.dic()
    arr=map.storewish

    csvpath=os.path.join(settings.BASE_DIR,'static/assets/data/datacollected2.csv')
    df=pd.read_csv(csvpath)
    data=df[df["course"] == val].to_dict(orient='records')

    return render(request, 'listing.html', {'data':data,'arr':arr, 'dic1':dic1.items()})

def listing2(request):
    val=""
    try:
        val=request.GET['q']
    except:
        val=request.GET['mobile-search']
    if(val):
    
        dic1=map.dic()
        arr=map.storewish
        data=(search.searchAns(val)).to_dict(orient='records')
        return render(request, 'listing.html', {'data':data,'arr':arr, 'dic1':dic1.items()})
    

def homepage(request):
    dic1=map.dic()
    arr=map.storewish
              
    csvpath=os.path.join(settings.BASE_DIR,'static/assets/data/index.csv')
    df=pd.read_csv(csvpath)
    data=df.to_dict(orient='records')

    return render(request, "index.html",{'dic1':dic1.items(), 'data':data, 'arr':arr})
def product(request,idx, platform):
    # idx=int(request.GET('idx'))
    
    dic1=map.dic()
    arr=map.storewish

    dataedx=pd.read_csv(os.path.join(settings.BASE_DIR,'static/assets/data/datacollected2.csv'))
    datayt=pd.read_csv(os.path.join(settings.BASE_DIR,'static/assets/data/youtube.csv'))
    if platform != 'youtube':
        data1=(dataedx[dataedx['idx']==idx]).to_dict(orient='records')

        topic=dataedx.loc[dataedx['idx']==idx, 'course'].iloc[0]
        data2=(datayt[datayt['course']==topic]).to_dict(orient='records')
        random.shuffle(data2)
        
        return render(request,"product.html",{'data1':data1[0], 'data2':data2,'dic1':dic1.items(), 'arr':arr})
    else:
        data1=(datayt[datayt['idx']==idx]).to_dict(orient='records')

        topic=datayt.loc[datayt['idx']==idx, 'course'].iloc[0]
        
        data2=(dataedx[dataedx['course']==topic]).to_dict(orient='records')
        random.shuffle(data2)
        
        return render(request,"product.html",{'data1':data1[0], 'data2':data2,'dic1':dic1.items(), 'arr':arr})

def addwish(request):
    
    if request.method=='GET':
        platform=request.GET['cat_plat']
        cat_id=request.GET['cat_id']
        
        
        if platform=='youtube':
            csvpath=os.path.join(settings.BASE_DIR, 'static/assets/data/youtube.csv')
            df=pd.read_csv(csvpath)
            data = (df[df['idx'].astype(str) == str(cat_id)]).to_dict(orient='records')
            map.storewish.append(data[0])
            return JsonResponse({'status':'success'})
        else:
            csvpath=os.path.join(settings.BASE_DIR, 'static/assets/data/datacollected2.csv')
            df=pd.read_csv(csvpath)
            data = (df[df['idx'].astype(str) == str(cat_id)]).to_dict(orient='records')
    
            map.storewish.append(data[0])
            return JsonResponse({'status':'success'})
def popuparr(request):
    if request.method == 'GET':
        key1 = int(request.GET['key1'])
        
        map.storewish.pop(key1)
        # if key1 < 0 or key1 >= len(map.storewish):
        return JsonResponse({'redirect': '/wishlist'})  # Use named URL if preferred
        # return JsonResponse({'status': 'success'})
