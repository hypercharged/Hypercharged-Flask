  $(document).ready(function(){
    $('.modal').modal();
    new WOW().init();
  });
$(".switch").find("input[type=checkbox]").on("change",function() {
    var status = $(this).prop('checked');
    if (status) {
        $('body').removeClass("white");
        $('body').addClass("black");
        $(".black-text").addClass("white-text");
        $(".black-text").removeClass("black-text");
        $("#logo").attr("src","/static/assets/hctransparentdark.png")
    }
    else {
        $('body').addClass("white");
        $('body').removeClass("black");
        $(".white-text").addClass("black-text");
        $(".white-text").removeClass("white-text");
    }
});