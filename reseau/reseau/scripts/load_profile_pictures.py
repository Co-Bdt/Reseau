import boto3
import os
from pathlib import Path
import reflex as rx

from ..models import UserAccount
from rxconfig import S3_BUCKET_NAME


def load_profile_pictures():
    """Load all profile pictures from AWS S3 if not present."""

    # For each user, check if the profile picture is in the local directory
    # If not, download it from AWS S3

    with rx.session() as session:
        users = session.exec(UserAccount.select()).all()

    for user in users:
        local_path = f"{rx.get_upload_dir()}/{user.profile_picture}"
        if not os.path.isfile(local_path):
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(S3_BUCKET_NAME)

            try:
                # Create the user's directory if it doesn't exist
                Path(
                    rx.get_upload_dir() /
                    f"{user.id}"
                ).mkdir(parents=True, exist_ok=True)

                # Download the profile picture from AWS S3
                bucket.download_file(
                    user.profile_picture,
                    rx.get_upload_dir() / f"{user.profile_picture}",
                )
            except Exception:
                pass
