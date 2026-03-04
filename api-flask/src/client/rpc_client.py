import rpyc
from rpyc.utils.classic import obtain

class RPCClient:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RPCClient, cls).__new__(cls)
        return cls._instance

    def get_connection(self):
        """Retorna uma conexão ativa ou cria uma nova se estiver caída."""
        try:
            if self._connection is None or self._connection.closed:
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
            print(f"Erro ao conectar ao RPC Service: {e}")
            return None

    def call(self, method_name, *args, **kwargs):
        conn = self.get_connection()

        if not conn:
            return None

        try:
            remote_method = getattr(conn.root, method_name)

            if kwargs:
                result = remote_method(*args, **kwargs)
            else:
                result = remote_method(*args)

            return obtain(result)

        except AttributeError:
            print(f"❌ Método {method_name} não existe no RPC")
            return None

        except Exception as e:
            print(f"❌ Erro ao chamar método {method_name}: {e}")
            return None
    
rpc_client = RPCClient()
