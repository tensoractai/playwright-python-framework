from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils
from utils.helpers import Helpers
from actions.common.login_actions import LoginActions
from actions.datasets.datasets_actions import DatasetsActions
from actions.templates.templates_actions import TemplatesActions
from actions.workflows.workflows_actions import WorkflowsActions
from actions.projects.projects_actions import ProjectsActions
from actions.annotator.annotator_actions import AnnotatorActions
from actions.reviewer.reviewer_actions import ReviewerActions
from actions.files.files_actions import FilesActions
from actions.common.common_actions import CommonActions
from actions.users.users_actions import UsersActions
from actions.superuser.superuser_actions import SuperUserActions


class ActionFactory:
    def __init__(self, page):
        self.page = page
        self.login_actions = LoginActions(page)
        self.ui_utils = UIUtils(page)
        self.helpers = Helpers(page)
        self.datasets_actions = DatasetsActions(page)
        self.templates_actions = TemplatesActions(page)
        self.page_factory = PageFactory(page)
        self.workflows_actions = WorkflowsActions(page)
        self.projects_actions = ProjectsActions(page)
        self.annotator_actions = AnnotatorActions(page)
        self.reviewer_actions = ReviewerActions(page)
        self.files_actions = FilesActions(page)
        self.common_actions = CommonActions(page)
        self.users_actions = UsersActions(page)
        self.superuser_actions = SuperUserActions(page)