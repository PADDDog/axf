$(document).ready(function () {
// 浮点数求和
function add(a, b) {
    var c, d, e;
    try {
        c = a.toString().split(".")[1].length;
    } catch (f) {
        c = 0;
    }
    try {
        d = b.toString().split(".")[1].length;
    } catch (f) {
        d = 0;
    }
    return e = Math.pow(10, Math.max(c, d)), (mul(a, e) + mul(b, e)) / e;
}

// 浮点数相减
function sub(a, b) {
    var c, d, e;
    try {
        c = a.toString().split(".")[1].length;
    } catch (f) {
        c = 0;
    }
    try {
        d = b.toString().split(".")[1].length;
    } catch (f) {
        d = 0;
    }
    return e = Math.pow(10, Math.max(c, d)), (mul(a, e) - mul(b, e)) / e;
}

// 浮点数相乘
function mul(a, b) {
    var c = 0,
        d = a.toString(),
        e = b.toString();
    try {
        c += d.split(".")[1].length;
    } catch (f) {}
    try {
        c += e.split(".")[1].length;
    } catch (f) {}
    return Number(d.replace(".", "")) * Number(e.replace(".", "")) / Math.pow(10, c);
}

// 浮点数相除
function div(a, b) {
    var c, d, e = 0,
        f = 0;
    try {
        e = a.toString().split(".")[1].length;
    } catch (g) {}
    try {
        f = b.toString().split(".")[1].length;
    } catch (g) {}
    return c = Number(a.toString().replace(".", "")), d = Number(b.toString().replace(".", "")), mul(c / d, Math.pow(10, f - e));
}

// 点击加号情况
    $(".addShopping").bind("click", function () {
        var ppp = $(this).attr("ga")
        $('[ga="' + ppp + '"][class="subShopping"]').show()
		$.post("/changecart/0/",{"productid":ppp},function (data) {
		    if (data.status == "max"){
                $("#" + ppp + "").text("" + data.data)
                $("#" + ppp + "").show()
                $('[ga="' + ppp + '"][class="addShopping"]').hide()
                $("#"+ ppp +"price").text(mul(data.hoprice,parseInt(data.data)))
            }
			else if (data.status == "success") {
				$("#sum0").text(add($("#sum0").text(),data.hoprice))
                $("#" + ppp + "").text("" + data.data)
                $("#" + ppp + "").show()
                $("#"+ ppp +"price").text(mul(data.hoprice,parseInt(data.data)))
                if ($("#"+ppp+"a").text() == "√"){
                	$("#sum").text(add($("#sum").text(),data.hoprice))
                }
           }
        })
    })
// 点击减号情况 
    $(".subShopping").bind("click", function () {
        var ppp = $(this).attr("ga")
        $('[ga="' + ppp + '"][class="addShopping"]').show()
		$.post("/changecart/1/",{"productid":ppp},function (data) {
			if (data.status == "success"||data.status == "max") {
			    if(data.data > 0) {
			    	$("#sum0").text(sub($("#sum0").text(),data.hoprice))
                    $("#" + ppp + "").text("" + data.data)
                    $("#"+ ppp +"price").text(mul(data.hoprice,parseInt(data.data)))
                    $("#" + ppp + "").show()
                    if ($("#"+ppp+"a").text() == "√"){
                    	$("#sum").text(sub($("#sum").text(),data.hoprice))
                    }
                }
                else if (data.data == 0){
			        if ($("#"+ppp+"a").text() == "√"){
                	$("#sum").text(sub($("#sum").text(),data.hoprice))}
                	$("#sum0").text(sub($("#sum0").text(),data.hoprice))
                    $("#"+ ppp +"li").hide()
                }
            }
        })
    })
// 点击全选情况
	$("#allturespan").bind("click",function(){
		if($("#isallture").text()=="√"){
			$(".isture").text("")
			$("#isallture").text("")
			$("#sum").text("0")
			$(".isture").attr("isget","notget")
		}
		else{
			$(".isture").text("√")
			$("#isallture").text("√")
			$("#sum").text($("#sum0").text())
			$(".isture").attr("isget","isget")
		}
	})
//自定义选择情况
	$(".ischose").bind("click",function(){
		var chose = $(this).attr("goodsid")
		if ($("#"+chose+"a").text() == "√"){
			$("#"+chose+"a").text("")
			$("#sum").text(sub($("#sum").text(),$("#"+chose+"price").text()))
			$("#"+chose+"a").attr("isget","notget")
		}else{
			$("#"+chose+"a").text("√")
			$("#sum").text(add($("#"+chose+"price").text(),$("#sum").text()))
			$("#"+chose+"a").attr("isget","isget")
		}
	})
	
//选择完毕
	$("#ok").bind("click",function(){
		is = $("[isget='isget']")
		ids= ""
		for(i = 0;i<is.length;i++){
			ids = ids + $(is[i]).attr("ga") + "*"
		}
		console.log(ids)
		$.post("/order/0/",{"ids":ids},function(){
			for(i = 0;i<is.length;i++){
				$(is[i]).parent().parent().parent().hide()
				window.location.href = "http://localhost:8000/cart/"
			}
		})
	})
})
