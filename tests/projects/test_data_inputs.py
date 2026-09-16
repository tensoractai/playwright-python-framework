class test_data_inputs:

    valid_dataset_Name = "AUT_Dataset_valid"
    valid_template_Name = "AUT_Template_valid"
    valid_workflow_Name = "AUT_Workflow_valid"
    valid_project_Name = "AUT_Project_valid"
    dataset_type_name = "Audio"
    dataset_files_upload = ["audio/audio 2.flac", "audio/audio 3.mp3"]
    template_files_upload = ["template/Updated Audio template.zip"]
    nodes_list = ["Start", "Annotate", "Review", "Complete"]

    special_char_project_name = "AUT_123_#%^&"
    db_query_project_names = "DROP"
    expected_project_tabs = ["Overview", "Tasks", "Workflow", "Taxonomies", "Datasets", "Teams"]
    delete_project_names = ["AUT_Delete_Proj_1", "AUT_Delete_Proj_2", "AUT_Delete_Proj_3", "AUT_Delete_Proj_4"]
    search_project_name = "AUT_Search_Project_Test"
    pagination_project_name = "AUT_Project_Pagination_Test"
    image_dataset_name = "AUT_Dataset_Image_AddSync"
    video_dataset_name = "AUT_Dataset_Video_AddSync"
    image_files_upload = ["image/web_optimized_1200x800_97kb.jpg"]
    video_files_upload = ["video/sample_960x540.mkv"]
    add_sync_project_name = "AUT_Project_AddSync"
    teams_project_name = "AUT_Project_Teams_Test"