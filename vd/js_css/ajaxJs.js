var page = 1

function load(){
    $("#load").fadeIn();
    $.ajax({
        url : "http://localhost:8000/get_list/?page="+page++,
        success : function(data) {
            var obj = jQuery.parseJSON(data)
            if(obj.code == 200){
                $("#videos").append(function(){
                    var text = '';
                    for(var i=0; i< obj.list.length;i++){
                        text += "<div class='video' id='" + obj.list[i].id +"'>";
                        text += "<div class='title'>" + obj.list[i].title + "| love:" + obj.list[i].love + "</div>";
                        text += "<div class='published'>发布时间:" + obj.list[i].published + "</div>";
                        text += "<div class='duration'>视频时长:" + obj.list[i].duration + "</div>";
                        text += "<div class='thumbnail'> <a href='http://cuit.sinaapp.com/player_ss.swf?VideoIDS=" + obj.list[i].id+"'>";
                        text += "<img src=" + obj.list[i].thumbnail + " /></a></div>";
                        text += "<div class='description'>" + obj.list[i].description + "</div>";
                        text += "</div>";
                    }
                    return text;
                });
            }
            $("#load").fadeOut();
        }});
}

function update_url(id) {
    $("#flash").html(
        '<p><object width="480" height="400" classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0" align="middle"><param name="allowfullscreen" value="true"><param name="quality" value="high"><param name="allowscriptaccess" value="always"><embed width="480" height="400" type="application/x-shockwave-flash" ' +
            'src="http://player.opengg.me/player.php/sid/' + id +
            '/v.swf" allowfullscreen="true" quality="high" allowscriptaccess="always" align="middle"><param name="src" value="http://player.opengg.me/player.php/sid/' + id +
            '/v.swf"></object></p>');

}

window.onscroll=function(){
    var a = document.documentElement.scrollTop==0? document.body.clientHeight : document.documentElement.clientHeight;
    var b = document.documentElement.scrollTop==0? document.body.scrollTop : document.documentElement.scrollTop;
    var c = document.documentElement.scrollTop==0? document.body.scrollHeight : document.documentElement.scrollHeight;
    if(a+b==c){
        $.ajax({
            url : "http://localhost:8000/get_list/?page="+page++,
            success : load()
        });
    }
}

$(document).ready(function(){
    load();
    $(document).on("click", ".title", function() {
        update_url($(this).parent().attr("id"));
        //$("#videos").fadeOut();
        $("#video_detail").fadeIn();
    })
    $('#return').click(function() {
        //$("#videos").fadeIn();
        $("#video_detail").fadeOut();
    });
});