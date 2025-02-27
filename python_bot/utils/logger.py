import logging 
from datetime import datetime


logging.basicConfig(
    filename=f"logs/{datetime.today().strftime('%Y-%m-%d')}_log.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

#  The configuration above will save our logs to the following file format: 2025-01-30_log.log. 
# This will generate a new log file every day. Another setting to keep in mind is the log level.
#  To enable lower severity logging, you may set this to logging.DEBUG - however, bear in mind 
# that this option is quite noisy.