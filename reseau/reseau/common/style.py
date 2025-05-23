import reflex as rx


style = {

    "font_family": "Inter, sans-serif",

    rx.heading: {
        'font_weight': '700',
        'font_size': '1.25em',
        'margin_bottom': '0.5em',
    },

    rx.hstack: {
        'align_items': 'center',
    },

    '.discreet-text': {
        'font_size': '0.8em',
        'color': 'gray',
    },


    '.desktop-title': {
        'font_weight': '700',
        'font_size': '1.2em',
    },
    '.desktop-medium-text': {
        'font_weight': '500',
    },
    '.desktop-text': {
        'font_weight': '400',
    },


    '.mobile-title': {
        'font_weight': '700',
        'font_size': '1.1em',
    },
    '.mobile-medium-text': {
        'font_weight': '500',
        'font_size': '0.9em',
    },
    '.mobile-text': {
        'font_weight': '400',
        'font_size': '0.9em',
    },

    "img": {
        "filter": "invert(0)",
        "_dark": {
            "filter": "invert(1) hue-rotate(180deg)",
        }
    },

}
