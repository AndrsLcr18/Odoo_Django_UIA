# -*- coding: utf-8 -*-
# Cliente RPC para odoo usando JSON-RPC y requests
import requests
import base64
# Configuración de conexión a Odoo, usuario y contraseña de API
ODOO_URL = "http://localhost:8069/jsonrpc"
ODOO_DB = "odooUIA"
ODOO_USER = "api@odoo.com"
ODOO_PASSWORD = "bd70d7d46b8e097624d4bd0ecc14ae5157de27ab"

class OdooRPC:
    def __init__(self):
        self.uid = None
        self.authenticate()

    def authenticate(self):
        """Autenticación en Odoo y obtención del UID"""
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "login",
                "args": [ODOO_DB, ODOO_USER, ODOO_PASSWORD]
            },
            "id": 1
        }
        response = requests.post(ODOO_URL, json=payload).json()
        self.uid = response.get("result")
        if not self.uid:
            raise Exception("Error autenticando en Odoo")

    def call(self, model, method, args=None, kwargs=None):
        """Llamada genérica a métodos de modelos"""
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [ODOO_DB, self.uid, ODOO_PASSWORD, model, method, args, kwargs]
            },
            "id": 2
        }
        response = requests.post(ODOO_URL, json=payload).json()
        if "error" in response:
            raise Exception(response["error"])
        return response.get("result")
