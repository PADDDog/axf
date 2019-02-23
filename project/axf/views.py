from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Wheel,Nav,Mustbuy,Shop,MainShow,FoodTypes,Goods,User,Cart,Consignee,Defaultaddr,Order,Comment
from django.http import JsonResponse
import time
import random
from django.conf import settings
from django.contrib.auth import logout
import os
from .forms.forms import LoginForm
import uuid

#主页
def home(request):
    #大轮播数据
    wheels = Wheel.objects.all()
    #导航条数据
    navs = Nav.objects.all()
    #必买数据
    mustbuyList = Mustbuy.objects.all()
    #便利店数据
    shopList = Shop.objects.all()
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:11]
    #其他数据
    mainList = MainShow.objects.all()
    return render(request,'home.html',{"title":"主页","wheels":wheels,'navs':navs,'mustbuyList':mustbuyList,'shopList':shopList,'shop1':shop1,'shop2':shop2,'shop3':shop3,'shop4':shop4,'mainList':mainList})

#超市
def market(request,categoryid,cid,sortid):
    #左侧类别栏点击位置
    typeN = FoodTypes.objects.get(typeid = categoryid).typename
    #左侧类别栏
    leftSlider = FoodTypes.objects.all()
    #检查用户登录状态
    try:
        token = request.session.get("token")
        user = User.objects.get(userToken=token)
        #获取用户购物车数据
        carts = Cart.objects.filter(userAccount=user.userAccount)
    except:
        pass
    #判断是否是全部类别
    if cid == 0:
        productList = Goods.objects.filter(categoryid=categoryid)
    else:
        productList = Goods.objects.filter(categoryid=categoryid,childcid=cid)
    #综合排序类别
    if sortid == 1:
        productList = productList.order_by("productnum")
    elif sortid == 2:
        productList = productList.order_by("-price")
    elif sortid == 3:
        productList = productList.order_by("price")

    # for c in carts:
        # for p in productList:
        #     if c.productid == p.productid:
        #         p.style = ""
        #         p.num = c.productnum
        #         p.wtf = "-"
        #         # p.num = c.productnum
        #         # p.btnstyle = ''
        #         # p.spstyle = 'color:red;'
        #     else:
        #         p.style = "display:none"
        #         # p.num = 0
        #         # p.btnstyle = 'display: none'
        #         # p.spstyle = 'display:none'

    #group：左侧栏点击的那一个父类别
    group = leftSlider.get(typeid=categoryid)
    childNameList = []
    #childNames：group的子分类
    childNames = group.childtypenames
    #arr1：子分类的剪切
    arr1 = childNames.split('#')
    #把arr1剪切成字典，key值是子类别名称，value值是类别id
    for str in arr1:
        arr2 = str.split(':')
        obj = {"childName":arr2[0],"childId":arr2[1]}
        #放进childNameList列表里，每个元素是一个字典
        childNameList.append(obj)
    return render(request,'market.html',{"title":"超市","leftSlider":leftSlider,'productList':productList,'childNameList':childNameList,'categoryid':categoryid,"cid":cid,"typeN":typeN})

#购物车
def cart(request):
    #cartList用来放对应用户的购物车内容
    cartList = []
    userInfo = {}
    #检查登录状态
    try:
        token = request.session.get("token")
    except:
        token = None
    #如果登录了：获取用户的购物车内容赋值给cartList，传给购物车页面
    if token:
        user = User.objects.get(userToken=token)
        #取出存在session里的收货信息放入userInfo
        try:
            useraccount = user.userAccount
            defaddr = Defaultaddr.objects.get(userAccount=useraccount).defaultaddr
            consig = Consignee.objects.get(pk = defaddr)
        except:
            consig = None
        cartsList = Cart.objects.filter(userAccount=user.userAccount,isDelete=False)
        sum = 0
        for cl in cartsList:
            sum = float(sum)+float(cl.productprice)
        return render(request, 'cart.html', {"title": "购物车","cartslist":cartsList,"sum":sum,"user":user,"consignee":consig})
    #没登录重定向到登录页面
    else:
        return redirect("/login/")

#我的
def mine(request):
    #获取存在session里的用户名，获取不到默认未登录
    username = request.session.get("username","未登录")
    #获取存在session里的token，用token获取用户头像和等级
    try:
        usertoken = request.session.get("token")
        userimg = User.objects.get(userToken=usertoken).userImg
        userrank = User.objects.get(userToken=usertoken).userRank
        return render(request,'mine.html',{"title":"我的","username":username,"userImg":userimg,"userRank":userrank})
    #没获取到的话直接渲染mine页面回去
    except  User.DoesNotExist as e:
        return render(request, 'mine.html', {"title": "我的","username":username})
