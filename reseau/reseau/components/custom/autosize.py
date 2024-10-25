import reflex as rx


class Autosize(rx.Component):
    """
    A textarea that automatically adjusts its height based on its content.
    """

    library = "react-textarea-autosize"
    tag = "TextareaAutosize"
    is_default = True


autosize_textarea = Autosize.create
