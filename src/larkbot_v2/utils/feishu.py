import base64
import hashlib
import hmac
import time

import httpx

from larkbot_v2.logger import logger


def gen_sign(timestamp: str, secret: str) -> str:
    """
    Generate sign for feishu request

    Args:
        timestamp: timestamp
        secret: secret
    Returns:
        sign: sign string
    """

    # 拼接 timestamp 和 secret
    string_to_sign = "{}\n{}".format(timestamp, secret)
    hmac_code = hmac.new(
        string_to_sign.encode("utf-8"), digestmod=hashlib.sha256
    ).digest()
    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode("utf-8")
    return sign


def send_to_lark(
    template_id: str, lark_webhook_url: str, lark_webhook_secret: str, variables: dict
) -> None:
    data = {
        "msg_type": "interactive",
        "card": {
            "type": "template",
            "data": {
                "template_id": template_id,
                "template_variable": variables,
            },
        },
    }
    logger.debug(data)

    timestamp = str(int(time.time()))
    data["timestamp"] = timestamp
    data["sign"] = gen_sign(timestamp, lark_webhook_secret)

    # TODO 增加超时和重试
    with httpx.Client(timeout=15, transport=httpx.HTTPTransport(retries=3)) as client:
        res = client.post(lark_webhook_url, json=data)

    if res.status_code != 200 or res.json()["code"] != 0:
        raise Exception(res.text)
