class XenForoNewMessageDispatcher:
    def __init__(self, xen_foro_new_thread_detector, discord_service, discord_mention_factory, clock_signal, forum_thread_url_factory, config):
        self._xen_foro_new_thread_detector = xen_foro_new_thread_detector
        self._discord_service = discord_service
        self._discord_mention_factory = discord_mention_factory
        self._clock_signal = clock_signal
        self._forum_thread_url_factory = forum_thread_url_factory
        self._config = config
        self._forums_by_forum_id = self.map_forum_configs_by_forum_id(config)

        update_period = config["update_period"]
        self._clock_signal.create_callback(update_period, self._check_for_new_threads)

    def map_forum_configs_by_forum_id(self, config):
        by_forum_id = dict()
        for forum_thread in config["forums"]:
            forum_id = forum_thread["forum_id"]
            by_forum_id[forum_id] = forum_thread
        return by_forum_id

    async def _check_for_new_threads(self):
        threads_needing_messages = self._xen_foro_new_thread_detector.get_threads_needing_messages()
        for new_thread in threads_needing_messages:
            await self._handle_new_thread(new_thread)

    async def _handle_new_thread(self, new_thread):
        forum_id = new_thread["forum_id"]
        thread_id = new_thread["thread_id"]
        matching_config = self._forums_by_forum_id[forum_id]
        target_channel = matching_config["target_discord_channel"]
        message_template = matching_config["message_template"]
        message_template = self._perform_url_replacement(message_template, forum_id, thread_id)
        message_template = self._discord_mention_factory.perform_replacement(message_template)
        await self._discord_service.send_channel_message(message_template, target_channel)

    def _perform_url_replacement(self, message_template, forum_id, thread_id):
        url = self._forum_thread_url_factory.get_url(self._config["base_url"], forum_id, thread_id)
        return message_template.replace("{thread_url}", url)