import ssl

def create_context(cert, key):
    ssl_ctx = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    ssl_ctx.load_cert_chain(certfile=cert,keyfile=key) 
    return ssl_ctx