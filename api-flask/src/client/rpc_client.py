import rpyc
import time
from rpyc.utils.classic import obtain


class RPCClient:
    _instance = None
    _connection = None

    MAX_RETRIES = 3
    RETRY_DELAY = 1  # segundos

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RPCClient, cls).__new__(cls)
        return cls._instance

    def get_connection(self):
        try:
            if self._connection is None or self._connection.closed:
                print("Criando nova conexão RPC...")
                self._connection = rpyc.connect(
                    host="rpc-service",
                    port=18861,
                    config={
                        "allow_public_attrs": True,
                        "allow_pickle": True,
                        "sync_request_timeout": 30
                    }
                )
            return self._connection
        except Exception as e:
            print(f"Erro ao conectar ao RPC: {e}")
            return None

    def reset_connection(self):
        """Força recriação da conexão"""
        try:
            if self._connection:
                self._connection.close()
        except:
            pass
        self._connection = None

    def call(self, method_name, *args, **kwargs):

        attempts = 0

        while attempts < self.MAX_RETRIES:
            conn = self.get_connection()

            if not conn:
                attempts += 1
                print(f"Tentativa {attempts} falhou ao conectar.")
                time.sleep(self.RETRY_DELAY * attempts)
                continue

            try:
                remote_method = getattr(conn.root, method_name)

                if kwargs:
                    result = remote_method(*args, **kwargs)
                else:
                    result = remote_method(*args)

                return obtain(result)

            except Exception as e:
                print(f"Erro na tentativa {attempts+1}: {e}")

                attempts += 1
                self.reset_connection()
                time.sleep(self.RETRY_DELAY * attempts)

        print(" RPC indisponível após múltiplas tentativas.")
        return None


rpc_client = RPCClient()