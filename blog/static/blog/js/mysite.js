/*The js for zzzzer's blog.*/

$(function() {
    // markdown图片自适应
    $(".main-content img").addClass("img-responsive");


    // 回到顶部按钮淡入淡出
    $(window).scroll(function() {
        if ($(window).scrollTop() >= 500) {
            $(".go-top").fadeIn(500);
        } else {
            $(".go-top").fadeOut(500);
        }
    });


    // 回到顶部功能
    $(".go-top").click(function() {
        $('html, body').animate({scrollTop: 0}, 700);
    });


    // 点赞按钮
    $("#like").click(function() {
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        // var pk = document.getElementById('like').name;
        var pk = $('#like').attr('name');
        // like后面要加'/'，否则会引发301
        $.post('/like/', {
                'csrfmiddlewaretoken':csrftoken,
                'pk': pk
            },
            function(data) {
                // 点赞动画
                $("body").append("<span id='num'>+1</span>");
                var $obj = $("#like");
                var $box = $("#num");
                var left = $obj.offset().left + $obj.width() / 2;
                var top = $obj.offset().top - $obj.height();
                $box.css({
                    "position": "absolute",
                    "left": left + "px",
                    "top": top + "px",
                    "font-size": '12px',
                    "color": "red"
                });
                $box.animate({
                        "font-size": '22px',
                        "opacity": "0.7",
                        "top": top - 30 + "px"
                    }, 
                    500, 
                    function() {
                        $box.remove();
                    }
                ); 
                $(".post-likes").text(data);
                $obj.prop("disabled", true);
            }
        );
    });


    // 生成验证码
    $('.comment-area').bind('click', function() {
        // 解绑事件
        $(this).unbind('click');
        $('.captcha').attr('src', '/captcha/');
    });


    // 刷新验证码
    $('.captcha').click(function() {
        var src = $(this).attr('src');
        $(this).attr('src', src + '?');
        alert('已刷新~');
    });


    // 提交评论
    $(".comment-btn").click(function() {
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var pk = $('#like').attr('name');
        var code = $('.code').val();
        var name = $('.user-name').val();
        var email = $('.user-email').val();
        var url = $('.user-url').val();
        var text = $('.comment-area').val();
        if (name.length == 0) {
            alert('你忘记输昵称了^_^');
        } else if (text.length == 0) {
            alert('你忘记写评论了^_^');
        } else if (code.length != 4) {
            alert('验证码啊...');
        } else {
            $.post('/comment/post/', {
                    'csrfmiddlewaretoken':csrftoken,
                    'pk': pk,
                    'code': code,
                    'name': name,
                    'email': email,
                    'url': url,
                    'text': text
                },
                function(data) {
                    var $captcha = $('.captcha');
                    var src = $captcha.attr('src');
                    if (data.status == 0) {
                        $captcha.attr('src', src + '?');
                        alert('很遗憾, 你没有通过图灵测试, 我有权怀疑你不是人类.\n\n搞错了? 那再试试吧!');
                    } else if (data.status == 1) {
                        $captcha.attr('src', src + '?');
                        alert('你输入的内容不符合要求!');
                    } else if (data.status == 2) {
                        // window.location.reload();
                        $captcha.attr('src', src + '?');
                        var people_comment = '<div><strong style="color:#0c81b8;">' + data['comment']['name'] + '</strong><span style="float:right;">' + data['comment']['created_time'] + '</span><p class="comment-text">' + data['comment']['text'] + '</p></div><hr style="margin:10px 0 10px 0;">';
                        $('.comment-list').prepend(people_comment);
                        $('#no-comment').remove();
                        $('.comment-count').text(data['comment']['count']);
                        $('.code').val('');
                        $('.user-name').val('');
                        $('.user-email').val('');
                        $('.user-url').val('');
                        $('.comment-area').val('');
                        alert('评论成功!');
                    }
                }
            );
        }
    });
});