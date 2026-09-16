from pages.common.login_page import LoginPage
from pages.datasets.datasets_page import datasetsPage
from pages.templates.templates_page import TemplatesPage
from pages.workflows.workflows_page import WorkflowsPage
from pages.projects.projects_page import ProjectsPage
from pages.annotator.annotator_page import AnnotatorPage
from pages.reviewer.reviewer_page import ReviewerPage
from pages.files.files_page import FilesPage
from pages.users.users_page import Userspage
from pages.superuser.superuser_page import SuperUserPage

class PageFactory:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.datasets_page = datasetsPage(page)
        self.templates_page = TemplatesPage(page)
        self.workflows_page = WorkflowsPage(page)
        self.projects_page = ProjectsPage(page)
        self.annotator_page = AnnotatorPage(page)
        self.reviewer_page = ReviewerPage(page)
        self.files_page = FilesPage(page)
        self.users_page = Userspage(page)
        self.superuser_page = SuperUserPage(page)
