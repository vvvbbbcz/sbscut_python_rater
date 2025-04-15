from logger import logger

def status_code_log(status_code: int, dth: str) -> None:
    if status_code == 302:
        logger.warning("Exceed 15 second limit")
    elif status_code != 200:
        logger.error("Failed to " + dth + ", status code: " + str(status_code))
    else:
        logger.info(dth[0].upper() + dth[1:] + " successfully")
