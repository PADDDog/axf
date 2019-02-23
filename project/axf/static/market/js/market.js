$(document).ready(function(){
    $(".addShopping").bind("click", function () {
        //$(this).attr("ga")
        var ppp = $(this).attr("ga")
        // var innum = parseInt($("#" + ppp + "").text()) + 1
        $('[ga="' + ppp + '"][class="subShopping"]').show()

		$.post("/changecart/0/",{"productid":ppp},function (data) {
			if (data.status == "success") {
                $("#" + ppp + "").text("" + data.data)
                $("#" + ppp + "").show()
            }else if (data.status == "max") {
			    $("#" + ppp + "").text("" + data.data)
                $("#" + ppp + "").show()
                $('[ga="' + ppp + '"][class="addShopping"]').hide()
            }
            else {
                if (data.data == -1){
					window.location.href = "http://localhost:8000/login/"
				}
			}
        })
    })
    $(".subShopping").bind("click", function () {
        var ppp = $(this).attr("ga")
		$.post("/changecart/1/",{"productid":ppp},function (data) {
			if (data.status == "success") {
			    if(data.data > 0) {
                    $("#" + ppp + "").text("" + data.data)
                    $("#" + ppp + "").show()
                    $('[ga="' + ppp + '"][class="addShopping"]').show()
                }
                else if (data.data == 0){
			        $("#" + ppp + "").hide()
                    $('[ga="' + ppp + '"][class="subShopping"]').hide()
                }
            }else {
			    $(this).hide()
                $("#" + ppp + "").hide()
				if (data.data = -1){
					window.location.href = "http://localhost:8000/login/"
				}
			}
        })
    })

    $("#typediv").hide()
    $("#sortdiv").hide()
    $("#alltypebtn").click(function () {
        $("#typediv").show(),
            $("#sortdiv").hide()
    })
    $("#showsortbtn").click(function () {
        $("#sortdiv").show(),
            $("#typediv").hide()
    })
    $("#typediv").click(function () {
        $("#typediv").hide()
    })
    $("#sortdiv").click(function () {
        $("#sortdiv").hide()
    })
})
