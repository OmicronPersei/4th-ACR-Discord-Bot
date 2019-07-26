from asyncio import Future

from asynctest import MagicMock, TestCase, PropertyMock
from user_roles_service import UserRolesService

def create_mock_role(role_props):
    role = MagicMock()
    type(role).name = role_props["name"]
    type(role).id = role_props["id"]
    return role

def create_mock_message(msg_content, channel_name, user_roles=None):
    mock_message = MagicMock()
    type(mock_message).content = PropertyMock(return_value=msg_content)
    
    mock_channel = MagicMock()
    type(mock_channel).name = PropertyMock(return_value=channel_name)
    type(mock_message).channel = PropertyMock(return_value=mock_channel)

    if user_roles is not None:
        mock_member = MagicMock()

        type(mock_member).roles = user_roles
        
        mock_edit = MagicMock(return_value=Future())
        mock_edit.return_value.set_result(None)
        type(mock_member).edit = mock_edit
        
        type(mock_message).author = PropertyMock(return_value=mock_member)

    mock_message.delete = MagicMock(return_value=Future())
    mock_message.delete.return_value.set_result(None) 

    return mock_message 

class BaseTestSetup:
    def setUp(self):
        self.mock_discord_service = MagicMock()
        self.mock_discord_service.create_listener_for_bot_command.side_effect = self.create_callback_side_effect

        self.all_mock_roles = [
            create_mock_role({ "name": "admin", "id": 1111 }),
            create_mock_role({ "name": "Fun-stuff", "id": 2222 }),
            create_mock_role({ "name": "Starcraft", "id": 3333 }),
        ]
        self.mock_discord_service.get_all_roles = MagicMock(return_value=self.all_mock_roles)

        self.mock_discord_service.send_channel_message = MagicMock(return_value=Future())
        self.mock_discord_service.send_channel_message.return_value.set_result(None)

        self.mock_config = { "command_keyword": "!roles", "blacklisted_roles": [ 1111 ] }

        self.user_roles_service = UserRolesService(self.mock_config, self.mock_discord_service)

    def create_callback_side_effect(self, *args, **kwargs):
        self.callback = args[1]

    def get_mock_role(self, name):
        return [x for x in self.all_mock_roles if x.name.lower() == name.lower()][0]


class TestRolesReturnsAllAvailableRoles(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles", "the_channel")

    async def runTest(self):
        await self.callback(self.mock_message)
        
        self.mock_discord_service.get_all_roles.assert_called()

        expected_message = "Roles available:\n`Fun-stuff`\n`Starcraft`"
        expected_channel = "the_channel"
        self.mock_discord_service.send_channel_message.assert_called_with(expected_message, expected_channel)

class TestAddRoleWhenUserDoesntHaveRole(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles add fun-stuff", "the_channel", [])
        self.mock_new_role = self.get_mock_role("Fun-stuff")

    async def runTest(self):
        await self.callback(self.mock_message)

        expected_roles_list = self.mock_message.author.roles
        expected_roles_list.append(self.mock_new_role)
        self.mock_message.author.edit.assert_called_with(roles=expected_roles_list)

class TestAddRoleWhenUserAlreadyHasRole(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles add fun-stuff", "the_channel", [ self.get_mock_role("Fun-stuff") ])

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_message.author.edit.assert_not_called()

class TestCantAddBlacklistedRole(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles add admin", "the_channel", [])

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_message.author.edit.assert_not_called()

class TestCantAddBlacklistedRoleDifferentCase(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles add AdMiN", "the_channel", [])

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_message.author.edit.assert_not_called()

class TestCanRemoveRoleWhenUserHasIt(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles remove fun-stuff", "the_channel", [ self.get_mock_role("Fun-stuff"), self.get_mock_role("admin") ])

    async def runTest(self):
        await self.callback(self.mock_message)

        expected_roles_list = [x for x in self.mock_message.author.roles if x.name.lower() != "fun-stuff"]
        self.mock_message.author.edit.assert_called_with(roles=expected_roles_list)

class TestCanRemoveRoleWhenUserHasItCaseInsensitive(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles remove fun-stuff", "the_channel", [ self.get_mock_role("Fun-stuff"), self.get_mock_role("admin") ])

    async def runTest(self):
        await self.callback(self.mock_message)

        expected_roles_list = [x for x in self.mock_message.author.roles if x.name.lower() != "fun-stuff"]
        self.mock_message.author.edit.assert_called_with(roles=expected_roles_list)

class TestCannotRemoveRoleThatIsBlacklisted(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles remove admin", "the_channel", [ self.get_mock_role("Fun-stuff"), self.get_mock_role("admin") ])

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_message.author.edit.assert_not_called()

class TestCannotRemoveRoleThatMemberDoesntHave(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_message = create_mock_message("!roles remove starcraft", "the_channel", [ self.get_mock_role("Fun-stuff"), self.get_mock_role("admin") ])

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_message.author.edit.assert_not_called()      

class TestMessageIsDeleted(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)

        self.mock_message = create_mock_message("!roles", "the_channel", [ self.get_mock_role("admin") ])
    
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