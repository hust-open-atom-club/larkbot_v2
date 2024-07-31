# larkbot_v2

## Run

Install Dependencies:
```bash
pdm install
```

Edit environment variables in `.env` file:
```shell
FEED_URL=https://lore.kernel.org/lkml/?q=hust.edu.cn&x=A
LARK_TEMPLATE_ID=AAq0zlsxIx1wz
LARK_WEBHOOK_URl=https://open.feishu.cn/open-apis/bot/v2/hook/{webhook_token}
LARK_WEBHOOK_SECRET={webhook_secret}
```

Debug mode:
```bash
python3 src/larkbot_v2/app.py
```

Production mode:
```bash
python3 -m larkbot_v2
```

## TODO

- [ ] Look up user_id from Kernel SIG Group
