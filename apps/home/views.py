# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import pandas as pd
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from core.settings import BASE_DIR
from .models import SparePartGood, SparePartOutRecord, SparePartOutRequest, Upload, User
from .forms import ManageFormOuT, ManageForm
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt




@login_required(login_url="/login/")
def index(request):
    requestsparepartout = SparePartOutRequest.objects.all()
    context = {'segment': 'index','requestsparepartou':requestsparepartout}
    
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@xframe_options_exempt
def autoadd(filename):
    print("run...........................")
    filename0 = str(filename).replace(' ','_')
    print(filename0)
    newFile = __file__.replace('home\\views.py','static\\imagesmediaurl\\fileupload\\'+str(filename0))
    print(newFile)
    df0 = pd.read_excel(newFile)
    df0.columns = [c.replace(' ', '_') for c in df0.columns]
    df0.columns = [c.replace('/', '') for c in df0.columns]
    df0 = df0.fillna('0')
    for i in range(0,df0.shape[0]):
        SparePartGood.objects.create(
                remainQTY=df0.loc[i,"Remaining_Qty"],
                consumQTY=df0.loc[i,"Consump_Qty_"],
                actualQTY = df0.loc[i,"Actual_Qty"],
                remark = df0.loc[i,"Remark"],
                transitWay=df0.loc[i,"Transporation_way_(DHL_Air_Sea)"],
                batch = df0.loc[i,"#_Batch"],
                invoice = df0.loc[i,"Invoice"],
                sender = df0.loc[i,"Sender"],
                warehouse = df0.loc[i,"Warehouse_\n(HN,DN,KH,HCM)"],
                deliverDate = df0.loc[i,"Delivery_date_"],
                productDescription = df0.loc[i,"Product_Description"],
                serialNumber = df0.loc[i,"SN"],
                csceHWMO = df0.loc[i,"Central_inverter,_string_inverter,_Comunication_device,_ESS_,_Hybird__inverter_,_wind_Converter_,_MV_device,_Other)"],
                sparePartType = df0.loc[i,"Spare_part_type_(product_spare_part)"],
                goodStatus = df0.loc[i,"Goods_status_(newgood)"],
                partCode = df0.loc[i,"Part_Code"]
            )
    print("DONE")
    return HttpResponse("""
                <h1> upload successful! go to main page after 5s</h1>
                 <script>
                    setTimeout(function(){
                            window.location.href = 'http://127.0.0.1:8000/upload/';
                        }, 5000);
                </script>
            """)
    

@login_required(login_url="/login/")
def index(request):
    requestsparepartout = SparePartOutRequest.objects.all()
    context = {'segment': 'index','requestsparepartou':requestsparepartout}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template


        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@xframe_options_exempt
@login_required(login_url='login')
def manageform(request):
    form = ManageForm()
    if request.method == 'POST':

        SparePartGood.objects.create(
            remainQTY=request.POST.get('remainQTY'),
            consumQTY=request.POST.get('consumQTY'),
            actualQTY = request.POST.get('actualQTY'),
            remark = request.POST.get('remark'),
            transitWay=request.POST.get('transitWay'),
            batch = request.POST.get('batch'),
            invoice = request.POST.get('invoice'),
            sender = request.POST.get('sender'),
            warehouse = request.POST.get('warehouse'),
            deliverDate = request.POST.get('deliverDate'),
            productDescription = request.POST.get('productDescription'),
            serialNumber = request.POST.get('serialNumber'),
            csceHWMO = request.POST.get('csceHWMO'),
            sparePartType = request.POST.get('sparePartType'),
            goodStatus = request.POST.get('goodStatus'),
            partCode = request.POST.get('partCode')
        )

        return redirect('pages')

    context = {'form': form}
    return render(request, 'home/manageform.html', context)


@xframe_options_exempt
@login_required(login_url='login')
def updateSpare(request, pk):
    spare = SparePartGood.objects.get(id=pk)
    form = ManageForm(instance=spare)
    
    # if request.user.role == 0:
    #     return HttpResponse('<h1>You are not allowed here!</h1>')

    if request.method == 'POST':
        form = ManageForm(request.POST, instance=spare)
        if form.is_valid:
            form.save()
            return redirect('pages')

    context = {'form': form}
    return render(request, 'home/manageform.html',context)

