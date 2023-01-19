from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    feature_store_path:str
    train_path:str
    test_path:str


@dataclass
class DataValidationArtifact:
    report_path:str
    good_dataset_train_path:str
    good_dataset_test_path:str
    bad_dataset_train_path:str
    bad_dataset_test_path:str


@dataclass
class DataTransformationArtifact:
    transformer_object_path:str
    x_train_df_transformed_path:str
    x_test_df_transformed_path:str
    y_train_df_transformed_path:str
    y_test_df_transformed_path:str


@dataclass
class ModelTraningArtifact:
    train_model_path:str

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    impruve_accuracy:float
    model_path:str
    transformer_path:str

@dataclass
class ModelPusherArtifact:
    pusher_dir:str
    saved_model_dir:str