$(function(){
    $("a", ".accordion").click(function(e) {
        $("#ajax-content").load($(this).attr("href")); });      

    
});