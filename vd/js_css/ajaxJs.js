var page = 1

function load_videos(){
    $("#load").fadeIn();
    $.ajax({
        url : "http://dota.idealweb.cn/get_list/?page="+page++,
        success : function(data) {
            var obj = jQuery.parseJSON(data);
            if(obj.code == 200){
                $("#videos").append(function(){
                    var text = '';
                    for(var i=0; i< obj.list.length;i++){
                        text += "<div class='video' id='" + obj.list[i].id +"'>";
                        text += "<div class='title'>" + obj.list[i].title + "| love:" + obj.list[i].love + "</div>";
                        text += "<div class='published'>发布时间:" + obj.list[i].published + "</div>";
                        text += "<div class='duration'>视频时长:" + obj.list[i].duration + "</div>";
                        text += "<div class='thumbnail'>";
                        text += "<img src=" + obj.list[i].thumbnail + " /></div>";
                        text += "<div class='description'>" + obj.list[i].description + "</div>";
                        text += "</div>";
                    }
                    return text;
                });
            }
            $("#load").fadeOut();
        }});
}

function load_flash(id) {
    $("#flash").html("正在加载。。。");
    $("#flash").html(
        '<p><object width="480" height="400" classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0" align="middle"><param name="allowfullscreen" value="true"><param name="quality" value="high"><param name="allowscriptaccess" value="always"><embed width="480" height="400" type="application/x-shockwave-flash" ' +
            'src="http://player.opengg.me/player.php/sid/' + id +
            '/v.swf" allowfullscreen="true" quality="high" allowscriptaccess="always" align="middle"><param name="src" value="http://player.opengg.me/player.php/sid/' + id +
            '/v.swf"></object></p>');
}

function load_comment(id) {
    $("#comment").html("正在加载。。。分页没做，评论没做");
    $.ajax({
        url : "https://openapi.youku.com/v2/comments/by_video.json?client_id=74f3668e4f16ef9f&count=30&video_id=" + id +"&page=1",
        success : function(data) {
            var text = "";
            for (var i = 0; i < data.comments.length; ++i) {
                text += (i+1) + ":" + data.comments[i].user.name + ":" + data.comments[i].content + "\n\n";
            }
            $("#comment").html(text);
        }
    });
}

window.OnScroll = function(){
    var a = document.documentElement.scrollTop==0? document.body.clientHeight : document.documentElement.clientHeight;
    var b = document.documentElement.scrollTop==0? document.body.scrollTop : document.documentElement.scrollTop;
    var c = document.documentElement.scrollTop==0? document.body.scrollHeight : document.documentElement.scrollHeight;
    if(a+b==c){
        $.ajax({
            url : "http://localhost:8000/get_list/?page="+page++,
            success : load_videos()
        });
    }
}

$(document).ready(function(){
    $("#videos").html("正在加载》》》");
    load_videos();
    $(document).on("click", ".thumbnail", function() {
        var id = $(this).parent().attr("id");
        load_flash(id);
        load_comment(id);
        $("#video_detail").fadeIn();
    });
    $('#return').click(function() {
        $("#video_detail").fadeOut();
    });
});