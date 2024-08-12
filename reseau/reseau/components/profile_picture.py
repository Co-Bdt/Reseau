import reflex as rx


class ProfilePicture(rx.ComponentState):

    @classmethod
    def get_component(
        cls,
        style: rx.Style,
        profile_picture: str = "",
    ) -> rx.Component:
        """A profile picture."""

        return rx.cond(
            profile_picture,
            rx.image(
                src=rx.get_upload_url(profile_picture),
                alt="Profile Picture",
                border_radius="50%",
                style=style,
            ),
            rx.image(
                src=rx.get_upload_url(
                            "blank_profile_picture"
                        ),
                alt="Profile Picture",
                border_radius="50%",
                style=style,
            ),
        )


profile_picture = ProfilePicture.create
