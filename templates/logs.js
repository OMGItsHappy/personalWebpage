$(document).ready(function(){
    $(".btn").click(function(){
        $.ajax({
            url : "/1.18",
            type : "get",
            contentType : "application/json",
            data : {
                button_text : $(this).text()
            },
            
            success : function(response){
                $(".btn").text("hello")
            }
        })
    })
})