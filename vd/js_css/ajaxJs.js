var page = 1

function load(){
    $.ajax({
        url : "http://localhost:8000/get_list/?page="+page++,
        success : function(data) {
            var obj = jQuery.parseJSON(data)
            if(obj.code == 200){
                $("#videos").append(function(){
                    var text = '';
                    for(var i=0; i< obj.list.length;i++){
                        text += "<div class='video'>";
                        text += "<div class='title'>" + obj.list[i].title + "</div>";
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
        }});
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
});