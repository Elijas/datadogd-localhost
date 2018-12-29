import datadog
import sentry_sdk

import auth_config
import config


# === sentry ===

def start_sentry():
    sentry_sdk.init(auth_config.SENTRY_INIT_URL, server_name=config.APP_HOST,
                    release='{}@{}'.format(config.APP_FULLNAME, config.APP_RELEASE_VERSION))


# === datadog ===

class Metrics:
    RESPONDED_CHATS = 'sp.lc.responded.chats'


_datadog_stats_val = None


def _get_datadog_stats():
    global _datadog_stats_val
    if _datadog_stats_val is None:
        datadog.initialize(api_key=auth_config.DATADOG_API_KEY, app_key=auth_config.DATADOG_APP_KEY)
        _datadog_stats_val = datadog.ThreadStats()
        _datadog_stats_val.start()
    return _datadog_stats_val


def increment_metric(name, value):
    _get_datadog_stats().increment(metric_name=name, value=value,
                                   tags=['app:{}'.format(config.APP_FULLNAME)])


def start_all():
    start_sentry()
    _get_datadog_stats()
