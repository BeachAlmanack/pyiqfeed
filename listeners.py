import numpy as np
from typing import Tuple


class SilentIQFeedListener:

    def feed_is_stale(self) -> None:
        pass

    def feed_is_fresh(self) -> None:
        pass

    def feed_has_error(self) -> None:
        pass

    def process_conn_stats(self, stats: dict) -> None:
        pass

    def process_timestamp(self, time_val: Tuple[np.datetime64, int]) -> None:
        pass


class SilentQuoteListener(SilentIQFeedListener):
    def process_invalid_symbol(self, bad_symbol: str) -> None:
        pass

    def process_news(self, news_item: dict) -> None:
        pass

    def process_regional_quote(self, quote: np.array) -> None:
        pass

    def process_summary(self, summary: np.array) -> None:
        pass

    def process_update(self, update: np.array) -> None:
        pass

    def process_fundamentals(self, fund: np.array) -> None:
        pass

    def process_auth_key(self, key: str) -> None:
        pass

    def process_keyok(self) -> None:
        pass

    def process_customer_info(self, cust_info: dict) -> None:
        pass

    def process_symbol_limit_reached(self, sym: str) -> None:
        pass

    def process_ip_addresses_used(self, ip: str) -> None:
        pass


class SilentAdminListener(SilentIQFeedListener):

    def process_register_client_app_completed(self) -> None:
        pass

    def process_remove_client_app_completed(self) -> None:
        pass

    def process_current_login(self, login: str) -> None:
        pass

    def process_current_password(self, password: str) -> None:
        pass

    def process_login_info_saved(self) -> None:
        pass

    def process_autoconnect_on(self) -> None:
        pass

    def process_autoconnect_off(self) -> None:
        pass

    def process_client_stats(self, client_stats: dict) -> None:
        pass


# noinspection PyMethodMayBeStatic
class VerboseIQFeedListener:

    def __init__(self, name: str):
        self._name = name

    def feed_is_stale(self) -> None:
        print("%s: Feed Disconnected" % self._name)

    def feed_is_fresh(self) -> None:
        print("%s: Feed Connected" % self._name)

    def feed_has_error(self) -> None:
        print("%s: Feed Reconnect Failed" % self._name)

    def process_conn_stats(self, stats: dict) -> None:
        print("%s: Connection Stats:" % self._name)
        print(stats)

    def process_timestamp(self, time_val: Tuple[np.datetime64, int]):
        print("%s: Timestamp:" % self._name)
        print(time_val)


# noinspection PyMethodMayBeStatic
class VerboseQuoteListener(VerboseIQFeedListener):

    def __init__(self, name: str):
        super().__init__(name)

    def process_invalid_symbol(self, bad_symbol: str) -> None:
        print("%s: Invalid Symbol: %s" % (self._name, bad_symbol))

    def process_news(self, news_item: dict) -> None:
        print("%s: News Item Received" % self._name)
        print(news_item)

    def process_regional_quote(self, quote: np.array) -> None:
        print("%s: Regional Quote:" % self._name)
        print(quote)

    def process_summary(self, summary: np.array) -> None:
        print("%s: Data Summary" % self._name)
        print(summary)

    def process_update(self, update: np.array) -> None:
        print("%s: Data Update" % self._name)
        print(update)

    def process_fundamentals(self, fund: np.array) -> None:
        print("%s: Fundamentals Received:" % self._name)
        print(fund)

    def process_auth_key(self, key: str) -> None:
        print("%s: Authorization Key Received: %s" % (self._name, key))

    def process_keyok(self) -> None:
        print("%s: Authorization Key OK" % self._name)

    def process_customer_info(self, cust_info: dict) -> None:
        print("%s: Customer Information:" % self._name)
        print(cust_info)

    def process_symbol_limit_reached(self, sym: str) -> None:
        print("%s: Symbol Limit Reached with subscription to %s" % (self._name, sym))

    def process_ip_addresses_used(self, ip: str) -> None:
        print("%s: IP Addresses Used: %s" % (self._name, ip))


# noinspection PyMethodMayBeStatic
class VerboseAdminListener(VerboseIQFeedListener):

    def __init__(self, name: str):
        super().__init__(name)

    def process_register_client_app_completed(self) -> None:
        print("%s: Register Client App Completed" % self._name)

    def process_remove_client_app_completed(self) -> None:
        print("%s: Remove Client App Completed" % self._name)

    def process_current_login(self, login: str) -> None:
        print("%s: Current Login: %s" % (self._name, login))

    def process_current_password(self, password: str) -> None:
        print("%s: Current Password: %s" % (self._name, password))

    def process_login_info_saved(self) -> None:
        print("%s: Login Info Saved" % self._name)

    def process_autoconnect_on(self) -> None:
        print("%s: Autoconnect On" % self._name)

    def process_autoconnect_off(self) -> None:
        print("%s: Autoconnect Off" % self._name)

    def process_client_stats(self, client_stats: dict) -> None:
        print("%s: Client Stats:" % self._name)
        print(client_stats)

