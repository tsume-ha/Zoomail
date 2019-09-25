from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required()
def index(request):
# その他資料はすべてHTMLに書き出します。
# /templates/otherdocs/index.html にどんどん書いていきましょう
# ファイルは /private_media/others/ 以下に「英数字ファイル名」で、
# FTPクライアントや、SSHクライアントソフトでサーバーに直接アップロードしてください。
# (FFFTPとかでいいです)
    params = {
    }
    return render(request, 'otherdocs/index.html', params)