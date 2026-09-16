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

@allure.feature("Dataset")
@allure.story("Dataset Pagination Check")
@allure.title("Dataset Pagination Check")
def test_Datset_Pagination(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        Pagination_Datset_Name = test_data_inputs.Pagination_Datset_Name
        Dataset_Type_PDF = test_data_inputs.Dataset_Type_PDF

        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        # Pagination Set to 5 and Check 
        action_factory.files_actions.set_files_pagination("5")
        dataset_name_count = action_factory.page_factory.datasets_page.files_name_list.count()
        if dataset_name_count > 5:
            status = "Fail"
            message = "Dataset name count is greater than 5"
            action_factory.helpers.attach_screenshot(name="DatasetNameCountGreaterThan5")
            action_factory.helpers.attach_allure(name="Dataset Name Count", text="Dataset name count is greater than 5")
            assert False, message
        else:
            status = "Pass"
            message = "Dataset name count is not greater than 5"
            action_factory.helpers.attach_screenshot(name="DatasetNameCountNotGreaterThan5")
            action_factory.helpers.attach_allure(name="Dataset Name Count", text="Dataset name count is not greater than 5")
            assert True, message
        # After setting Pagination to 5 Create New Dataset 
        action_factory.datasets_actions.create_dataset(Pagination_Datset_Name, Dataset_Type_PDF)
        dataset_name_count = action_factory.page_factory.datasets_page.files_name_list.count()
        if dataset_name_count > 5:
            status = "Fail"
            message = "Dataset name count is greater than 5 after creating new dataset"
            action_factory.helpers.attach_screenshot(name="DatasetNameCountGreaterThan5_AfterPagination")
            action_factory.helpers.attach_allure(name="Dataset Name Count", text="Dataset name count is greater than 5 after creating new dataset")
            assert False, message
        else:
            status = "Pass"
            message = "Dataset name count is not greater than 5 after creating new dataset"
            action_factory.helpers.attach_screenshot(name="DatasetNameCountNotGreaterThan5_AfterPagination")
            action_factory.helpers.attach_allure(name="Dataset Name Count", text="Dataset name count is not greater than 5")
            assert True, message
        # Next Tab Swich and Check the files Count Pagination : 
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.ui_utils.smart_wait()
        dataset_name_count = action_factory.page_factory.datasets_page.files_name_list.count()
        if dataset_name_count > 5:
            status = "Fail"
            message = "Dataset name count is greater than 5"
            action_factory.helpers.attach_screenshot(name="DatasetNameCountGreaterThan5")
            action_factory.helpers.attach_allure(name="Dataset Name Count", text="Dataset name count is greater than 5")
            assert False, message
        else:
            status = "Pass"
            message = "Dataset name count is not greater than 5"
            action_factory.helpers.attach_screenshot(name="DatasetNameCountNotGreaterThan5")
            action_factory.helpers.attach_allure(name="Dataset Name Count", text="Dataset name count is not greater than 5")
            assert True, message
        # Pagination for 10
        action_factory.files_actions.set_files_pagination("10")
        dataset_name_count = action_factory.page_factory.datasets_page.files_name_list.count()
        if dataset_name_count > 10:
            status = "Fail"
            message = "Dataset name count is greater than 10"
            action_factory.helpers.attach_screenshot(name="DatasetNameCountGreaterThan10")
            action_factory.helpers.attach_allure(name="Dataset Name Count", text="Dataset name count is greater than 10")
            assert False, message
        else:
            status = "Pass"
            message = "Dataset name count is not greater than 10"
            action_factory.helpers.attach_screenshot(name="DatasetNameCountNotGreaterThan10")
            action_factory.helpers.attach_allure(name="Dataset Name Count", text="Dataset name count is not greater than 10")
            assert True, message
        # Pagination for 20
        action_factory.files_actions.set_files_pagination("20")
        dataset_name_count = action_factory.page_factory.datasets_page.files_name_list.count()
        if dataset_name_count > 20:
            status = "Fail"
            message = "Dataset name count is greater than 20"
            action_factory.helpers.attach_screenshot(name="DatasetNameCountGreaterThan20")
            action_factory.helpers.attach_allure(name="Dataset Name Count", text="Dataset name count is greater than 20")
            assert False, message
        else:
            status = "Pass"
            message = "Dataset name count is not greater than 20"
            action_factory.helpers.attach_screenshot(name="DatasetNameCountNotGreaterThan20")
            action_factory.helpers.attach_allure(name="Dataset Name Count", text="Dataset name count is not greater than 20")
            assert True, message
        # Pagination for 50
        action_factory.files_actions.set_files_pagination("50")
        dataset_name_count = action_factory.page_factory.datasets_page.files_name_list.count()
        if dataset_name_count > 50:
            status = "Fail"
            message = "Dataset name count is greater than 50"
            action_factory.helpers.attach_screenshot(name="DatasetNameCountGreaterThan50")
            action_factory.helpers.attach_allure(name="Dataset Name Count", text="Dataset name count is greater than 50")
            assert False, message
        else:
            status = "Pass"
            message = "Dataset name count is not greater than 50"
            action_factory.helpers.attach_screenshot(name="DatasetNameCountNotGreaterThan50")
            action_factory.helpers.attach_allure(name="Dataset Name Count", text="Dataset name count is not greater than 50")
            assert True, message

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


    