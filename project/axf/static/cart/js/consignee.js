$(document).ready(function(){

$("#subm").bind("click",function(){
	if($("#conname").val()==""||$("#conname").val()==null){
		$("#noname").show()
	}
	if($("#conphone").val()==""||$("#conphone").val()==null){
		$("#nophone").show()
	}
	if($("#conaddr").val()==""||$("#conaddr").val()==null){
		$("#noaddr").show()
	}
	else{
		$("#theform").submit()
	}
})

$("#conname").bind("blur",function(){
	console.log("3456787654")
	if($("#conname").val()==""||$("#conname").val()==null){
		$("#noname").show()
	}
})

$("#conphone").bind("blur",function(){
	if($("#conphone").val()==""||$("#conphone").val()==null){
		$("#nophone").show()
	}
})

$("#conaddr").bind("blur",function(){
	if($("#conaddr").val()==""||$("#conaddr").val()==null){
		$("#noaddr").show()
	}
})

$("#conname").bind("focus",function(){
	$("#noname").hide()
})

$("#conphone").bind("focus",function(){
	$("#nophone").hide()
})

$("#conaddr").bind("focus",function(){
		$("#noaddr").hide()
})
})
