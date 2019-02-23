var isPreserved = false;
$(document).ready(function(){
    try {
        if ($.cookie("nightMode") != null) {
            isPreserved = true;
            toggleMode($.cookie("nightMode"));
        }
    }
    catch {

    }
    $('.modal').modal();
    new WOW().init();
  });
$(".switch").find("input[type=checkbox]").on("change",function() {
    let status = $(this).prop('checked');
    $.removeCookie("nightMode");
    $.cookie("nightMode", status, {
        expires: 365*20,
        path: '/'
    });
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