from huggingface_hub import HfApi

api = HfApi()

# tạo repo trước
api.create_repo(
    repo_id="LTKThoa/nextfund-campaign-moderation",
    repo_type="model",
    exist_ok=True
)

# upload
api.upload_folder(
    folder_path="./model",
    repo_id="LTKThoa/nextfund-campaign-moderation",
    repo_type="model"
)

print("Upload success!")