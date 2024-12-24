from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, StickerSendMessage, ImageSendMessage, LocationSendMessage

from datetime import datetime

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

def index(request):
    return HttpResponse("阿母,我成功了~~!")

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:

            # 若有訊息事件
            if isinstance(event, MessageEvent):

                txtmsg = event.message.text

                if txtmsg in ["你好", "Hello", "早安", "Hi"]:
                    
                    stkpkg, stkid = 1070, 17840
                    replymsg = "你好, 請問需要為你做什麼?"

                    line_bot_api.reply_message(
                    event.reply_token,
                    [StickerSendMessage(package_id = stkpkg, sticker_id=stkid),
                     TextSendMessage( text = replymsg )])

                else:
                    
                    replymsg = "你所傳的訊息是:\n" + txtmsg

                    # 回傳收到的文字訊息
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage( text = replymsg ))
                     
                     

        return HttpResponse()
    else:
        return HttpResponseBadRequest()