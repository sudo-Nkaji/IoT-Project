from opcua import Client
from opcua import ua

# サーバーのエンドポイント
url = "opc.tcp://172.16.126.52:4840/freeopcua/server/"
client = Client(url)

# 値変更を受け取るためのハンドラ
class SubHandler(object):
    def datachange_notification(self, node, val, data):
        print(f"Data change: {node}, New value={val}")

# 接続と購読処理
try:
    client.connect()
    print("Connected to OPC UA server")

    # ノードID取得
    idx = 2  # 上のサーバーコードで登録した名前空間index
    status_node = client.get_node(f"ns={idx};s=Machine.Status")
    counter_node = client.get_node(f"ns={idx};s=Machine.Counter")

    # サブスクリプション設定
    handler = SubHandler()
    sub = client.create_subscription(1000, handler)
    sub.subscribe_data_change(status_node)
    sub.subscribe_data_change(counter_node)

    print("Subscribed to Status and Counter nodes. Waiting for updates...")
    while True:
        pass  # ハンドラが通知を処理してくれる

finally:
    client.disconnect()
    print("Client disconnected")
