$(document).ready(function(){
	
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
}
	
	$(".selectaddr").bind("click",function(){
		orderid = $(this).attr("id")
		if($("#orderpro"+orderid).text()){
			$("#orderpro"+orderid).text("")
		}else{
		$.post("/getorder/",{"orderid":orderid},function(data){
			product = data.data
			$("#orderpro"+orderid).text("订单详情")
			$("#orderpro"+orderid).append("<hr/ size='2px' noshade=false>")
			for(i=0;i<product.length;i++){
				$("#orderpro"+orderid).append("<li class='name'>"+"商品名称："+product[i].name+"</li>")
				$("#orderpro"+orderid).append('<img class="img" src="'+product[i].img+'"/>')
				$("#orderpro"+orderid).append("<li class='num'>"+"商品数量："+product[i].num+"</li>")
				$("#orderpro"+orderid).append("<li class='price'>"+"商品总价："+mul(product[i].price,parseInt(product[i].num))+"</li>")
				$("#orderpro"+orderid).append("<hr/ size='2px' noshade=false>")
				
			}
		})
		}
	})
	$(".delorder").click(function(event){
		id = $(this).attr("id")
		$.post("/delorder/",{"id":id},function(data){
			if(data.status){
			$("#"+data.status).hide()
			}
		})
		event.stopPropagation();
	})
	$(".buy").click(function(event){
		if ($(this).text()=="付款"){
		id = ($(this).attr("id").split("buy"))[0]
		$.post("/status/0/",{"id":id},function(data){
			if(data.status){
			$("#"+data.status+"buy").text("已付款")
			}
		})}else{
			alert("已付款，无需重复操作")
		}
		event.stopPropagation();
	})
	$(".iget").click(function(event){
		id = ($(this).attr("id").split("get"))[0]
		$.post("/status/1/",{"id":id},function(data){
			if(data.status){
			$("#"+data.status+"get").text("已收货")
			$("#"+data.status).remove()
			}
		})
		event.stopPropagation();
	})
	$(".rebake").click(function(event){
		id = $(this).attr("id")
		$.post("/status/2/",{"id":id},function(data){
			if(data.status){
			$("#"+data.status).text("已退货")
			$("#"+data.status+"get").remove()
			}
		})
		event.stopPropagation();
	})
	
})
