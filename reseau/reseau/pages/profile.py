import boto3
import reflex as rx

from ..common.base_state import BaseState
from ..components.profile import profile
from ..reseau import PROFILE_ROUTE, S3_BUCKET_NAME
from ..common.template import template
from ..models.user_account import UserAccount


class ProfileState(BaseState):
    profile_text: str = ""  # the user's profile text
    profile_img: str = ""  # the user's profile image

    def init(self):
        self.profile_text = self.authenticated_user.profile_text
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(S3_BUCKET_NAME)

        try:
            bucket.download_file(
                f"{self.authenticated_user.id}/profile_picture",
                f"./{rx.get_upload_dir()}/profile_picture",
            )
            self.profile_img = "profile_picture"
        except Exception:
            self.profile_img = ""

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded file(s).
        """
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

        # Update the profile_img var.
        self.profile_img = file.filename

    def save_profile(self) -> rx.event.EventSpec:
        profile_text_cleaned = self.authenticated_user.clean_profile_text(
            self.profile_text
        )
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(S3_BUCKET_NAME)

        # Retrieve the authenticated user with its id
        with rx.session() as session:
            user: UserAccount = session.exec(
                UserAccount.select().where(
                    UserAccount.id == self.authenticated_user.id
                )
            ).first()
            user.profile_text = profile_text_cleaned
            session.add(user)
            session.commit()

        # Update the authenticated user's profile text
        self.set_profile_text(profile_text_cleaned)

        # Upload the profile picture to S3
        bucket.upload_file(
            f"{rx.get_upload_dir()}/{self.profile_img}",
            f"{self.authenticated_user.id}/profile_picture"
        )

        return rx.toast.success("Profil mis à jour.")


@rx.page(title="Profil", route=PROFILE_ROUTE, on_load=ProfileState.init)
@template
def profile_page() -> rx.Component:
    return rx.cond(
        ProfileState.is_hydrated,
        rx.vstack(
            rx.heading("Ton profil", size="5", style={"margin-bottom": "1em"}),
            rx.hstack(
                rx.upload(
                    rx.image(
                        src=rx.get_upload_url(ProfileState.profile_img),
                        width="9vh",
                        height="9vh",
                        border="3px solid #ccc",
                        border_radius="50%",
                    ),
                    id="profile_img",
                    padding="0px",
                    width="10vh",
                    height="10vh",
                    border="none",
                    multiple=False,
                    accept={
                        "image/png": [".png"],
                        "image/jpeg": [".jpg", ".jpeg"],
                    },
                    on_drop=ProfileState.handle_upload(
                        rx.upload_files(upload_id="profile_img")
                    ),
                ),
                profile(
                    ProfileState.profile_text,
                    ProfileState.set_profile_text,
                    ProfileState.save_profile
                ),
                width="100%",
            ),
            rx.center(
                rx.divider(size="3"),
                width="100%",
            ),
            rx.text("Tags..."),
            width="100%",
        ),
    ),
