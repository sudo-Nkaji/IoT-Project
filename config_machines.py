"""
config_machines.py
----------------------------------------
各設備（ラズパイやPLC）の接続設定を一元管理するファイル。
URI, エンドポイント, IPアドレスなどを定義します。

このファイルはプロジェクトルートに配置し、
サーバー・クライアント・DBから共通で参照します。
"""

MACHINES = {
    "JC-1": {
        "type": "raspi",  # 設備の種類 (raspi / plc など)
        "ip": "172.16.126.52",
        "endpoint": "opc.tcp://172.16.126.52:4840/freeopcua/server/",
        "uri": "http://factory.local/opcua/jc1/",
        "desc": "E2ジョイントライン",
    },
}

def get_machine_info(name: str):
    """設備名から設定情報を取得"""
    if name not in MACHINES:
        raise KeyError(f"Unknown machine name: {name}")
    return MACHINES[name]

if __name__ == "__main__":
    # テスト実行例
    for name, info in MACHINES.items():
        print(f"[{name}] → {info['endpoint']} | {info['uri']}")
