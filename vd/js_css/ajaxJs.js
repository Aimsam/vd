var page = 1;
var domain = "http://192.168.1.112:8000";

//加载视频列表
function load_videos(){
    $("#load").fadeIn();
    $.ajax({
        url : domain +"/get_list/?page=" + page++,
        success : function(data) {
            var obj = jQuery.parseJSON(data);
            if(obj.code == 200){
                $("#videos").append(function(){
                    var text = '';
                    for(var i=0; i< obj.list.length;i++){
                        text += "<div class='video' id='" + obj.list[i].id +"'>";
                        text += "<div class='title'>" + obj.list[i].title + "</div>";
                        text += "<div class='love'>" + "love:" + obj.list[i].love + "</div>";
                        text += "<div class='published'>发布时间:" + obj.list[i].published + "</div>";
                        text += "<div class='duration'>视频时长:" + obj.list[i].duration + "</div>";
                        text += "<div class='thumbnail'> ";
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

//加载flash
function load_flash(id) {
    $("#flash").html("正在加载。。。");
    $("#flash").html(
        '<p><object width="480" height="400" classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0" align="middle"><param name="allowfullscreen" value="true"><param name="quality" value="high"><param name="allowscriptaccess" value="always"><embed width="480" height="400" type="application/x-shockwave-flash" ' +
            'src="http://player.opengg.me/player.php/sid/' + id +
            '/v.swf" allowfullscreen="true" quality="high" allowscriptaccess="always" align="middle"><param name="src" value="http://player.opengg.me/player.php/sid/' + id +
            '/v.swf"></object></p>');
}

//加载评论
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

function love(dom) {
    var id = $(dom).parent().attr("id");
    $.ajax({
        url : domain + "/love/" + id,
        success : function(data) {
            obj = $.parseJSON(data);
            switch (obj.code) {
                case 100 :
                    $(dom).html("love:" + (parseInt($(dom).html().substr(5, 6)) + 1));
                    break;
                case 101 :
                    alert("id is empty");
                    break;
                case 102 :
                    alert("id is not exit");
                    break;
                case 103 :
                    alert("亲！注意节奏！");
                    break;
            }
        }
    });
}

//瀑布流
window.onscroll = function(){
    var a = document.documentElement.scrollTop == 0 ? document.body.clientHeight : document.documentElement.clientHeight;
    var b = document.documentElement.scrollTop == 0 ? document.body.scrollTop : document.documentElement.scrollTop;
    var c = document.documentElement.scrollTop == 0 ? document.body.scrollHeight : document.documentElement.scrollHeight;
    if(a + b == c){
        load_videos();
    }
}


$(document).ready(function(){
    load_videos();

    $(document).on("click", ".thumbnail", function() {
        var id = $(this).parent().attr("id");
        load_flash(id);
        load_comment(id);
        $("#video_detail").fadeIn();
    });

    $(document).on("click", ".love", function() {
        love(this);//此处需要得到love的ID
    });

    $('#return').click(function() {
        $("#video_detail").fadeOut();
    });
});