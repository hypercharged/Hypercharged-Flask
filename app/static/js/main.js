var isPreserved = false;
$(document).ready(function(){
    try {
        if (document.cookie.split("mode=")[1] == "true" || document.cookie.split("mode=")[1] == "false") {
            isPreserved = true;
            toggleMode(document.cookie.split("mode=")[1]=="true");
        }
    }
    catch {

    }
    $('.modal').modal();
    new WOW().init();
  });
$(".switch").find("input[type=checkbox]").on("change",function() {
    var status = $(this).prop('checked');
    document.cookie = "mode="+status;
    toggleMode(status);
});
function toggleMode(status) {
    if (status) {
        $('body').removeClass("white");
        $('body').addClass("black");
        $(".black-text").addClass("white-text");
        $(".black-text").removeClass("black-text");
        $("#logo").attr("src","/static/assets/hctransparentdark.png");
        $(".lever").removeClass("blue");
        $(".lever").addClass("red");
    }
    else {
        $('body').addClass("white");
        $('body').removeClass("black");
        $(".white-text").addClass("black-text");
        $(".white-text").removeClass("white-text");
        $("#logo").attr("src","/static/assets/hctransparent.png")
        $(".lever").addClass("blue");
        $(".lever").removeClass("red");

    }
    $('.switch').prop('checked', true);
  }