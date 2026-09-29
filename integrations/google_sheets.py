"""
Модуль интеграции с Google Sheets.
"""
import logging
from datetime import datetime
from typing import Dict, Any, List
import gspread
from oauth2client.service_account import ServiceAccountCredentials

logger = logging.getLogger(__name__)

class SheetsDB:
    """Класс для работы с Google Таблицами как с базой данных."""

    def __init__(self, spreadsheet_id: str, credentials_path: str = 'credentials.json') -> None:
        """
        Инициализация подключения к Google Sheets.
        
        :param spreadsheet_id: ID таблицы Google
        :param credentials_path: Путь к файлу ключей сервисного аккаунта
        """
        self.spreadsheet_id = spreadsheet_id
        self.credentials_path = credentials_path
        self.client = None
        self.sheet = None
        
        self._connect()

    def _connect(self) -> None:
        """Подключение к API Google Sheets."""
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, scope)
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open_by_key(self.spreadsheet_id)
            logger.info("Успешное подключение к Google Sheets.")
        except Exception as e:
            logger.warning(f"Не удалось подключиться к Google Sheets: {e}")

    def _get_or_create_worksheet(self, name: str) -> gspread.Worksheet:
        """
        Получение листа по имени, если его нет - создание.
        
        :param name: Название листа
        :return: Объект листа Worksheet
        """
        if not self.sheet:
            raise RuntimeError("Нет подключения к Google Sheets.")
            
        try:
            return self.sheet.worksheet(name)
        except gspread.exceptions.WorksheetNotFound:
            logger.info(f"Лист '{name}' не найден. Создаю новый.")
            return self.sheet.add_worksheet(title=name, rows=1000, cols=20)

    def read_config(self) -> Dict[str, Any]:
        """
        Чтение конфигурации из листа 'Config'.
        
        :return: Словарь с настройками
        """
        if not self.sheet:
            return {}
            
        try:
            ws = self._get_or_create_worksheet('Config')
            records = ws.get_all_records()
            
            config = {}
            for row in records:
                if 'Key' in row and 'Value' in row:
                    config[row['Key']] = row['Value']
            return config
        except Exception as e:
            logger.error(f"Ошибка чтения конфигурации: {e}")
            return {}

    def write_stage_output(self, stage: str, data: Dict[str, Any]) -> None:
        """
        Запись результатов этапа на соответствующий лист.
        
        :param stage: Название этапа
        :param data: Данные для записи
        """
        if not self.sheet:
            return
            
        try:
            ws = self._get_or_create_worksheet(stage)
            
            # Если лист пустой, записываем заголовки
            if not ws.get_all_values():
                headers = ['Timestamp'] + list(data.keys())
                ws.append_row(headers)
                
            row_data = [datetime.now().isoformat()] + list(data.values())
            ws.append_row(row_data)
        except Exception as e:
            logger.error(f"Ошибка записи результатов этапа: {e}")

    def log_event(self, stage: str, status: str, notes: str = '', error: str = '') -> None:
        """
        Логирование события на лист 'Log'.
        
        :param stage: Этап пайплайна
        :param status: Статус (Успех, Ошибка, В процессе)
        :param notes: Дополнительные заметки
        :param error: Текст ошибки, если есть
        """
        if not self.sheet:
            return
            
        try:
            ws = self._get_or_create_worksheet('Log')
            
            if not ws.get_all_values():
                ws.append_row(['Timestamp', 'Stage', 'Status', 'Notes', 'Error'])
                
            row = [datetime.now().isoformat(), stage, status, notes, error]
            ws.append_row(row)
        except Exception as e:
            logger.error(f"Ошибка логирования события: {e}")

    def get_all_outputs(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Чтение всех результатов со всех листов.
        
        :return: Словарь, где ключ - имя листа, значение - список записей
        """
        if not self.sheet:
            return {}
            
        try:
            result = {}
            for ws in self.sheet.worksheets():
                if ws.title not in ['Config', 'Log']:
                    result[ws.title] = ws.get_all_records()
            return result
        except Exception as e:
            logger.error(f"Ошибка получения всех результатов: {e}")
            return {}
