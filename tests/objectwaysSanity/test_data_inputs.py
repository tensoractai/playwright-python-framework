class test_data_inputs:

        # TC_A - Start Annotate Review Complete workflow
        TC_A_dataset_name = "AUT_Dataset_Bas_{i}"
        TC_A_template_name = "AUT_Template_Bas_{i}"
        TC_A_workflow_name = "AUT_Workflow_Bas_{i}"
        TC_A_project_name = "AUT_Project_Bas_{i}"
        TC_A_dataset_type_name = "Audio"
        TC_A_Dataset_files_upload = ["audio/audio 2.flac", "audio/audio 3.mp3"]
        TC_A_Template_files_upload = ["template/Updated Audio template.zip"]
        TC_A_nodes_list = ["Start", "Annotate", "Review", "Complete"]
        TC_A_annotation_text_1 = "Segment 1 by Annotator 1"
        TC_A_annotation_text_2 = "Segment 2 by Annotator 1"
        TC_A_annotation_text_Edit = "Segment Edit by Annotator 1"
        TC_A_annotation_text_3 = "Segment 3 by Annotator 1"
        TC_A_annotation_text_4 = "Segment 4 by Annotator 1"
        TC_A_reviewer_text_Edit = "Segment Edit by reviewer 1"
        TC_A_reviewer_text_Approve = "Segment Approve by reviewer 1"

        # TC_B - Start Annotate Review Annotate Review Complete
        TC_B_dataset_name = "AUT_Dataset_Comp_{i}"
        TC_B_template_name = "AUT_Template_Comp_{i}_A"
        TC_B_template_name_2 = "AUT_Template_Comp_{i}_B"
        TC_B_workflow_name = "AUT_Workflow_Comp_{i}"
        TC_B_project_name = "AUT_Project_Comp_{i}"
        TC_B_Template_files_upload_1 = ["template/Test Audio A.zip"]
        TC_B_Template_files_upload_2 = ["template/Updated Audio template.zip"]
        TC_B_nodes_list = ["Start", "Annotate", "Review", "Annotate", "Review", "Complete"]
        TC_B_annotation_1_1 = "Segment 1 by Annotator 1"
        TC_B_annotation_1_2 = "Segment 2 by Annotator 1"
        TC_B_annotation_1_3 = "Segment 3 by Annotator 1"
        TC_B_annotation_1_4 = "Segment 4 by Annotator 1"
        TC_B_annotation_1_Edit = "Segment Edit by Annotator 1"
        TC_B_annotation_2_1 = "Segment 1 by Annotator 2"
        TC_B_annotation_2_2 = "Segment 2 by Annotator 2"
        TC_B_annotation_2_3 = "Segment 3 by Annotator 2"
        TC_B_annotation_2_4 = "Segment 4 by Annotator 2"
        TC_B_annotation_2_Edit = "Segment Edit by Annotator 2"
        TC_B_reviewer_1_text_Edit = "Segment Edit by Reviewer 1"
        TC_B_reviewer_1_text_Approve = "Segment Approve by Reviewer 1"
        TC_B_reviewer_2_text_Edit = "Segment Edit by Reviewer 2"
        TC_B_reviewer_2_text_Approve = "Segment Approve by Reviewer 2"

        # TC_C - Start, Annotate (Consensus Mode), Review, Complete
        TC_C_dataset_name = "AUT_Dataset_Consen_{i}"
        TC_C_template_name = "AUT_Template_Consen_{i}"
        TC_C_workflow_name = "AUT_Workflow_Consen_{i}"
        TC_C_project_name = "AUT_Project_Consen_{i}"
        TC_C_nodes_list = ["Start", "Annotate", "Review", "Complete"]
        TC_C_annotation_1_1 = "Segment 1 by Annotator 1"
        TC_C_annotation_1_2 = "Segment 2 by Annotator 1"
        TC_C_annotation_1_3 = "Segment 3 by Annotator 1"
        TC_C_annotation_1_4 = "Segment 4 by Annotator 1"
        TC_C_annotation_1_Edit = "Segment Edit by Annotator 1"
        TC_C_annotation_2_1 = "Segment 1 by Annotator 2"
        TC_C_annotation_2_2 = "Segment 2 by Annotator 2"
        TC_C_annotation_2_3 = "Segment 3 by Annotator 2"
        TC_C_annotation_2_4 = "Segment 4 by Annotator 2"
        TC_C_annotation_2_Edit = "Segment Edit by Annotator 2"
        TC_C_reviewer_1_text_Edit = "Segment Edit by Reviewer 1"
        TC_C_reviewer_1_text_Approve = "Segment Approve by Reviewer 1"

        # TC_D - Start Annotate Review 1 Review 2 Complete 
        TC_D_dataset_name = "AUT_Dataset_2Review_{i}"
        TC_D_template_name = "AUT_Template_2Review_{i}"
        TC_D_workflow_name = "AUT_Workflow_2Review_{i}"
        TC_D_project_name = "AUT_Project_2Review_{i}"
        TC_D_nodes_list = ["Start", "Annotate", "Review","Review", "Complete"]
        TC_D_annotation_1_1 = "Segment 1 by Annotator 1"
        TC_D_annotation_1_2 = "Segment 2 by Annotator 1"
        TC_D_annotation_1_3 = "Segment 3 by Annotator 1"
        TC_D_annotation_1_4 = "Segment 4 by Annotator 1"
        TC_D_annotation_1_Edit = "Segment Edit by Annotator 1"
        TC_D_reviewer_1_text_Edit = "Segment Edit by Reviewer 1"
        TC_D_reviewer_1_text_Approve = "Segment Approve by Reviewer 1"
        TC_D_reviewer_2_text_Edit = "Segment Edit by Reviewer 2"
        TC_D_reviewer_2_text_Approve = "Segment Approve by Reviewer 2"




