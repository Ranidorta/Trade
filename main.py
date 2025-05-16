import time
import json
from utils.logger import logger
from signal_generator import generate_signal
from validator import validate_signal
from risk_manager import manage_risk
from database import insert_signal
from data_fetcher import get_symbols

with open('config.json') as f:
    config = json.load(f)

logger.info("Iniciando trade_signal_agent")

try:
    while True:
        symbols = get_symbols()
        for symbol in symbols:
            logger.info(f"Processando símbolo: {symbol}")
            raw_signal = generate_signal(symbol)
            signal = validate_signal(raw_signal)
            if signal:
                final = manage_risk(signal)
                if final:
                    insert_signal(final)
                    logger.info(f"Sinal armazenado: {final}")
            else:
                logger.info("Nenhum novo sinal válido no momento.")
        time.sleep(60)
except KeyboardInterrupt:
    logger.info("Execução interrompida pelo usuário.")
except Exception as e:
    logger.exception(f"Erro inesperado: {e}")