# def indes(request):
#     return render(request,'indes.html')
# def base(request):
#     return render(request,'base.html')

#登录
def login(request):
    #验证请求是否为POST请求，对内容进行判断
    if request.method == "POST":
        #获取表单
        f = LoginForm(request.POST)
        if f.is_valid():
            #信息格式验证正确
            name = f.cleaned_data["username"]
            pswd = f.cleaned_data["passwd"]
            # 获取表单的username，passwd
            userAccount = request.POST.get("username")
            password = request.POST.get("passwd")
            try:
                #根据username去用户表取对应用户账号的密码
                truepass = User.objects.get(userAccount=userAccount).userPasswd
                #与表单的密码匹配
                if truepass == password:
                    user = User.objects.get(userAccount=userAccount)
                    username = user.userName
                    userimg = user.userImg
                    userrank = user.userRank
                    newtoken = str(time.time()+random.randrange(1,100000))
                    user.userToken = newtoken
                    user.save()
                    request.session["username"] = user.userName
                    request.session["token"] = user.userToken
                    return render(request, 'mine.html',
                                  {"username": username, "userImg": userimg, "userRank": userrank})
                #密码不匹配情况，返回second给login页面渲染，提示用户
                return render(request, 'login.html', {"title": "登录", "form": f, "second": 'true'})
            #匹配不到用户，用户不存在，返回second给login页面渲染，提示用户
            except User.DoesNotExist as e:
                return render(request,'login.html',{"title":"登录","form":f,"second":'true'})
        #信息格式不对，返回error给login页面渲染，提示用户
        else:
            return render(request, 'login.html', {"title": "登录", "form": f, "error": f.errors})

    #不是POST请求，直接返回登录页面
    else:
        f = LoginForm()
        return render(request,'login.html',{"title":"登录","form":f})



#注册
def register(request):
    #验证请求是否为POST请求
    if request.method == "POST":
        #获取POST请求内容
        userAccount = request.POST.get("userAccount")
        userPasswd = request.POST.get("userPass")
        userName = request.POST.get("userName")
        userPhone = request.POST.get("userPhone")
        userAdderss = request.POST.get("userAdderss")
        userRank = 0
        userToken = str(time.time() + random.randrange(1,100000))
        #获取图片文件
        f = request.FILES["userImg"]
        userImg = ("../static/mdeia/"+userAccount+".jpg")
        #合成图片保存路径
        imgURL = os.path.join(settings.MDEIA_ROOT,userAccount+".jpg")
        #保存图片
        with open(imgURL,'wb') as fp:
            for data in f.chunks():
                fp.write(data)
        #创建并保存用户数据到数据库
        user = User.createuser(userAccount,userPasswd,userName,userPhone,userAdderss,userImg,userRank,userToken)
        user.save()
        #保存userName，userToken到session里
        request.session["username"] = userName
        request.session["token"] = userToken
        return redirect("/mine/")
    else:
        #检测POST失败，重新返回注册
        return render(request, 'register.html', {"title": "注册"})#, "form": form


#检测注册账号是否存在
def checkuserid(request):
    userid = request.POST.get("userid")
    try:
        #根据userid从数据库里获取用户账号
        user = User.objects.get(userAccount=userid)
        #获取到即返回Json数据，提示用户账号已被注册
        return JsonResponse({"data":"该用户已被注册","status":"error"})
    except User.DoesNotExist as e:
        #未获取到返回Json数据，证明注册的账号名可用
        return JsonResponse({"data": "ok", "status": "success"})


#退出登录
def quit(request):
    logout(request)
    return redirect("/mine/")


