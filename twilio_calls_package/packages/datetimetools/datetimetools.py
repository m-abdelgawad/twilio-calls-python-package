from datetime import datetime, timedelta
import logging

# Import logger
log = logging.getLogger(__name__)


def get_current_timestamp(output_format='%Y-%m-%d__%H-%M-%S'):
    log.info("Start DateTimeTools module")
    current_timestamp = str(datetime.now().strftime(output_format))
    log.info("Finished DateTimeTools module")
    return current_timestamp


def get_today_date(output_format='%Y-%m-%d'):
    return datetime.now().strftime(output_format)


def get_past_date(days_count, output_format='%Y-%m-%d'):
    tday_date = datetime.now()
    past_date = timedelta(days=days_count)
    return (tday_date - past_date).strftime(output_format)


def format_date(input_date, target_format):
    return input_date.strftime(target_format)


def format_str_date(input_date, current_format, target_format):
    return datetime.strptime(input_date, current_format).strftime(target_format)


def datetime_to_epoch(datetime_object):
    epoch = datetime.utcfromtimestamp(0)
    return int((datetime_object.replace(microsecond=0) - epoch).total_seconds())


def epoch_to_datetime(epoch_date, output_format):
    return datetime.fromtimestamp(epoch_date).strftime(output_format)
