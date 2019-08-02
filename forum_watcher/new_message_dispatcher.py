from clock_source import ClockSource

class NewMessageDispatcher:
    def __init__(self, new_thread_detector, discord_service, discord_mention_factory, forum_thread_data_storage, forum_thread_url_factory, config):
        self._new_thread_detector = new_thread_detector
        self._discord_service = discord_service
        self._discord_mention_factory = discord_mention_factory
        self._forum_thread_url_factory = forum_thread_url_factory
        self._forum_thread_data_storage = forum_thread_data_storage
        self._config = config
        self._forums_by_forum_id = self._map_forum_configs_by_forum_id(config)

        self._setup_clock_signal_callback()

    def _setup_clock_signal_callback(self):
        update_period = self._config["update_period"]
        self._clock_signal = self._get_clock_source(update_period)
        self._clock_signal.callbacks.append(self._check_for_new_threads)

    def _get_clock_source(self, update_period):
        return ClockSource(update_period)

    def start(self):
        self._clock_signal.start()
        self._forum_thread_data_storage.check_forums_have_allocated_storage()

    def stop(self):
        self._clock_signal.stop()

    async def _check_for_new_threads(self):
        threads_needing_messages = self._new_thread_detector.get_threads_needing_messages()
        for new_thread in threads_needing_messages:
            await self._handle_new_thread(new_thread)

    async def _handle_new_thread(self, new_thread):
        forum_name = self._config["forum_name"]
        forum_id = new_thread["forum_id"]
        thread_id = new_thread["thread_id"]
        thread_title = new_thread["title"]
        matching_config = self._forums_by_forum_id[forum_id]
        target_channel = matching_config["target_discord_channel"]
        message_template = matching_config["message_template"]
        message_reactions = matching_config["discord_message_reactions"]
        message_template = self._perform_url_replacement(message_template, thread_title)
        message_template = self._discord_mention_factory.perform_replacement(message_template)
        sent_message = await self._discord_service.send_channel_message(message_template, target_channel)
        await self._discord_service.set_reactions_for_message(sent_message, message_reactions)
        self._store_new_forum_thread_record(forum_name, forum_id, thread_id)

    def _perform_url_replacement(self, message_template, thread_title):
        url = self._forum_thread_url_factory.get_url(self._config["base_url"], thread_title)
        return message_template.replace("{thread_url}", url)

    def _store_new_forum_thread_record(self, forum_name, forum_id, thread_id):
        record_obj = {
            "forum_name": forum_name,
            "forum_id": forum_id,
            "thread_id": thread_id
        }
        self._forum_thread_data_storage.store_new_forum_thread_record(record_obj)

    def _map_forum_configs_by_forum_id(self, config):
        by_forum_id = dict()
        for forum_thread in config["forums"]:
            forum_id = forum_thread["forum_id"]
            by_forum_id[forum_id] = forum_thread
        return by_forum_id