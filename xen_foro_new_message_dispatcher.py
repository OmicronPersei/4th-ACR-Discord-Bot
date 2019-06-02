class XenForoNewMessageDispatcher:
    def __init__(self, xen_foro_new_thread_detector, discord_service, discord_mention_factory, clock_signal, config):
        self._xen_foro_new_thread_detector = xen_foro_new_thread_detector
        self._discord_service = discord_service
        self._discord_mention_factory = discord_mention_factory
        self._clock_signal = clock_signal
        self._config = config

        update_period = config["update_period"]
        self._clock_signal.create_callback(update_period, self._check_for_new_threads)

    def _check_for_new_threads(self):
        pass