@login_required(login_url='login')
def deleteSpare(request, pk):
    spare = SparePartGood.objects.get(id=pk)

    # if request.user == 0:
    #     return HttpResponse('<h1>You are not allowed here!</h1>')

    if request.method == 'POST':
        spare.delete()
        return redirect('pages')
    return render(request, 'home/delete.html', {'obj':spare})

@xframe_options_exempt
def manageTable(request):
    data = SparePartGood.objects.all()

    showsender = 1
    showinvoice =1 
    if(request.GET.get('mybtn')):
        showsender = request.GET.get('sender')
        showinvoice = request.GET.get('invoice')
        key3 = request.GET.get('batch')
        



    context = {'data': data,'showsender':showsender, 'showinvoice':showinvoice}
    return render(request,'home/manageTable.html', context)

@xframe_options_exempt
def managesparepartouttable(request):
    data = SparePartOutRecord.objects.all()
    
    context = {'data': data}
    return render(request,'home/managesparepartouttable.html', context)

@login_required(login_url='login')
@xframe_options_exempt
def uploadall(request):
    try:
        filehere = Upload.objects.get(id=1)
    except:
        filehere = None

    if request.method == 'POST':
        
        upload = Upload.objects.create(
            user = request.user,
            file = request.FILES.get('files')
        )
        filename = request.FILES.get('files')
        
        try:
            autoadd(filename)
        except:
            return HttpResponse("""
            <h1>ERROR</h1><div>
            <a href="http://127.0.0.1:8000/tables.html">
                <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
                <title>arrow-left</title>
                <path
                    d="M13.723 2.286l-13.723 13.714 13.719 13.714 1.616-1.611-10.96-10.96h27.625v-2.286h-27.625l10.965-10.965-1.616-1.607z">
                </path>
                </svg>
                </a>
            </div>
            """)
        return HttpResponse("""
                <h1> upload successful! go to main page after 5s</h1>
                 <script>
                    setTimeout(function(){
                            window.location.href = 'http://127.0.0.1:8000/upload/';
                        }, 5000);
                </script>
            """)
    if filehere != None:
        context = {'filehere':filehere}
    else:
        context = {}
    return render(request,'home/uploadall.html', context)

@login_required(login_url='login')
@xframe_options_exempt
def managespare(request, pk):
    spare = SparePartGood.objects.get(id = pk)
    spareOut = spare.sparepartoutrecord_set.all()
    spareOutRequest = spare.sparepartoutrequest_set.all()
    
    requestsuccess = 2
    if request.method == 'POST':
        try:
            outqty = request.POST.get('outqty')
            if int(outqty) <= spare.remainQTY and int(outqty) > 0:
                out = SparePartOutRequest.objects.create(
                    userOutRequestor = request.user,
                    sparePartGoodOut = spare,
                    outqty = request.POST.get('outqty'),
                    outDate = request.POST.get('outDate'),
                    outReceiver = request.POST.get('outReceiver'),
                    outRemark = request.POST.get('outRemark')
                )
                requestsuccess == 1
        except:
            requestsuccess == 0

    if(request.GET.get('mybtn')):
        # mypythoncode.mypythonfunction( int(request.GET.get('mytextbox')))
        pk = int(request.GET.get('mytextbox'))
        spareOutInRequest = spare.sparepartoutrequest_set.get(id=pk)
        spareOutSubmit = SparePartOutRecord.objects.create(
            userOutRequestor = spareOutInRequest.userOutRequestor,
            sparePartGoodOut = spare,
            outqty = spareOutInRequest.outqty,
            outDate = spareOutInRequest.outDate,
            outReceiver = spareOutInRequest.outReceiver,
            outRemark = spareOutInRequest.outRemark
        )
        spare.consumQTY += int(spareOutSubmit.outqty)
        spare.remainQTY -= int(spareOutSubmit.outqty)
        spare.save()
        spareOutInRequest.role = 1
        spareOutInRequest.save()
        return redirect('manage-spare', pk=spare.id)
    totalOut = 0
    # for out in spareOut:
    #     totalOut += int(out.outqty)
    totalOut += int(spare.consumQTY)
    context = {'spare': spare, 'spareOut':spareOut, 'totalOut': totalOut, 'spareOutRequest': spareOutRequest,'requestsuccess':requestsuccess}
    return render(request, 'home/managespare.html', context)


