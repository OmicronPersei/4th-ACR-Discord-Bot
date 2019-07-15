from asyncio import Future

from asynctest import MagicMock, TestCase, PropertyMock
from user_roles_service import UserRolesService

class BaseTestSetup:
    def setUp(self):
        self.mock_discord_service = MagicMock()
        self.mock_discord_service.create_listener_for_bot_command.side_effect = self.create_callback_side_effect
        self.mock_discord_service.get_all_roles_names = MagicMock(return_value=[ "admin", "Fun-stuff", "Starcraft" ])
        self.mock_discord_service.send_channel_message = MagicMock(return_value=Future())
        self.mock_discord_service.send_channel_message.return_value.set_result(None)

        self.mock_config = { "command_keyword": "!roles", "blacklisted_roles": [ "admin" ] }

        self.user_roles_service = UserRolesService(self.mock_config, self.mock_discord_service)

    def create_callback_side_effect(self, *args, **kwargs):
        self.callback = args[1]

def create_mock_message(msg_content, channel_name, user_roles=None):
    mock_message = MagicMock()
    type(mock_message).content = PropertyMock(return_value=msg_content)
    
    mock_channel = MagicMock()
    type(mock_channel).name = PropertyMock(return_value=channel_name)
    type(mock_message).channel = PropertyMock(return_value=mock_channel)

    if user_roles is not None:
        mock_member = MagicMock()
        roles = []
        for role_name in user_roles:
            role = MagicMock()
            type(role).name = PropertyMock(return_value=role_name)
            roles.append(role)
        type(mock_member).roles = PropertyMock(return_value=roles)
        
        mock_edit = MagicMock(return_value=Future())
        mock_edit.return_value.set_result(None)
        type(mock_member).edit = mock_edit
        
        type(mock_message).author = PropertyMock(return_value=mock_member)

    mock_message.delete = MagicMock(return_value=Future())
    mock_message.delete.return_value.set_result(None) 

    return mock_message 

class TestRolesReturnsAllAvailableRoles(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles", "the_channel")

    async def runTest(self):
        await self.callback(self.mock_message)
        
        self.mock_discord_service.get_all_roles_names.assert_called()

        expected_message = "Roles available:\n`Fun-stuff`\n`Starcraft`"
        expected_channel = "the_channel"
        self.mock_discord_service.send_channel_message.assert_called_with(expected_message, expected_channel)

class TestAddRoleWhenUserDoesntHaveRole(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles add fun-stuff", "the_channel", [])
        self.mock_new_role = MagicMock()
        type(self.mock_new_role).name = PropertyMock(return_value="Fun-stuff")

        self.mock_discord_service.get_matching_role = MagicMock(return_value=self.mock_new_role)

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_discord_service.get_matching_role.assert_called_with("fun-stuff")

        expected_roles_list = self.mock_message.author.roles
        expected_roles_list.append(self.mock_new_role)
        self.mock_message.author.edit.assert_called_with(roles=expected_roles_list)

class TestAddRoleWhenUserDoesntHaveRoleCaseInsensitive(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles add Fun-stuff", "the_channel", [])
        self.mock_new_role = MagicMock()
        type(self.mock_new_role).name = PropertyMock(return_value="Fun-stuff")

        self.mock_discord_service.get_matching_role = MagicMock(return_value=self.mock_new_role)

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_discord_service.get_matching_role.assert_called_with("fun-stuff")

        expected_roles_list = self.mock_message.author.roles
        expected_roles_list.append(self.mock_new_role)
        self.mock_message.author.edit.assert_called_with(roles=expected_roles_list)

class TestAddRoleWhenUserAlreadyHasRole(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles add fun-stuff", "the_channel", ["Fun-stuff"])

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_discord_service.get_matching_role.assert_not_called()

        self.mock_message.author.edit.assert_not_called()

class TestCantAddBlacklistedRole(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles add admin", "the_channel", [])

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_discord_service.get_matching_role.assert_not_called()

        self.mock_message.author.edit.assert_not_called()

class TestCantAddBlacklistedRoleDifferentCase(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles add AdMiN", "the_channel", [])

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_discord_service.get_matching_role.assert_not_called()

        self.mock_message.author.edit.assert_not_called()

class TestCanRemoveRoleWhenUserHasIt(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles remove fun-stuff", "the_channel", ["Fun-stuff", "admin"])

    async def runTest(self):
        await self.callback(self.mock_message)

        expected_roles_list = [x for x in self.mock_message.author.roles if x.name.lower() != "fun-stuff"]
        self.mock_message.author.edit.assert_called_with(roles=expected_roles_list)

class TestCanRemoveRoleWhenUserHasItCaseInsensitive(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles remove fun-stuff", "the_channel", ["Fun-stuff", "admin"])

    async def runTest(self):
        await self.callback(self.mock_message)

        expected_roles_list = [x for x in self.mock_message.author.roles if x.name.lower() != "fun-stuff"]
        self.mock_message.author.edit.assert_called_with(roles=expected_roles_list)

class TestCannotRemoveRoleThatIsBlacklisted(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles remove admin", "the_channel", ["Fun-stuff", "admin"])

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_message.author.edit.assert_not_called()

class TestCannotRemoveRoleThatMemberDoesntHave(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles remove starcraft", "the_channel", ["Fun-stuff", "admin"])

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_message.author.edit.assert_not_called()      

class TestMessageIsDeleted(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)

        self.mock_message = create_mock_message("!roles", "the_channel", [ "admin" ])
    
    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_message.delete.assert_called()

class TestFunctionalityIsRestrictedToSpecificChannel(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_config["restrict_to_channel"] = "role-request"
        self.mock_message = create_mock_message("!roles", "barracks", [])

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_discord_service.send_channel_message.assert_not_called()

class TestFunctionalityIsNotRestrictedToSpecificChannelWhenNotSpecifiedInConfig(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_config["restrict_to_channel"] = None
        self.mock_message = create_mock_message("!roles", "barracks", [])

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_discord_service.send_channel_message.assert_called()