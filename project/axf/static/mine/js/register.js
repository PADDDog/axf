$(document).ready(function(){
    $("#accunt").bind("focus",function () {
        $("#accunterr").hide()
        $("#checkerr").hide()
        $(".subm").attr("disabled",false)
    })
    $("#accunt").bind("blur",function(){
    	instr = this.value
    	if(instr.length < 6 || instr.length > 12){
    	$("#accunterr").show()
    	return
    	}
    	$.post("/checkuserid/",{"userid":instr},function(data){
    		if(data.status == "error"){
    			$("#checkerr").show()
    			$(".subm").attr("disabled","disabled")
    		}
    	})
    })
    $("#pass").blur(function(){
    	instr = this.value
    	if(instr.length < 6 || instr.length > 16){
    	$("#passerr").show()
    	return
    	}
    })
    $("#pass").focus(function(){
    	$("#passerr").hide()
    	return
    })
    $("#passwd").blur(function(){
//  	console.log($("#passwd").val(),$("#pass").val())
    	if($("#passwd").val() != $("#pass").val()){
    	$("#passwderr").show()
    	$(".subm").attr("disabled","disabled")
    	return
    	}
    })
    $("#passwd").focus(function(){
    	$("#passwderr").hide()
    	$(".subm").attr("disabled",false)
    	return
    })

})