@login_required(login_url='login')
def manageSparePartOut(request):
    form = ManageFormOuT()
    if request.method == 'POST':
        SparePartOutRecord.objects.create(
            remainQTY=request.POST.get('remainQTY'),
            consumQTY=request.POST.get('consumQTY'),
            actualQTY = request.POST.get('actualQTY'),
            remark = request.POST.get('remark'),
            transitWay=request.POST.get('transitWay'),
            batch = request.POST.get('batch'),
            invoice = request.POST.get('invoice'),
            sender = request.POST.get('sender'),
            warehouse = request.POST.get('warehouse'),
            deliverDate = request.POST.get('deliverDate'),
            productDescription = request.POST.get('productDescription'),
            serialNumber = request.POST.get('serialNumber'),
            csceHWMO = request.POST.get('csceHWMO'),
            sparePartType = request.POST.get('sparePartType'),
            goodStatus = request.POST.get('goodStatus'),
            partCode = request.POST.get('partCode'),

            outqty = request.POST.get('outqty'),
            outDate = request.POST.get('outDate'),
            outRequestor = request.POST.get('outRequestor'),
            outReceiver = request.POST.get('outReceiver'),
            outGSP = request.POST.get('outGSP'),
            outRemark = request.POST.get('outRemark')
        )

        return redirect('manageTable')

    context = {'form': form}
    return render(request, 'home/manageSparePartOut.html', context)

def upload(request):
    data = Upload.objects.all()
    drop = 0
    context = {'data':data, 'drop':drop}
    return render(request, 'home/upload.html', context)

def requestsparepartout(request):
    data = SparePartOutRequest.objects.all()
    droprequest = 0
    requestsuccess = 2
    spareSearch = SparePartGood.objects.all()
    if request.method == 'POST':
        
        partCode = request.POST.get('SparePartCode')
        outqty = request.POST.get('outqty')
        warehouse = request.POST.get('warehouse')
        for spare in spareSearch:
            if spare.partCode == partCode and spare.remainQTY >= int(outqty) and spare.warehouse == warehouse and int(outqty)>0:
                out = SparePartOutRequest.objects.create(
                    userOutRequestor = request.user,
                    sparePartGoodOut = spare,
                    outqty = request.POST.get('outqty'),
                    outDate = request.POST.get('outDate'),
                    outReceiver = request.POST.get('outReceiver'),
                    # outGSP = request.POST.get('outGSP'),
                    outRemark = request.POST.get('outRemark'),
                    file = request.FILES.get('reportfile')
                )
                requestsuccess = 1
                break
            else:
                requestsuccess = 0

    if(request.GET.get('submitbtn')):
        # mypythoncode.mypythonfunction( int(request.GET.get('mytextbox')))
        pk = int(request.GET.get('mytextbox'))
        data2 = SparePartOutRequest.objects.get(id=pk)
        spareOutInRequest = data2.sparePartGoodOut.sparepartoutrequest_set.get(id=pk)
        if data2.role == 0:
            spareOutSubmit = SparePartOutRecord.objects.create(
                userOutRequestor = spareOutInRequest.userOutRequestor,
                sparePartGoodOut = data2.sparePartGoodOut,
                outqty = spareOutInRequest.outqty,
                outDate = spareOutInRequest.outDate,
                outReceiver = spareOutInRequest.outReceiver,
                outGSP = request.GET.get('mytextboxGSP'),
                outRemark = spareOutInRequest.outRemark
            )
            data2.sparePartGoodOut.consumQTY += int(spareOutSubmit.outqty)
            data2.sparePartGoodOut.remainQTY -= int(spareOutSubmit.outqty)
            data2.sparePartGoodOut.save()
            spareOutInRequest.role = 1
            spareOutInRequest.save()
            return redirect('manage-spare', pk=data2.sparePartGoodOut.id)
        else:
            pass

    context ={'data':data, 'droprequest':droprequest,'requestsuccess':requestsuccess,'spareSearch':spareSearch}
    return render(request, 'home/requestsparepartout.html', context)