#改变购物车数量
def changecart(request,type):
    #判断用户是否登录
    try:
        token = request.session.get("token")
    except:
        token = None
    #用户未登录返回Json让（market.js）跳转登录页面
    if token == None:
        return JsonResponse({"data":-1,"status":"error"})
    #用户登录状态
    #获取（market.js）发起的ajax请求里用户加入购物车的商品Id
    productid = request.POST.get("productid")
    #根据商品Id获取商品信息
    product = Goods.objects.get(productid=productid)
    #获取商品库存
    prostorenums = product.storenums
    #根据token值获取用户信息
    user = User.objects.get(userToken=token)
    # hoprice为购物车内商品单价
    hoprice = product.price
    try:
        #根据用户账号及商品Id获取购物车内对象信息及商品购买数量
        cart = Cart.objects.get(userAccount=user.userAccount, productid=productid)
        cartnums = cart.productnum
    except:
        # 未获取到表明该商品还未加入过购物车
        cartnums = 0
    #market加数量的情况
    if type == 0:
        #如购物车内商品大于等于库存
        if cartnums >= product.storenums:
            # 将库存storenums返回页面修改购物车内商品数量
            return JsonResponse({"data": product.storenums, "status": "max","hoprice":hoprice})
        #筛选获取购物车内商品信息
        carts = Cart.objects.filter(userAccount=user.userAccount,productid=productid)
        c = None
        if carts.count() == 0:
            #购物车内无该商品直接增加一条订单
            c = Cart.createcart(user.userAccount,productid,1,product.price,True,product.productimg,product.productlongname,False)
            c.save()
        else:
            #购物车内有该商品则只修改对应订单的数量价格
            c = carts.get(productid=productid)
            c.productnum += 1
            c.productprice = "%.2f" % (float(product.price) * c.productnum)
            c.save()
        return JsonResponse({"data":c.productnum,"status":"success","hoprice":hoprice})

    # market减数量的情况
    elif type == 1:
        #筛选获取用户购物车内商品信息
        carts = Cart.objects.filter(userAccount=user.userAccount)
        #用户购物车内该商品数量减一，并重新计算价格
        cart = carts.get(productid=productid)
        cart.productnum -= 1
        cart.productprice = "%.2f" % (float(product.price) * cart.productnum)
        # 如购物车内商品减少到0，则从数据库中购物车信息表里删除该商品，否则保存到数据库
        if cart.productnum == 0:
            cart.delete()
        else:
            cart.save()
        return JsonResponse({"data": cart.productnum, "status": "success","hoprice":hoprice})

#收货信息
def consignee(request):
    #如果是POST请求
    if request.method == "POST":
        #获取当前登录的token
        token = request.session.get("token")
        #根据token获取用户账号
        userAccount = User.objects.get(userToken=token).userAccount
        #获取用户信息
        conname = request.POST.get("conname")
        conphone = request.POST.get("conphone")
        conaddr = request.POST.get("conaddr")
        #保存收货人信息到数据库
        consignee = Consignee()
        consignee.userAccount = userAccount
        consignee.consigneeName = conname
        consignee.consigneeTel = conphone
        consignee.consigneeAddr = conaddr
        consignee.save()
        #跳转到收货信息列表
        return redirect("/alladdr/")
    #不是POST请求直接放回consignee.html
    else:
        return render(request,"consignee.html",{"title":"收货人"})
#收货信息列表
def alladdr(request):
    #获取token
    try:
        token = request.session.get("token")
    except:
        token = None
    #如果token不为空
    if token:
        #获取该token对应用户的所有收货信息
        userAccount = User.objects.get(userToken=token).userAccount
        addrList = Consignee.objects.all().filter(userAccount=userAccount)
        return render(request,"alladdr.html",{"title":"收货地址管理","addrList":addrList})
    else:
        #没有获取到token返回登录页面
        return redirect("/login/")

#删除收货信息
def deladdr(request):
    #获取ajax请求中的id，找到对应的收货信息并删除
    addrid = request.POST.get("id")
    consignee = Consignee.objects.filter(pk=addrid)
    consignee.delete()
    #返回id回去页面隐藏
    return JsonResponse({"status":addrid})

#默认收货信息
def addrchose(request):
    # 获取token
    try:
        token = request.session.get("token")
    except:
        token = None
    # 如果token不为空
    if token:
        #获取token对应的用户账号及默认地址对应id
        useraccount = User.objects.get(userToken=token).userAccount
        addrid = request.POST.get("id")
        #删除原默认地址
        try:
            defaultaddr = Defaultaddr.objects.get(userAccount = useraccount)
            defaultaddr.delete()
        except:
            pass
        #保存默认地址
        defaultaddr = Defaultaddr()
        defaultaddr.userAccount = useraccount
        defaultaddr.defaultaddr = addrid
        defaultaddr.save()
        return redirect("/cart/")
    # 没有获取到token返回登录页面
    else:
        return redirect("/login/")

