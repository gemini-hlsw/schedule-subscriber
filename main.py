import asyncio
import signal
import logging
import os
import socket
from queries import Session, new_schedule_mutation
from config import ODB_ENDPOINT_URL, CORE_ENDPOINT_URL
from aiorun import run

heroku_port = os.environ.get("PORT")


def keep_port():
    if heroku_port:
        #  Needed so heroku won't kill the process
        logging.info("Socket reading!")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", int(heroku_port)))
            s.listen(1)
            conn, address = s.accept()  # accept new connection
            logging.info("Connection from: " + str(address))


async def callback():
    # run query to set a new schedule
    s = Session(url=CORE_ENDPOINT_URL)
    try:
        a = await s.query(new_schedule_mutation)
        logging.info(a)  # Respond from mutation
    except Exception as e:
        logging.info(e)  # fail to create new schedule


async def main():
    done = asyncio.Event()

    def shutdown():
        done.set()
        asyncio.get_event_loop().stop()

    asyncio.get_event_loop().add_signal_handler(signal.SIGINT, shutdown)
    s = Session(url=ODB_ENDPOINT_URL)
    # await keep_port()
    while not done.is_set():
        change = await s.subscribe_all()
        logging.debug(change)
        if change:
            await callback()


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info(f'{heroku_port=}')
    keep_port()
    try:
        run(main())
    except KeyboardInterrupt:
        pass
