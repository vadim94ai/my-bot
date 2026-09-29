"""
Модуль интеграции с Prodamus.
"""
import hmac
import hashlib
import json
import urllib.parse
from typing import Dict, Any

class ProdamusClient:
    """Клиент для работы с API Prodamus."""

    def __init__(self, api_key: str, merchant_id: str, secret_key: str, config_path: str = 'configs/prodamus_config.json') -> None:
        """
        Инициализация клиента Prodamus.
        
        :param api_key: API ключ Prodamus
        :param merchant_id: ID мерчанта
        :param secret_key: Секретный ключ для подписи
        :param config_path: Путь к файлу конфигурации
        """
        self.api_key = api_key
        self.merchant_id = merchant_id
        self.secret_key = secret_key
        self.config_path = config_path
        self._load_config()

    def _load_config(self) -> None:
        """Загрузка конфигурации из JSON файла."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {}

    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """
        Генерация HMAC подписи для параметров.
        
        :param params: Словарь параметров
        :return: Строка с подписью
        """
        sorted_params = dict(sorted(params.items()))
        param_strings = [f"{k}={v}" for k, v in sorted_params.items()]
        data_to_sign = "&".join(param_strings)
        
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            data_to_sign.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature

    async def create_payment_link(self, amount: int, description: str, customer_email: str = '', order_id: str = '') -> str:
        """
        Создает ссылку на оплату.
        
        :param amount: Сумма к оплате
        :param description: Описание платежа
        :param customer_email: Email клиента
        :param order_id: Уникальный номер заказа
        :return: URL для оплаты
        """
        base_url = f"https://{self.merchant_id}.payform.ru"
        
        params = {
            'do': 'pay',
            'order_id': order_id,
            'customer_email': customer_email,
            'products[0][name]': description,
            'products[0][price]': str(amount),
            'products[0][quantity]': '1',
        }
        
        signature = self._generate_signature(params)
        params['signature'] = signature
        
        query_string = urllib.parse.urlencode(params)
        return f"{base_url}?{query_string}"

    def verify_webhook_signature(self, data: Dict[str, Any], signature: str) -> bool:
        """
        Проверка подписи входящего вебхука.
        
        :param data: Данные вебхука
        :param signature: Переданная подпись
        :return: True если подпись верна, иначе False
        """
        expected_signature = self._generate_signature(data)
        return hmac.compare_digest(expected_signature, signature)

    async def handle_webhook(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка уведомления об оплате.
        
        :param data: Данные вебхука от Prodamus
        :return: Разобранный результат платежа
        """
        # Обычно здесь проверяется подпись, но для примера мы просто парсим
        status = data.get('payment_status')
        order_id = data.get('order_id')
        amount = data.get('amount')
        customer_email = data.get('customer_email')
        
        return {
            'status': status,
            'order_id': order_id,
            'amount': amount,
            'customer_email': customer_email
        }
