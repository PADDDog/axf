$(document).ready(function(){
	//绑定提交按钮
	$(".but").click(function(){
		//获取商品ID、订单ID及评论内容comm
		productid = $(this).attr("id")
		orderid = $(this).attr("ord")
		comm = $("#"+productid+"text").val()
		$.post("/savecomm/",{"comment":comm,"productid":productid,"orderid":orderid},function(){
			$("#"+productid+"ul").remove()
		})
	})
})
