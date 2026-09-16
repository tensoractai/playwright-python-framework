class test_data_inputs:
    # Valid User Creation Inputs
    valid_user_name = "AutomationTesting1"
    valid_user_email = "automationtesting1@test.com"
    valid_user_password = "AUT_Testing@123"
    valid_user_roles = [
        "Company Admin",
        "Project Supervisor",
        "Project Viewer",
        "Annotator",
        "Reviewer",
        "Dataset Supervisor",
        "Dataset Viewer",
        "API User"
    ]
    # Invalid User Form Inputs
    invalid_user_name = "Invalid_user"
    invalid_email = "hello123"
    invalid_short_password = "hello"
    invalid_confirm_password = "automation"
    # Query Keyword Inputs
    sql_drop_name = "DROP"
    sql_drop_email = "drop@drop.com"
    sql_drop_password = "Drop@123"
    # Super User & Company Creation Inputs
    superuser_company_name = "AUT_Testing_1"
    superuser_legal_name = "AUT_Testing"
    superuser_email_domain = "automation.com"
    new_company_admin_name = "Testing"
    new_company_admin_email = "aaa@automation.com"
    new_company_admin_password = "Testing@123"
    updated_new_password = "AutomationTest@123"
    annotator_name = "AUT Annotator"
    annotator_email = "annotator@automation.com"
    reviewer_name = "AUT Reviewer"
    reviewer_email = "reviewer@automation.com"
    # Company & User Deletion Inputs
    delete_company_name = "AUT_testing"
    delete_company_domain = "auttesting.com"
    delete_user_name = "AUT Delete User"
    delete_user_email = "delete_user@auttesting.com"
    # Search User Validation Inputs
    search_user_name = "Search User Test"
    search_user_email = "search_user_test@test.com"
    search_user_password = "SearchUser@123"
    search_user_roles = ["Company Admin"]
    non_existing_search_user = "non_existing_user_9999"
    # Pagination User Validation Inputs
    pagination_user_name = "Pagination User Test"
    pagination_user_email = "pagination_user@test.com"
    pagination_user_password = "PaginationUser@123"
    pagination_user_roles = ["Company Admin"]
    # Deactivate User Validation Inputs
    deactivate_user_name = "Deactivate User Test"
    deactivate_user_email = "deactivate_user@test.com"
    deactivate_user_password = "DeactivateUser@123"
    deactivate_user_roles = ["Company Admin"]
    # Edit User Roles Inputs
    edit_roles_user_name = "Edit Roles"
    edit_roles_user_email = "edit_roles_user@test.com"
    edit_roles_user_password = "EditRolesUser@123"
    edit_roles_initial_roles = ["Company Admin"]
    edit_roles_new_role = "Project Supervisor"
    # Bulk Deactivate User Inputs
    bulk_deactivate_user1_name = "Bulk User 1"
    bulk_deactivate_user1_email = "bulk_user1@test.com"
    bulk_deactivate_user1_password = "BulkUser1@123"
    bulk_deactivate_user1_roles = ["Company Admin"]
    bulk_deactivate_user2_name = "Bulk User 2"
    bulk_deactivate_user2_email = "bulk_user2@test.com"
    bulk_deactivate_user2_password = "BulkUser2@123"
    bulk_deactivate_user2_roles = ["Project Supervisor"]
    # Single and Bulk Delete User Inputs
    single_bulk_delete_user1_name = "Delete User 1"
    single_bulk_delete_user1_email = "delete_user1@test.com"
    single_bulk_delete_user1_password = "DeleteUser1@123"
    single_bulk_delete_user1_roles = ["Company Admin"]
    single_bulk_delete_user2_name = "Delete User 2"
    single_bulk_delete_user2_email = "delete_user2@test.com"
    single_bulk_delete_user2_password = "DeleteUser2@123"
    single_bulk_delete_user2_roles = ["Project Supervisor"]
    single_bulk_delete_user3_name = "Delete User 3"
    single_bulk_delete_user3_email = "delete_user3@test.com"
    single_bulk_delete_user3_password = "DeleteUser3@123"
    single_bulk_delete_user3_roles = ["Annotator"]