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
                        "sync_request_timeout": 10
                    }
                )
            return self._connection
        except Exception as e:
            print(f"Erro ao conectar ao RPC Service: {e}")
            return None

    def call(self, method_name, *args, **kwargs):
        """Executa um método remoto e já retorna os dados limpos (obtain)."""
        conn = self.get_connection()
        if conn:
            try:
                # Acessa o método exposto no rpc-service (root.exposed_...)
                remote_method = getattr(conn.root, f"create_room" if method_name == "create_room" else f"join_room")
                # Se preferir automatizar o prefixo 'exposed_', use:
                # remote_method = getattr(conn.root, method_name)
                
                result = remote_method(*args, **kwargs)
                return obtain(result)
            except Exception as e:
                print(f"Erro ao chamar método remoto {method_name}: {e}")
                return None
        return None

# Instância única para ser importada nos controllers
rpc_client = RPCClient()