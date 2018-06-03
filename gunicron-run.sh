#!/bin/bash

# 还需配置好nginx

# 只会获取输出到stdout的内容, 不会获取stderr的内容
where=$(pipenv --venv)
# -z 代表空, -n 为非空
if [ -n "$where" ]; then
    "${where}/bin/gunicorn" myblog.wsgi -bunix:/tmp/zzzzer.sock -D
    echo "Gunicorn init OK"
fi
 
