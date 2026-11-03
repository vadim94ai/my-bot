#!/usr/bin/env python3
"""Главный оркестратор пайплайна инфопродукта.

Запускает 5 этапов последовательно:
1. Маркетинг → анализ и стратегия
2. Копирайтинг → продающие тексты
3. Дизайн → HTML-лендинг
4. Видео → презентация и субтитры
5. DevOps → деплой и интеграции
"""
import argparse
import asyncio
import json
import logging
import sys
sys.stdout.reconfigure(encoding='utf-8')
import time
from datetime import datetime, timezone
from pathlib import Path

from agents.marketing_agent import MarketingAgent
from agents.copywriting_agent import CopywritingAgent
from agents.design_agent import DesignAgent
from agents.video_agent import VideoAgent
from agents.devops_agent import DevOpsAgent

logging.basicConfig(level=logging.INFO, format='\033[94m%(asctime)s\033[0m | \033[92m%(levelname)s\033[0m | %(message)s')
logger = logging.getLogger("Pipeline")

STAGES = {
    "marketing": MarketingAgent,
    "copywriting": CopywritingAgent,
    "design": DesignAgent,
    "video": VideoAgent,
    "devops": DevOpsAgent
}

def load_config(config_path: str) -> dict:
    """Загружает конфигурацию проекта."""
    path = Path(config_path)
    if not path.exists():
        fallback_path = Path("configs") / config_path
        if fallback_path.exists():
            path = fallback_path
        elif Path("configs/project_config.json").exists():
            path = Path("configs/project_config.json")
        else:
            logger.warning(f"Конфигурационный файл {config_path} не найден. Используется пустой конфиг.")
            return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

async def run_stage(stage_name: str, agent_class, context: dict, dry_run: bool = False) -> dict:
    """Запускает отдельный этап пайплайна."""
    start_time = time.time()
    logger.info(f"--- Запуск этапа: {stage_name.upper()} ---")
    
    if dry_run:
        logger.info(f"[DRY-RUN] Этап {stage_name} пропущен.")
        await asyncio.sleep(0.5)
        result = {"status": "dry-run", "artifacts": []}
    else:
        try:
            agent = agent_class()
            result = await agent.run(context)
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Ошибка на этапе {stage_name}: {e}")
            result = {"status": "error", "error": str(e)}

    elapsed = time.time() - start_time
    result["elapsed_time_sec"] = round(elapsed, 2)
    logger.info(f"--- Завершен этап: {stage_name.upper()} за {result['elapsed_time_sec']} сек ---")
    
    return result

async def main():
    parser = argparse.ArgumentParser(description="Главный оркестратор пайплайна инфопродукта.")
    parser.add_argument("--dry-run", action="store_true", help="Проверить конфиги без реального запуска")
    parser.add_argument("--stage", type=str, choices=list(STAGES.keys()), help="Запустить только конкретный этап")
    parser.add_argument("--config", type=str, default="configs/project_config.json", help="Путь к файлу конфигурации")
    
    args = parser.parse_args()
    
    logger.info("Инициализация пайплайна...")
    config = load_config(args.config)
    context = {"config": config, "artifacts": {}}
    
    stages_to_run = [args.stage] if args.stage else list(STAGES.keys())
    
    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "is_dry_run": args.dry_run,
        "stages": {},
        "total_time_sec": 0
    }
    
    global_start = time.time()
    
    for stage in stages_to_run:
        agent_class = STAGES[stage]
        result = await run_stage(stage, agent_class, context, dry_run=args.dry_run)
        
        summary["stages"][stage] = result
        
        if result.get("status") == "error":
            logger.warning(f"Продолжаем выполнение несмотря на ошибку в {stage}...")
            
    summary["total_time_sec"] = round(time.time() - global_start, 2)
    
    # Сохраняем результат
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)
    summary_path = out_dir / "pipeline_summary.json"
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    # Выводим финальный отчет
    print("\n" + "="*50)
    print("🏆 ФИНАЛЬНЫЙ ОТЧЕТ ПАЙПЛАЙНА")
    print("="*50)
    print(f"Режим DRY-RUN: {'Включен' if args.dry_run else 'Выключен'}")
    print(f"Общее время: {summary['total_time_sec']} сек")
    print("Статусы этапов:")
    for st, res in summary["stages"].items():
        status_icon = "✅" if res.get("status") in ["success", "dry-run"] or not res.get("error") else "❌"
        print(f"  {status_icon} {st.ljust(15)} : {res['elapsed_time_sec']} сек")
    print("="*50)
    print(f"📄 Детальный отчет сохранен в: {summary_path}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Пайплайн остановлен пользователем.")
        sys.exit(1)