def order(request,type):
    # 获取token
    try:
        token = request.session.get("token")
    except:
        token = None
    # 如果token不为空
    if token:
        # 获取token对应的用户账号
        user = User.objects.get(userToken=token)
        #如果是POST请求，保存订单
        if request.method == "POST":
            progressLongStr = request.POST.get("ids")
            #生产订单号
            orderid = ''.join(str(uuid.uuid4()).split('-'))
            #用户账号
            userid = user.userAccount
            #默认地址id
            consigneeid = Defaultaddr.objects.get(userAccount=userid).defaultaddr
            #保存订单对象信息
            consignee = Consignee.objects.get(pk=consigneeid)
            consigneeName = consignee.consigneeName
            consigneeTel = consignee.consigneeTel
            consigneeAddr = consignee.consigneeAddr

            order = Order.createorder(orderid,userid,consigneeName,consigneeTel,consigneeAddr,progressLongStr,False)
            order.save()
            #删除购物车信息
            itemList = progressLongStr.split("*")  # item = [id1_num1,id2_num2]
            itemList.pop()
            for item in itemList:
                i = item.split("_")  # i = [id,num]
                productid = i[0]
                try:
                    product = Cart.objects.get(userAccount=userid,productid=productid,productnum=i[1])
                    product.delete()
                except Cart.DoesNotExist as e:
                    pass
            #POST请求结束
            return redirect("/order/0/")
        else:
            userid = user.userAccount
            #全部订单
            if type == 0:
                orders = Order.objects.filter(userid=userid)
            #待付款订单
            elif type == 1:
                orders = Order.objects.filter(userid=userid,payment=False)
            # 待收货订单
            elif type ==2:
                orders = Order.objects.filter(userid=userid, payment=True,orderstatus="待收货")
            #退货订单
            elif type == 3:
                orders = Order.objects.filter(userid=userid, payment=True,orderstatus="退货")
            return render(request, "order.html",{"orders":orders})
    else:
        return redirect("/login/")

def getorder(request):
    orderid = request.POST.get("orderid")
    order = Order.objects.get(orderid=orderid)
    LongStr = order.progressStr
    itemList = LongStr.split("*")#item = [id1_num1,id2_num2]
    itemList.pop()
    products = []
    for item in itemList:
        i =item.split("_")#i = [id,num]
        productid = i[0]
        productinfo = {}
        orderpro = Goods.objects.get(productid=productid)
        productinfo["name"]=orderpro.productlongname
        print(i[1])
        productinfo["num"] = i[1]
        productinfo["price"] = orderpro.price
        productinfo["img"] = orderpro.productimg
        products.append(productinfo)
    return JsonResponse({"data":products})

#删除订单
def delorder(request):
    orderpk = request.POST.get("id")
    order = Order.objects.get(pk=orderpk)
    orderid = order.orderid
    order.delete()
    #返回orderid到js消除页面中的订单
    return JsonResponse({"status":orderid})

#判断订单状态
def status(request,type):
    id = request.POST.get("id")
    order = Order.objects.get(pk = id)
    if type == 0:
        #订单已付款，待收货
        order.payment = True
    elif type == 1:
        #订单已收货
        order.orderstatus = "已收货"
    elif type == 2:
        #订单退货
        order.orderstatus = "退货"
    order.save()
    return JsonResponse({"status":id})

#评论
def comment(request):
    #获取用户信息
    token = request.session.get("token")
    user = User.objects.get(userToken=token)
    #将订单中的商品分别以字典保存到列表
    products = []
    #获取所有待评论订单
    orders = Order.objects.filter(userid=user.userAccount,orderstatus="已收货")
    #循环所有订单，将订单内的商品提出
    for order in orders:
        orderid = order.orderid
        LongStr = order.progressStr
        itemList = LongStr.split("*")#[*productid_productnum]
        #循环订单内的所有商品，添加到products列表
        for item in itemList:
            if item:
                product = item.split("_")
                productid = product[0]
                productinfo = {}
                good = Goods.objects.get(productid=productid)
                #判断商品是否已经评论，如果已经评论，不操作
                try:
                    testcomm = Comment.objects.get(orderid=orderid,productid=good.productid)
                #商品未评论，保存到列表
                except:
                    productinfo["orderid"] = orderid
                    productinfo["name"] = good.productname
                    productinfo["img"] = good.productimg
                    productinfo["num"] = product[1]
                    productinfo["price"] = good.price
                    productinfo["productid"] = good.productid
                    products.append(productinfo)
    #将商品列表返回页面渲染
    return render(request,"comment.html",{"title":"待用户评论","products":products})

#保存评论
def savecomm(request):
    # 获取用户信息
    token = request.session.get("token")
    user = User.objects.get(userToken=token)
    #将评论保存到数据库
    comment = Comment()
    comment.userAccount = user.userAccount
    comment.comment = request.POST.get("comment")
    comment.productid = request.POST.get("productid")
    comment.orderid = request.POST.get("orderid")
    comment.userName = user.userName
    comment.save()
    return JsonResponse({})

def goodsinfo(request,goodsid):
    goods = Goods.objects.get(productid=goodsid)
    comments = Comment.objects.filter(productid=goodsid)
    return render(request,"goodsinfo.html",{"goodsinfo":goods,"comments":comments})





