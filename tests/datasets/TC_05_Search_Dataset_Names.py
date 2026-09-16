import allure
import pytest
from actions.action_factory import ActionFactory
from test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("company_Username")
    password = action_factory.helpers.fetch_dotenv("company_Password")
    company_Name = action_factory.helpers.fetch_dotenv("company_Name")
    diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
    diff_email_password = action_factory.helpers.fetch_dotenv(
        "different_email_for_otp_password"
    )
    # Login
    action_factory.login_actions.perform_login(
        url=url,
        email=email,
        password=password
    )
    action_factory.login_actions.use_different_email_OTP(
        diff_email,
        diff_email_password
    )
    action_factory.login_actions.select_organization(company_Name, "Company Admin")
    return action_factory

@allure.feature("Datset")
@allure.story("Search Dataset Name")
@allure.title("Search Dataset Name")
def test_Search_Dataset_Names(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each

        # Create one Datset and Search that Dataset Name 
        Search_Dataset_Name = test_data_inputs.Search_Dataset_Name
        Search_Dataset_Type = test_data_inputs.Dataset_Type_CSV

        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.datasets_actions.create_dataset(dataset_name=Search_Dataset_Name, dataset_type_name=Search_Dataset_Type)
        action_factory.ui_utils.smart_wait()

        # Search the Dataset Name and Validate
        action_factory.files_actions.search_files_name(Search_Dataset_Name)
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        print(f"Files names list: {files_name_list}")

        if Search_Dataset_Name in files_name_list:
            status = "Pass"
            message = f"Seached Dataset Name displayed properly"
            action_factory.helpers.attach_screenshot(name="SearchedDatasetNameDisplayedProperly")
            action_factory.helpers.attach_allure(name="Searched Dataset", text="Searched Dataset Name displayed properly")
            assert True, message
        else:
            status = "Fail"
            message = f"Searched Dataset Name not displayed properly"
            action_factory.helpers.attach_screenshot(name="SearchedDatasetNameNotDisplayedProperly")
            action_factory.helpers.attach_allure(name="Searched Dataset", text="Searched Dataset Name not displayed properly")
            assert False, message    

    except Exception as e:
        status = "Fail"
        message = str(e)
        action_factory.helpers.handle_failure(message=message)
        raise

    finally:
        action_factory.helpers.write_test_results(
            status=status,
            message=message
        ) 