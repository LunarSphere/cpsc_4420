from huggingface_hub import HfApi, upload_file, login


repo_id = "Kevius/sanpo_annotations"
api = HfApi()
api.create_repo(repo_id=repo_id, repo_type="dataset", exist_ok=True)

upload_file(
    path_or_fileobj="test.json",
    path_in_repo="test.json",
    repo_id=repo_id,
    repo_type="dataset",
    commit_message="Upload test.json"
)

upload_file(
    path_or_fileobj="sanpo.tar.gz",
    path_in_repo="sanpo.tar.gz",
    repo_id=repo_id,
    repo_type="dataset",
    commit_message="Uploaded videos as tar.gz archive"
)

print(f"Uploaded files to https://huggingface.co/datasets/{repo_id}")
