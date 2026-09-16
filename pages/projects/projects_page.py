from utils.ui_utils import UIUtils

class ProjectsPage:
    def __init__(self, page):
        self.page = page
        self.ui_utils = UIUtils(page)

        self.project_menu         = page.get_by_role("link", name="Projects")
        self.create_project_btn    = page.get_by_role("button", name="Create Project")
        self.delete_toolbar_btn    = page.get_by_role("button", name="Delete")
        self.projects_heading      = page.get_by_role("heading", name="Projects")
        self.project_name_input = page.get_by_role('textbox', name= 'Enter Project Name' )
        self.select_dataset = page.get_by_role('button', name= 'Select Datasets' )
        self.select_workflow = page.get_by_role('button', name= 'Select Workflow' )
        self.create_project_page = page.get_by_text('PlaceholderProject Name*:')
        self.heading_create_project = page.get_by_role('heading', name= 'Create Project' )
        self.project_names_list = page.locator('div[class*="medium text"]')
        self.task_panel = page.get_by_role('tabpanel', name= 'Tasks' )
        self.teams_tab = page.get_by_role('tab', name= 'Teams' )
        self.teams_panel = page.get_by_text('TeamsAdd UsersRemove Selected')
        self.add_user_btn = page.get_by_role('button', name= 'Add Users' )
        self.remove_selected_btn = page.get_by_role('button', name='Remove Selected')
        self.assign_user_dropdown = page.get_by_role("combobox").first
        self.add_btn = page.get_by_role('button', name='Add' )
        self.assigners_list = page.locator("div[class*='truncate']")
        self.project_delete_success = page.get_by_text('Successfully Deleted Project')
        self.project_description_input = page.get_by_role('textbox', name='Description')
        self.overview_tab = page.get_by_role('tab', name='Overview')
        self.tasks_tab = page.get_by_role('tab', name='Tasks')
        self.workflow_tab = page.get_by_role('tab', name='Workflow')
        self.taxonomy_tab = page.get_by_role('tab', name='Taxonomy')
        self.project_datasets_tab = page.get_by_role('tab', name='Datasets')
        self.teams_tab = page.get_by_role('tab', name='Teams')
        self.add_taxonomy_btn = page.get_by_role('button', name='Add Taxonomy')
        self.add_datasets_btn = page.get_by_role('button', name='Add Datasets')
        self.project_datasets_add_btn = page.get_by_test_id('project-datasets-add-btn')
        self.add_sync_btn = page.get_by_role('button', name='Add/Sync')
        self.add_datasets_modal_submit_btn = page.get_by_test_id('add-datasets-modal-submit-btn')
        self.export_json_btn = page.get_by_role('button', name='Export')
        self.search_input = page.get_by_role('textbox', name='Search')
        self.search_datasets_input = page.get_by_role('textbox', name='Search Datasets')
        self.duplicate_project_warning = page.get_by_text('A project with this name already exists')
        self.duplicate_project_error = page.get_by_text('A Project with this name')
        self.invalid_name_error = page.get_by_text('Only letters, numbers, spaces')
        self.annotation_approval_select = page.get_by_role('combobox')
        self.annotation_submit_btn = page.get_by_role('button', name='Submit')
        self.cancel_exit_btn = page.get_by_role('button', name='Cancel and Exit')
        self.save_exit_btn = page.get_by_role('button', name='Save and Exit')
        self.dataset_incompatible_toast = page.get_by_text('incompatible', exact=False)
        self.file_name_list_Task_tab = page.locator("td[class*='truncate max'] span")
        self.dataset_name_list = page.locator("td[class*='medium text']")
        self.tasks_table_master_checkbox = page.get_by_role('row', name='File Name Annotator Reviewer').get_by_role('checkbox')
        self.project_tabs = page.locator("div[role='tablist'] button")
        self.pagination_dropdown = page.locator("#itemsPerPage")
        self.modal_pagination_select = page.get_by_test_id('pagination-items-per-page-select')
        self.remove_user_confirm = page.get_by_test_id('remove-users-confirmation-modal-confirm-input')
        self.remove_btn = page.get_by_test_id('remove-users-confirmation-modal-submit-btn')
        self.removed_user_toast = page.get_by_text('Successfully Removed Users')



    def select_dropdowns(self, dropdown_name):
        return self.page.get_by_text(dropdown_name, exact=True)

    def click_projects_name(self, dataset_type_name):
        return self.page.get_by_text(dataset_type_name, exact=True)

    def get_user_checkbox(self, email):
        return self.page.locator(
            f"td[title='{email}']"
        ).locator("..").locator("td.px-6").first

    def get_file_status(self, file_name):
        return self.page.locator(
            f"td[title='{file_name}'] ~ td div"
        )

    def get_dataset_modal_checkbox(self, dataset_name):
        row = self.page.get_by_role("row").filter(has_text=dataset_name)
        modal_cb = row.get_by_test_id('add-datasets-modal-col-checkbox')
        if modal_cb.count() > 0:
            return modal_cb.first
        return row.get_by_role("checkbox").first

    def return_Dataset_checkbox_addsync(self, dataset_name):
        return self.page.locator(
            f"tr[data-testid*='add-datasets-modal-row'] td:has-text('{dataset_name}')"
        ).locator("xpath=preceding-sibling::td/input")

    def get_email_click_checkbox(self, email):
        return self.page.locator(
            'td[data-testid="project-collaborators-col-email"]').filter(has_text=email).locator(
            "xpath=preceding-sibling::td//input"
        )
