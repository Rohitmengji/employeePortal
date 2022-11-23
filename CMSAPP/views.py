from datetime import date
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from CMSAPP.models import userdata, UploadFileData,FriendRequest,ChatDetails
import os, sys
import hashlib

#------------------------------------------------------------------------------------------------------
def findDup(parentFolder):
    # Dups in format {hash:[names]}

    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups
# Joins two dictionaries
def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]
 
 
def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()
 
 
def printResults(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    path="" 
    i=0
    if len(results) > 0:
        print('Duplicates Found:')
        print('The following files are identical. The name could differ, but the content is identical')
        print('___________________')
        i=0
        for result in results:
        	i=0
        	singleimagename=""
        	for subresult in result:
        		i=i+1
        		print('\t\t%s' % subresult)
        		if i==1 and subresult!="NOFILE":
        			singleimagename=subresult
        			print("FILENAME--->"+singleimagename)
        		if os.path.exists(subresult) and i>1:
        			iddata=ChatDetails.objects.all()
        			m=iddata[0].id
        			print("-------->"+str(m))
        			x=0
        			for x in range(len(iddata)):
        				if x>0:
        					c=iddata[x]
        					print("M2======="+str(m))
        					if(str(c.filename).replace("/","-").endswith(subresult.replace("\\","-"))):
        						print("YES ITS ENDIND WITH")        			
        						data=ChatDetails.objects.get(id=c.id)
        						data.filename="/"+singleimagename.replace("\\","/")
        						print("REPLACE NAME"+singleimagename)
        						data.save()
        						os.remove(subresult)
        			i=2	           

def checkduplicate(request):
	if request.method=="POST":
		return render(request,"cms/checkduplicate.html",{"msg":"Deleted Duplicate Files"})
	else:
		dups = {}
		joinDicts(dups, findDup("media"))
		printResults(dups)

		return render(request,"cms/checkduplicate.html")
def viewusers(request):
	if request.method=="POST":
		m=FriendRequest()
		m.emailid1=request.POST.get("txtemailid","")
		m.name1=request.POST.get("txtname","")
		m.gender1=request.POST.get("txtgender","")
		m.country1=request.POST.get("txtcountry","")
		m.profession1=request.POST.get("txtprofession","")
		m.mobilenumber1=request.POST.get("txtmobilenumber","")
		m.emailid2=request.session["emailid"]
		m.name2=request.session["name"]
		m.gender2=request.session["gender"]
		m.country2=request.session["country"]
		m.profession2=request.session["profession"]
		m.mobilenumber2=request.session["mobilenumber"]
		m.status="0"
		m.save()
		data=userdata.objects.exclude(email=request.session["emailid"])
		return render(request,"cms/viewusers.html",{"data":data,"msg":"Request Sent"})
	else:
		data=userdata.objects.exclude(email=request.session["emailid"])
		return render(request,"cms/viewusers.html",{"data":data})
def acceptedrequest(request):
	data=""
	if request.method=="POST":
		emailid=request.POST.get("txtemailid","")
		request.session["getemailchat"]=emailid
		if  ChatDetails.objects.filter(messageto=request.session["emailid"],messagefrom=emailid).exists():
			data=ChatDetails.objects.filter(messageto=request.session["emailid"],messagefrom=emailid)
			return render(request,"cms/userviewmsg.html",{"data":data})
		else:
	  		FriendRequest.objects.filter(emailid1=request.session["emailid"]).exists()
	  		data=FriendRequest.objects.filter(emailid1=request.session["emailid"],status=1)
	  		return render(request,"cms/acceptedrequest.html",{"data":data})
	else:
		if  FriendRequest.objects.filter(emailid1=request.session["emailid"]).exists():
			data=FriendRequest.objects.filter(emailid1=request.session["emailid"],status=1)
	return render(request,"cms/acceptedrequest.html",{"data":data})


def myfriends(request):
	data=""
	if request.method=="POST":
		reqid=request.POST.get("txtrequestid","")
		m=FriendRequest.objects.get(id=reqid)
		m.status=1
		m.save()
		if  FriendRequest.objects.filter(emailid1=request.session["emailid"]).exists():
			data=FriendRequest.objects.filter(emailid1=request.session["emailid"],status=0)
			return render(request,"cms/myfriends.html",{"data":data})
		else:
			return render(request,"cms/myfriends.html",{"data":data})
	if  FriendRequest.objects.filter(emailid1=request.session["emailid"]).exists():
		data=FriendRequest.objects.filter(emailid1=request.session["emailid"],status=0)
		return render(request,"cms/myfriends.html",{"data":data})
	else:
		return render(request,"cms/myfriends.html",{"data":data})
	

def usermessages(request):
	return render(request,"cms/usermessages.html")

def userregistercode(request):
	if request.method=="POST":
		s=userdata()
		s.name=request.POST.get("entername","")
		s.mobilenumber=request.POST.get("mobilenumber","")
		s.email=request.POST.get("emailid","")
		s.password=request.POST.get("password","")
		s.gender=request.POST.get("gender","")
		s.country=request.POST.get("Country","")
		s.profession=request.POST.get("Profession","")
		s.save()
		return render(request,"cms/userregister.html",{"msg":"Registered Successfully"})
	else:
		return render(request,"cms/userregister.html")
def UploadFilecode(request):
	if request.method=="POST":
		s=UploadFileData()
		s.filetype=request.POST.get("Filetype","")
		s.name=request.POST.get("entername","")
		s.file=request.POST.get("photo","")
		return render(request,"cms/uploadfile.html",{"msg":"Uploaded Successfully"})
	else:
		return render(request,"cms/uploadfile.html")
def registerdisplayCode(request):
	if request.method=="POST":
		hid=request.POST.get("hid","")
		if userdata.objects.filter(id=hid).exists():	
			m=userdata.objects.get(id=hid)
			m.delete()
		data=userdata.objects.all()
		return render(request,"cms/registerdisplay.html",{"data":data,"msg":"User Deleted"})
	else:
		data=userdata.objects.all()
		return render(request,"cms/registerdisplay.html",{"data":data})

def login(request):
	try:
		if request.method=="POST":
			emailid=request.POST.get("emailid","")
			password=request.POST.get("password","")
			print(emailid=="admin@gmail.com")
			print(password=="admin123")
			if(emailid=="admin@gmail.com" and password=="admin123"):
				return render(request,"cms/adminhome.html")
			else:	
				r=userdata.objects.get(email=emailid,password=password)
				request.session['emailid']=emailid;
				request.session['name']=r.name;
				request.session['mobilenumber']=r.mobilenumber;
				request.session['gender']=r.gender;
				request.session['country']=r.country;
				request.session['profession']=r.profession;
				dd1=FriendRequest.objects.filter(emailid2=request.session["emailid"],status=1).exists()
				if  dd1:
					data1=FriendRequest.objects.filter(emailid1=request.session["emailid"],status=1)
					return render(request,"cms/userhome.html",{"data1":data1})
				
				return render(request,"cms/userhome.html",{"msg":"Mail Sent"})
		else:
			return render(request,"cms/login.html")
	except Exception as e:
		return render(request,"cms/login.html",{"msg":"Invalid Email Id or Password"})

def userhome(request):
	if request.method=="POST" :
		if len(request.FILES) != 0:
			myfile = request.FILES['upfile']
			fs = FileSystemStorage()
			filename = fs.save(myfile.name, myfile)
			uploaded_file_url = fs.url(filename)
		else:	
			uploaded_file_url="NOFILE"
		msg=ChatDetails()
		msg.messageto=request.POST.get("username","")
		msg.message=request.POST.get("txtmessage","")
		msg.messagefrom=request.session["emailid"]
		today = date.today()
		msg.currentdate=today.strftime("%d/%m/%Y")
		msg.filename=uploaded_file_url
		msg.save()
		dd1=FriendRequest.objects.filter(emailid2=request.session["emailid"],status=1).exists()
		if  dd1:
			data1=FriendRequest.objects.filter(emailid1=request.session["emailid"],status=1)
			return render(request,"cms/userhome.html",{"data1":data1,"msg":"Mail Sent"})
		else:
			return render(request,"cms/userhome.html",{"msg":"Mail Sent"})
	else:	
		dd1=FriendRequest.objects.filter(emailid2=request.session["emailid"],status=1).exists()
		if  dd1:
			data1=FriendRequest.objects.filter(emailid1=request.session["emailid"],status=1)
			return render(request,"cms/userhome.html",{"data1":data1})
		else:
			return render(request,"cms/userhome.html")

def adminhome(request):
	return render(request,"cms/adminhome.html")

def uploaddisplayCode(request):
	data=UploadFileData.objects.all()
	return render(request,"cms/uploaddisplay.html",{"data":data})
# Create your views here.
