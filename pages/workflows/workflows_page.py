from utils.ui_utils import UIUtils

class WorkflowsPage:
    def __init__(self, page):
        self.page = page
        self.ui_utils = UIUtils(page)

        self.frame = page.frame_locator("iframe")
        self.workflows_menu = page.get_by_role("link", name="Workflows")
        self.create_workflow_btn = page.get_by_role("button", name="Create workflow")
        self.enter_workflow_name_input = page.locator("input#workflowName")
        self.description_input = page.get_by_role('textbox', name= 'Description' )
        self.next_button = page.get_by_role('button', name= 'Next')
        self.workflow_chart = page.locator('.react-flow__pane')
        self.nodes_in_chart = page.locator("div[class*='node-start']")
        self.plus_icon = page.locator("svg[class*='lucide-plus']")
        self.save_btn = page.get_by_role("button", name="Save")
        self.close_btn = page.get_by_role('button', name= 'Close' )
        self.template_applied_name = page.locator('div[class*="medium cursor"]')
        self.workflow_names_list = page.locator('div[class*="medium text"]')
        self.fit_view = page.get_by_role('button', name= 'fit view')
        self.required_annotators = page.get_by_role('spinbutton', name= 'Required annotators' )
        self.blank_workflow = page.get_by_role('radio',  name='Blank Workflow')
        self.annotators_review = page.get_by_role('radio',  name='Annotation & Review')
        self.assisted_annotation = page.get_by_role('radio', name='Assisted Annotation')
        self.cancel_btn = page.get_by_role('button', name='Cancel')
        self.back_btn = page.get_by_role('button', name='Back')
        self.workflow_exists_error = page.locator("svg[class*='lucide-circle'] ~ span").filter(has_text="A Workflow with this name already exists")
        self.workflow_invalid_name_error = page.get_by_text("Only letters, numbers, spaces, _ and - are allowed", exact=False)
        self.search_btn = page.get_by_role('textbox', name='search')
        self.no_workflows_found = page.get_by_role('cell', name= 'No workflows found' )
        self.edit_button = page.get_by_role("button", name="Edit").or_(page.locator("button:has-text('Edit')"))
        self.edit_name = page.locator("input[class*='nodrag']")
        self.delete_confirmation = page.get_by_role('heading', name= 'Deletion Confirmation' )
        self.workflow_delete_success_popup = self.page.get_by_text('Successfully Deleted Workflow')
        self.workflow_delete_failed_popup = self.page.get_by_text('Failed Deleted Workflow')
        self.workflow_edit_error = page.get_by_text('This workflow is currently in')

    def click_workflow_name(self, workflow_name):
        return self.page.locator("div[class*='workflow-name']").filter(has_text=workflow_name)

    def click_nodes_workflow(self, node_name):
        return self.page.locator(f"div[class*='space'] div[class*='{node_name.lower()}']")

    def verify_nodes_in_workflow_chart(self, nodesName):
        nodeNames = nodesName.strip().lower()
        return self.page.locator(f"div[class*='node-{nodeNames}']").first

    def get_template_option(self, template_name):
        return self.page.locator("span").filter(has_text=template_name)

    def get_node_connector(self, node_name: str, node_index: int, position: str, handle_index: int):
        nodes = self.page.locator(f"div[class*='node-{node_name}']")
        node = nodes.nth(node_index - 1)
        handle = node.locator(f"div[data-handlepos*='{position}']").nth(handle_index - 1)
        return handle

    def return_applied_template_click(self, oldTemplateName , index):
        return self.page.locator("div[class*='medium cursor-pointer']").filter(has_text=oldTemplateName).nth(index-1)

    def delete_node_btn(self, node_name: str, index: int = 1):
        return self.page.locator(f"div[class*='node-{node_name.lower()}']").nth(index - 1).locator("svg[class*='lucide-x']").first

    def edit_node_pencil(self, node_name: str, index: int = 1):
        return self.page.locator(f"div[class*='node-{node_name.lower()}']").nth(index - 1).locator("svg[class*='lucide-pencil']").first
        

    

    