var page = 1;
var domain = "http://localhost:8000";
var enable_pull = false;
var author = "all";
var node = 1;
var author_list = new Array();


//加载视频列表
function load_videos(){
    $("#author_list").fadeOut();
    $("#follow").fadeOut();
    $("#load").fadeIn();
    var url = domain +"/get_list/?node=" + node + "&author=" + author + "&page=" + page++;
    $.ajax({
        url : url,
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
            } else {
                alert("error error code" + obj.code);
            }
            $("#load").fadeOut();
        }});
}

//加载flash
function load_flash(id) {
    $("#flash").html("正在加载。。。");
    $('#flash').html(
        '<p><object type="application/x-shockwave-flash" data="http://static.youku.com/v1.0.0310/v/swf/loader.swf" width="480" height="400" id="movie_player">' +
            '<param name="allowFullScreen" value="true">' +
            '<param name="allowscriptaccess" value="always">' +
            '<param name="flashvars" value="VideoIDS=XNTA3OTAxNTcy&amp;ShowId=0&amp;' +
            'category=91&amp;Cp=0&amp;Light=on&amp;THX=off&amp;unCookie=0&amp;' +
            'frame=0&amp;pvid=136359071463108P&amp;Tid=0&amp;isAutoPlay=true&amp;Version=/v1.0.0843&amp;' +
            'show_ce=0&amp;winType=interior&amp;embedid=AjEzMjA3NzA4MgJuZXdzLnlvdWt1LmNvbQIvbGlhbmdodWkyMDEz&amp;' +
            'vext=bc%3D%26pid%3D%26unCookie%3D0%26frame%3D0%26type%3D0%26svt%3D0%26emb%3DAjEz' +
            'MjA3NzA4MgJuZXdzLnlvdWt1LmNvbQIvbGlhbmdodWkyMDEz%26dn%3D%E7%BD%91%E9%A1%B5%26hwc%3D1%26mtype%3Doth">'+
            '<param name="movie" value="http://player.opengg.me/loader.swf">' +
            '<div class="player_html5"><div class="picture" style="height:100%">' +
            '<div style="line-height:460px;">' +
            '<span style="font-size:18px">您还没有安装flash播放器,请点击<a href="http://www.adobe.com/go/getflash" target="_blank">这里</a>安装' +
            '</object></p>'
    );
}

//加载作者列表
function load_authors() {
    var html = "";
    $.ajax({
        url : domain + "/get_author_list",
        success : function(data) {
            $("#author_list").append(function(){
                var obj = jQuery.parseJSON(data);
                for(var i = 0; i < obj.list.length; ++i) {
                    html += '<div class="author" id="' + obj.list[i].id + '"><div class="author_name">' + obj.list[i].name + '</div>';
                    if(is_followed(obj.list[i].id) != null) {
                        html += '<div class="follow">取消关注</div>';
                    } else {
                        html += '<div class="follow">点击关注</div>';
                    }
                    html += '<div class="author_love">love:' + obj.list[i].love + "</div>";
                    html += '<div class="author_avatar"><img src="/img/dog.jpg"></div>';
                    html += '<div class="author_description">' + obj.list[i].description + '</div></div>';
                }
                return html;
            });
        }
    });
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

//喜欢
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


//关注后更新关注列表
//{u'UMjU3MzI2NDMy': {'last_view': 9999999999, 'author_name': u'\u5c0f\u6ee1'}, u'123123': {'last_view': 9999999999, 'author_name': u'dfsdf'}}
function update_follow_list() {
    $("#follow_list").html("ddd");
    //获取作者列表  id 名字 时间
    //var author_list = new Array();
    var follow_dict = $.cookie("follow_dict");
    var reg = /u'(\w+)?':\s/g;
    var arr;
    while((arr = reg.exec(follow_dict)) != null) {
        var temp = new Array();
        temp['id'] = arr[1];
        author_list.push(temp);
    }
    reg = /'author_name':\su'(\S+)'}/g;
    var i = 0;
    while((arr = reg.exec(follow_dict)) != null) {
        author_list[i]['name'] = unescape(arr[1].replace(/\\u/g, "%u"));
        i++;
    }
    //显示

}

//获取更新视频数量
function get_update_video_number() {

}

//是否关注
function is_followed(id) {
    var follow_dict = $.cookie('follow_dict');
    return follow_dict.match(id);
}

//关注
function follow(dom) {
    var author_id = $(dom).parent().attr("id");
    var author_name = $(dom).prev().text();
    var csrftoken = $.cookie('csrftoken');
    alert($.cookie('follow_dict'));
    $.ajax({
        url : domain + "/follow/",
        type : 'post',
        data : {
            'csrfmiddlewaretoken' : csrftoken,
            'author_id' : author_id,
            'author_name' : author_name
        },
        error : function(data) {
            alert(data);
        },
        success : function(data) {
            obj = $.parseJSON(data);
            var cookies = obj.cookies;
            if(obj.code == 4001) {
                $(dom).text("取消关注");
                $.cookie('follow_dict', null, { path : "/"});
                $.cookie('follow_dict', cookies, { path : "/"});
            }
            if(obj.code == 4002) {
                $(dom).text("点击关注");
                $.cookie('follow_dict', null, { path : "/"});
                $.cookie('follow_dict', cookies, { path : "/"});
            }
        }
    });

}


//瀑布流
window.onscroll = function(){
    var a = document.documentElement.scrollTop == 0 ? document.body.clientHeight : document.documentElement.clientHeight;
    var b = document.documentElement.scrollTop == 0 ? document.body.scrollTop : document.documentElement.scrollTop;
    var c = document.documentElement.scrollTop == 0 ? document.body.scrollHeight : document.documentElement.scrollHeight;
    if((a + b == c) && enable_pull == true){
        load_videos();
    }
}

$(document).ready(function(){
    //test
    alert('');
    $.ajax({
        type:'get',
        url:'http://localhost:8000/test',
        dataType:'jsonp',
        jsonp:"callback",
        jsonpCallback:"cccc",
        //data:{"a":"insert", "type":"aa", "time":"bb", "id":"dd", "allowVote":"cc"},
        async: false,
        error: function(data) {
          alert(data);
        },
        success:function(data){
            alert("ddd");
        }
    })



    //加载作者
    load_authors();

    //加载关注列表
    update_follow_list();

    //返回
    $('#glance_return').click(function() {
        enable_pull = false;
        $("#author_list").fadeIn();
        $("#left").fadeIn();
        $("#videos").fadeOut();
    });

    //随便看看
    $('#glance').click(function() {
        $("#videos").fadeIn();
        $("#videos").html("");
        author = "all";
        page = 1;
        load_videos();
        enable_pull = true;
    });

    //作者
    $(document).on("click", ".author_name", function() {
        $("#videos").fadeIn();
        $("#videos").html("");
        author  = $(this).parent().attr("id");
        page = 1;
        load_videos();
        enable_pull = true;
    });

    //视频
    $(document).on("click", ".thumbnail", function() {
        var id = $(this).parent().attr("id");
        load_flash(id);
        load_comment(id);
        $("#video_detail").fadeIn();
    });

    //视频喜欢
    $(document).on("click", ".love", function() {
        love(this);//此处需要得到love的ID
    });

    //关注
    $(document).on("click", ".follow", function() {
        follow(this);
    });

    //返回
    $('#return').click(function() {
        $("#video_detail").fadeOut();
    });

});