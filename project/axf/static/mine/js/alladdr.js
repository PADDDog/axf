$(document).ready(function(){
	$(".deladdr").click(function(event){
		id = $(this).attr("id")
		$.post("/deladdr/",{"id":id},function(data){
			if (data.status){
				$("#"+data.status+"id").hide()
			}
		})
		event.stopPropagation();
	})
	$(".back").click(function () {
		window.location.href = "http://localhost:8000/mine/"
    })
	$(".selectaddr").click(function () {
		id = $(this).attr("ga")
		$.post("/addrchose/",{"id":id},function (data) {
			window.location.href ="http://localhost:8000/cart/"
            }

		)
    })
})
