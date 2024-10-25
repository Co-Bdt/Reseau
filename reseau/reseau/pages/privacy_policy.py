# Code a stateless page without content using the Reflex framework.

import reflex as rx

from ..components.landing.navbar import navbar

from ..common.template import template
from ..reseau import PRIVACY_POLICY_ROUTE


title1 = rx.Style(
    font_weight='600',
    font_size='1.5em',
    margin_top='0.75em',
    margin_bottom='0.25em',
)

title2 = rx.Style(
    font_weight='500',
    font_size='1.25em',
)


def privacy_policy_content() -> rx.Component:
    return rx.vstack(
        "Dernière mise à jour : 14 septembre 2024",
        rx.text("Cette politique de confidentialité décrit nos politiques et procédures concernant la collecte, l'utilisation et la divulgation de vos informations lorsque vous utilisez l'application Reseau. Elle vous informe de vos droits en matière de protection de la vie privée et de la manière dont la loi vous protège. En utilisant l'application Reseau, vous acceptez la collecte et l'utilisation de vos informations conformément à cette politique de confidentialité."),

        rx.text("1. Interprétation et Définitions", style=title1),
        rx.text("Interprétation", style=title2),
        rx.text("Les mots dont la première lettre est en majuscule ont des significations définies dans les conditions suivantes. Les définitions suivantes auront la même signification qu'elles apparaissent au singulier ou au pluriel."),
        rx.text("Définitions", style=title2),
        rx.text("Aux fins de cette politique de confidentialité :",
        "- Compte désigne un compte unique créé pour vous permettre d'accéder à notre application ou à des parties de celle-ci.",
        "- Affilié désigne une entité qui contrôle, est contrôlée par ou est sous contrôle commun avec une partie.",
        "- Cookies sont de petits fichiers placés sur votre ordinateur, appareil mobile ou tout autre appareil par un site Web.",
        "- Pays désigne : France",
        "- Appareil désigne tout appareil pouvant accéder à l'application.",
        "- Données personnelles désigne toute information relative à une personne identifiée ou identifiable.",
        "- Service désigne l'application Reseau.",
        "- Fournisseur de services désigne toute personne physique ou morale qui traite les données pour le compte de Reseau.",
        "- Données d'utilisation désigne les données collectées automatiquement, générées par l'utilisation de l'application ou par l'infrastructure de l'application elle-même.",
        "- Site Web désigne le site Web associé à l'application Reseau.",
        "- Vous désigne l'individu accédant ou utilisant l'application, ou la société ou autre entité juridique au nom de laquelle cet individu accède ou utilise l'application, selon le cas."),

        rx.text("2. Collecte et Utilisation de vos Données Personnelles", style=title1),
        rx.text("Types de Données Collectées", style=title2),
        rx.text.strong("Données Personnelles"),
        rx.text("Nous ne collectons pas de données personnelles identifiables lorsque vous utilisez l'application Reseau."),
        rx.text.strong("Données d'utilisation"),
        rx.text("En tant qu'application, Reseau ne collecte pas de données d'utilisation. Nous ne suivons pas l'activité des utilisateurs, et nous n'enregistrons aucune information sur la manière dont vous utilisez l'application."),
        rx.text("Technologies de suivi et Cookies", style=title2),
        rx.text("Nous n'utilisons pas de cookies ni d'autres technologies de suivi pour collecter des informations sur votre utilisation de l'application."),

        rx.text("3. Politique de Confidentialité et Utilisation des Données de Google", style=title1),
        rx.text("Utilisation des API Google", style=title2),
        rx.text("L'application Reseau utilise certaines API Google pour améliorer ses fonctionnalités et offrir un meilleur service. Nous nous engageons à respecter les politiques de confidentialité et les exigences de Google en matière de données utilisateur."),
        rx.text("Collecte et Utilisation des Données via les API Google", style=title2),
        rx.text("Lorsque vous utilisez des fonctionnalités qui impliquent les API Google, telles que l'authentification via Google ou l'intégration de services Google, nous pouvons accéder à certaines informations personnelles fournies par Google. Ces informations peuvent inclure des données telles que votre adresse email, votre nom, et d'autres détails de profil, selon les autorisations que vous avez accordées à l'application."),
        rx.text("Conformité avec la Politique des Services API de Google", style=title2),
        rx.text("Nous adhérons à la Politique des services API de Google en matière de données utilisateur. Cela inclut les exigences de limitation d'utilisation des données et la transparence concernant la façon dont nous utilisons ces informations. Nous nous engageons à utiliser ces données uniquement dans le cadre des fonctionnalités que nous fournissons et ne les partagerons pas avec des tiers sans votre consentement explicite."),
        rx.text("Sécurité et Confidentialité", style=title2),
        rx.text("Nous mettons en place des mesures de sécurité appropriées pour protéger les données que nous obtenons via les API Google. Nous ne transférons pas ces données à d'autres applications ou services sans respecter strictement les directives de Google. Nous avons mis en œuvre des pratiques rigoureuses pour garantir la confidentialité et la sécurité des informations que nous recevons de Google."),
        rx.text("Consentement", style=title2),
        rx.text("En utilisant les fonctionnalités de notre application qui impliquent les API Google, vous consentez à la collecte et à l'utilisation de vos informations par Google et par nous, conformément à la présente politique de confidentialité."),

        rx.text("4. Utilisation de vos Données Personnelles", style=title1),
        rx.text("Comme nous ne collectons pas de données personnelles, nous ne les utilisons pas."),

        rx.text("5. Conservation de vos Données Personnelles", style=title1),
        rx.text("Nous ne conservons pas de données personnelles car nous n'en collectons pas."),

        rx.text("6. Transfert de vos Données Personnelles", style=title1),
        rx.text("Puisque nous ne collectons pas de données personnelles, il n'y a pas de transfert de ces données."),

        rx.text("7. Suppression de vos Données Personnelles", style=title1),
        rx.text("Étant donné que nous ne collectons pas de données personnelles, il n'y a pas de données à supprimer."),

        rx.text("8. Divulgation de vos Données Personnelles", style=title1),
        rx.text("Nous ne divulguons pas de données personnelles puisque nous n'en collectons pas."),

        rx.text("9. Sécurité de vos Données Personnelles", style=title1),
        rx.text("Bien que nous ne collectons pas de données personnelles, nous nous efforçons d'assurer la sécurité de l'application contre les accès non autorisés et les violations de sécurité."),

        rx.text("10. Confidentialité des Enfants", style=title1),
        rx.text("Notre application ne s'adresse pas aux personnes de moins de 13 ans. Nous ne collectons pas sciemment de données personnelles identifiables auprès de quiconque de moins de 13 ans. Si nous prenons connaissance que nous avons collecté des données personnelles d'enfants de moins de 13 ans, nous prendrons des mesures pour les supprimer."),

        rx.text("11. Liens vers d'autres Sites Web", style=title1),
        rx.text("Notre application peut contenir des liens vers d'autres sites Web. Nous n'avons aucun contrôle sur ces sites et ne sommes pas responsables de leurs politiques de confidentialité. Nous vous encourageons à lire leurs politiques de confidentialité."),

        rx.text("12. Modifications de cette Politique de Confidentialité", style=title1),
        rx.text("Nous pouvons mettre à jour cette politique de confidentialité de temps à autre. Nous vous informerons de tout changement en publiant la nouvelle politique de confidentialité sur cette page. Les changements seront effectifs dès leur publication. Nous vous conseillons de consulter cette politique périodiquement pour rester informé des modifications."),

        rx.text("13. Nous Contacter", style=title1),
        rx.text("Si vous avez des questions concernant cette politique de confidentialité, vous pouvez nous contacter :"),
        rx.text("- Par email : contact.reseaudevperso@gmail.com"),
        rx.text("- En visitant notre site Web : https://reseau-devperso.fr"),
        spacing='2',
        margin_bottom='5em',
    ),


class PrivacyPolicy(rx.State):
    ...


@rx.page(title='Privacy Policy', route=PRIVACY_POLICY_ROUTE)
@template
def privacy_policy_page() -> rx.Component:
    '''
    Render the privacy policy page.
    '''
    return rx.vstack(
        rx.container(
            navbar(),
            rx.text(
                "Politique de Confidentialité",
                style=rx.Style(
                    font_weight='700',
                    font_size='2em',
                    margin_y='1em',
                ),
            ),
            privacy_policy_content(),
            padding='0',
            size='4',
            style=rx.Style(
                width='100%',
            ),
        ),
    )
