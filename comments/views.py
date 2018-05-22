from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from blog.models import Post

from .forms import CommentForm
from .models import Comment

from common.captcha import build_captcha


def captcha(request):
    """验证码生成."""

    code, raw = get_captcha()
    request.session["code"] = code
    return HttpResponse(raw)


def post_comment(request):
    """检查提交的评论."""

    # request和session都不包含code时, 要赋个不同的初值, 否则就匹配成一样了
    input_code = request.POST.get('code', 'request_no_code')
    # 如果字符串长度不为4, 绕过前端, 有问题; 也防止code过长, 溢出问题?.
    if len(input_code) == 4:
        input_code = input_code.lower()
        session_code = request.session.get('code', 'session_no_code').lower()
        # 更新code, 防止如果不请求captcha, 就一直不刷新code
        request.session['code'] = 'fuckoff'
        if input_code == session_code:
            pk = request.POST.get('pk')
            post = get_object_or_404(Post, pk=pk)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                ret_comment = {
                    'name': form.data['name'], 
                    'text': form.data['text'], 
                    # 这里要注意的是: strftime代表分钟的是'%M', 而模板语法中是'i'
                    'created_time': timezone.localtime(comment.created_time).strftime('%Y-%m-%d %H:%M'),
                    # 该文章下评论数
                    'count': post.comment_set.count(), 
                }
                return JsonResponse({'status': 2, 'comment':ret_comment})
            return JsonResponse({'status': 1})
    return JsonResponse({'status': 0})
