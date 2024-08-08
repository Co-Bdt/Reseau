/** @jsxImportSource @emotion/react */


import { ErrorBoundary } from "react-error-boundary"
import { Fragment, useCallback, useContext, useEffect, useRef, useState } from "react"
import { ColorModeContext, EventLoopContext, StateContexts } from "/utils/context"
import { Event, getBackendURL, getRefValue, getRefValues, isTrue, refs } from "/utils/state"
import { MessageSquareQuoteIcon as LucideMessageSquareQuoteIcon, UserSearchIcon as LucideUserSearchIcon, WifiOffIcon as LucideWifiOffIcon } from "lucide-react"
import { keyframes } from "@emotion/react"
import { toast, Toaster } from "sonner"
import env from "/env.json"
import { Box as RadixThemesBox, Button as RadixThemesButton, Card as RadixThemesCard, Container as RadixThemesContainer, Dialog as RadixThemesDialog, Flex as RadixThemesFlex, Grid as RadixThemesGrid, Heading as RadixThemesHeading, Link as RadixThemesLink, Separator as RadixThemesSeparator, Text as RadixThemesText, TextArea as RadixThemesTextArea, TextField as RadixThemesTextField } from "@radix-ui/themes"
import NextLink from "next/link"
import { Root as RadixFormRoot, Submit as RadixFormSubmit } from "@radix-ui/react-form"
import { DebounceInput } from "react-debounce-input"
import TextareaAutosize from "react-textarea-autosize"
import NextHead from "next/head"



export function Fragment_4ce3d32fe06533f833330f03365137ed () {
  const reflex___state____state__reseau___common___base_state____base_state = useContext(StateContexts.reflex___state____state__reseau___common___base_state____base_state)
  const { resolvedColorMode } = useContext(ColorModeContext)
  const reflex___state____state = useContext(StateContexts.reflex___state____state)
  const reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state = useContext(StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state)
  const reflex___state____state__abc____write_post_dialog_n1 = useContext(StateContexts.reflex___state____state__abc____write_post_dialog_n1)
  const ref_title = useRef(null); refs['ref_title'] = ref_title;
  const [addEvents, connectErrors] = useContext(EventLoopContext);
  const ref_content = useRef(null); refs['ref_content'] = ref_content;
  const reflex___state____state__abc____write_comment_form_n1 = useContext(StateContexts.reflex___state____state__abc____write_comment_form_n1)
  const reflex___state____state__abc____write_post_dialog_n2 = useContext(StateContexts.reflex___state____state__abc____write_post_dialog_n2)
  const reflex___state____state__abc____write_comment_form_n2 = useContext(StateContexts.reflex___state____state__abc____write_comment_form_n2)


  
    const handleSubmit_76703654d1005b9269b38ed14b0ec59d = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...{"title": getRefValue(refs['ref_title']), "content": getRefValue(refs['ref_content'])}}

        addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___home____home_state.publish_post", {form_data:form_data})])

        if (true) {
            $form.reset()
        }
    })
    
  
    const handleSubmit_63ada62a9d0c97f0ae91e82f3952d4a8 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...{}}

        addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___home____home_state.publish_comment", {form_data:form_data})])

        if (false) {
            $form.reset()
        }
    })
    
  
    const handleSubmit_bbb455c8ea3dabf9a7e7359eb493a88c = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...{"title": getRefValue(refs['ref_title']), "content": getRefValue(refs['ref_content'])}}

        addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___home____home_state.publish_post", {form_data:form_data})])

        if (true) {
            $form.reset()
        }
    })
    
  
    const handleSubmit_bbf334e0e085825f4b15f3f707f6649e = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...{}}

        addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___home____home_state.publish_comment", {form_data:form_data})])

        if (false) {
            $form.reset()
        }
    })
    

  return (
    <Fragment>
  {isTrue(reflex___state____state__reseau___common___base_state____base_state.is_authenticated) ? (
  <Fragment>
  <RadixThemesBox css={{"width": "100%", "@media screen and (min-width: 0)": {"margin": "0"}, "@media screen and (min-width: 30em)": {"margin": "0"}, "@media screen and (min-width: 48em)": {"margin": "0"}, "@media screen and (min-width: 62em)": {"margin": "2em 0"}}}>
  <RadixThemesContainer css={{"padding": "16px", "@media screen and (min-width: 0)": {"paddingTop": "1em", "paddingBottom": "1em", "paddingInlineStart": "1em", "paddingInlineEnd": "1em"}, "@media screen and (min-width: 30em)": {"paddingTop": "1em", "paddingBottom": "1em", "paddingInlineStart": "1em", "paddingInlineEnd": "1em"}, "@media screen and (min-width: 48em)": {"paddingTop": "1em", "paddingBottom": "1em", "paddingInlineStart": "1em", "paddingInlineEnd": "1em"}, "@media screen and (min-width: 62em)": {"paddingTop": "0", "paddingBottom": "0", "paddingInlineStart": "1em", "paddingInlineEnd": "1em"}, "@media screen and (min-width: 80em)": {"paddingTop": "0", "paddingBottom": "0", "paddingInlineStart": "0", "paddingInlineEnd": "0"}}} size={`4`}>
  <RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"width": "100%", "paddingTop": "1em", "@media screen and (min-width: 0)": {"paddingBottom": "1em"}, "@media screen and (min-width: 30em)": {"paddingBottom": "1em"}, "@media screen and (min-width: 48em)": {"paddingBottom": "1em"}, "@media screen and (min-width: 62em)": {"paddingBottom": "2em"}}} direction={`row`} justify={`start`} gap={`3`}>
  <RadixThemesBox css={{"justify": "start"}}>
  <RadixThemesBox css={{"width": "100%", "margin": "0", "@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesLink asChild={true} css={{"fontWeight": "bold", "letterSpacing": "1px", "color": isTrue(((resolvedColorMode) === (`light`))) ? `black` : `white`, "&:hover": {"color": "var(--accent-8)"}}} size={`7`} underline={`none`}>
  <NextLink href={`/`} passHref={true}>
  {`Reseau`}
</NextLink>
</RadixThemesLink>
</RadixThemesBox>
  <RadixThemesBox css={{"width": "100%", "margin": "0", "padding": "6px", "@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesLink asChild={true} css={{"fontWeight": "bold", "letterSpacing": "1px", "color": isTrue(((resolvedColorMode) === (`light`))) ? `black` : `white`, "&:hover": {"color": "var(--accent-8)"}}} size={`6`} underline={`none`}>
  <NextLink href={`/`} passHref={true}>
  {`Reseau`}
</NextLink>
</RadixThemesLink>
</RadixThemesBox>
</RadixThemesBox>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"width": "100%"}} direction={`row`} justify={`end`} gap={`4`}>
  <Fragment>
  {isTrue(reflex___state____state__reseau___common___base_state____base_state.is_authenticated) ? (
  <Fragment>
  <RadixThemesLink asChild={true} css={{"&:hover": {"color": "var(--accent-8)"}}} underline={`none`}>
  <NextLink href={`/membres`} passHref={true}>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"&:hover": {"background": "var(--gray-4)"}, "border-radius": "0.5em", "padding": "6px"}} direction={`row`} gap={`3`}>
  <Fragment>
  {isTrue(((resolvedColorMode) === (`light`))) ? (
  <Fragment>
  <LucideUserSearchIcon css={{"color": "black"}} size={28}/>
</Fragment>
) : (
  <Fragment>
  <LucideUserSearchIcon css={{"color": "white"}} size={28}/>
</Fragment>
)}
</Fragment>
</RadixThemesFlex>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"&:hover": {"background": "var(--gray-4)"}, "border-radius": "0.5em", "padding": "6px"}} direction={`row`} gap={`3`}>
  <Fragment>
  {isTrue(((resolvedColorMode) === (`light`))) ? (
  <Fragment>
  <LucideUserSearchIcon css={{"color": "black"}} size={24}/>
</Fragment>
) : (
  <Fragment>
  <LucideUserSearchIcon css={{"color": "white"}} size={24}/>
</Fragment>
)}
</Fragment>
</RadixThemesFlex>
</RadixThemesBox>
</NextLink>
</RadixThemesLink>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  <RadixThemesLink asChild={true} css={{"padding": "6px", "&:hover": {"color": "var(--accent-8)"}}}>
  <NextLink href={`/profil`} passHref={true}>
  <img css={{"border": "0.5px solid #ccc", "width": "4vh", "height": "4vh", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/${reflex___state____state__reseau___common___base_state____base_state.authenticated_user.id}_profile_picture.png`}/>
</NextLink>
</RadixThemesLink>
</RadixThemesFlex>
</RadixThemesFlex>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"paddingTop": "1em", "paddingBottom": "1em"}} direction={`row`} justify={`start`} gap={`3`}>
  <RadixThemesBox css={{"justify": "start"}}>
  <RadixThemesBox css={{"width": "100%", "margin": "0", "@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesLink asChild={true} css={{"fontWeight": "bold", "letterSpacing": "1px", "color": isTrue(((resolvedColorMode) === (`light`))) ? `black` : `white`, "&:hover": {"color": "var(--accent-8)"}}} size={`7`} underline={`none`}>
  <NextLink href={`/`} passHref={true}>
  {`Reseau`}
</NextLink>
</RadixThemesLink>
</RadixThemesBox>
  <RadixThemesBox css={{"width": "100%", "margin": "0", "padding": "6px", "@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesLink asChild={true} css={{"fontWeight": "bold", "letterSpacing": "1px", "color": isTrue(((resolvedColorMode) === (`light`))) ? `black` : `white`, "&:hover": {"color": "var(--accent-8)"}}} size={`6`} underline={`none`}>
  <NextLink href={`/`} passHref={true}>
  {`Reseau`}
</NextLink>
</RadixThemesLink>
</RadixThemesBox>
</RadixThemesBox>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"width": "100%"}} direction={`row`} justify={`end`} gap={`4`}>
  <Fragment>
  {isTrue(reflex___state____state__reseau___common___base_state____base_state.is_authenticated) ? (
  <Fragment>
  <RadixThemesLink asChild={true} css={{"&:hover": {"color": "var(--accent-8)"}}} underline={`none`}>
  <NextLink href={`/membres`} passHref={true}>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"&:hover": {"background": "var(--gray-4)"}, "border-radius": "0.5em", "padding": "6px"}} direction={`row`} gap={`3`}>
  <Fragment>
  {isTrue(((resolvedColorMode) === (`light`))) ? (
  <Fragment>
  <LucideUserSearchIcon css={{"color": "black"}} size={28}/>
</Fragment>
) : (
  <Fragment>
  <LucideUserSearchIcon css={{"color": "white"}} size={28}/>
</Fragment>
)}
</Fragment>
</RadixThemesFlex>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"&:hover": {"background": "var(--gray-4)"}, "border-radius": "0.5em", "padding": "6px"}} direction={`row`} gap={`3`}>
  <Fragment>
  {isTrue(((resolvedColorMode) === (`light`))) ? (
  <Fragment>
  <LucideUserSearchIcon css={{"color": "black"}} size={24}/>
</Fragment>
) : (
  <Fragment>
  <LucideUserSearchIcon css={{"color": "white"}} size={24}/>
</Fragment>
)}
</Fragment>
</RadixThemesFlex>
</RadixThemesBox>
</NextLink>
</RadixThemesLink>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  <RadixThemesLink asChild={true} css={{"padding": "6px", "&:hover": {"color": "var(--accent-8)"}}}>
  <NextLink href={`/profil`} passHref={true}>
  <img css={{"border": "0.5px solid #ccc", "width": "4vh", "height": "4vh", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/${reflex___state____state__reseau___common___base_state____base_state.authenticated_user.id}_profile_picture.png`}/>
</NextLink>
</RadixThemesLink>
</RadixThemesFlex>
</RadixThemesFlex>
</RadixThemesBox>
</RadixThemesBox>
  <Fragment>
  {isTrue(reflex___state____state.is_hydrated) ? (
  <Fragment>
  {isTrue(reflex___state____state__reseau___common___base_state____base_state.is_authenticated) ? (
  <Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"width": "100%"}} direction={`column`} gap={`3`}>
  <RadixThemesHeading css={{"marginBottom": "0.5em"}} size={`5`}>
  {`Communauté`}
</RadixThemesHeading>
  <RadixThemesDialog.Root>
  <RadixThemesDialog.Trigger>
  <RadixThemesButton color={`gray`} css={{"justifyContent": "start", "backgroundColor": "white", "@media screen and (min-width: 0)": {"fontSize": "0.9em"}, "@media screen and (min-width: 30em)": {"fontSize": "1em"}, "cursor": "pointer", "width": "100%"}} radius={`large`} size={`3`} variant={`outline`}>
  {`Écris quelque chose`}
</RadixThemesButton>
</RadixThemesDialog.Trigger>
  <RadixThemesDialog.Content css={{"@media screen and (min-width: 0)": {"padding": "1em 0.5em"}, "@media screen and (min-width: 30em)": {"padding": "1.5em"}}}>
  <RadixFormRoot className={`Root `} css={{"width": "100%"}} onSubmit={handleSubmit_76703654d1005b9269b38ed14b0ec59d}>
  <RadixThemesFlex direction={`column`} gap={`2`}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"marginBottom": "0.5em"}} direction={`row`} gap={`3`}>
  <Fragment>
  {isTrue(reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state.own_profile_picture_exists) ? (
  <Fragment>
  <img css={{"width": "4vh", "height": "4vh", "border": "0.5px solid #ccc", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/${reflex___state____state__reseau___common___base_state____base_state.authenticated_user.id}_profile_picture.png`}/>
</Fragment>
) : (
  <Fragment>
  <img css={{"width": "4vh", "height": "4vh", "border": "0.5px solid #ccc", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/blank_profile_picture`}/>
</Fragment>
)}
</Fragment>
  <RadixThemesText as={`p`} weight={`medium`}>
  {reflex___state____state__reseau___common___base_state____base_state.authenticated_user.username}
</RadixThemesText>
</RadixThemesFlex>
  <RadixThemesText as={`p`} size={`2`} weight={`medium`}>
  {`Titre`}
</RadixThemesText>
  <DebounceInput color={`gray`} css={{"border": "0.5px solid #ccc", "@media screen and (min-width: 0)": {"fontSize": "0.9em"}, "@media screen and (min-width: 30em)": {"fontSize": "1em"}, "width": "100%", "backgroundColor": isTrue(((resolvedColorMode) === (`light`))) ? `white` : `#121212`, "color": isTrue(((resolvedColorMode) === (`light`))) ? `black` : `white`}} debounceTimeout={300} element={RadixThemesTextField.Root} id={`title`} inputRef={ref_title} name={`title`} onChange={(_e0) => addEvents([Event("reflex___state____state.abc____write_post_dialog_n1.set_title", {value:_e0.target.value})], (_e0), {})} size={`3`} value={reflex___state____state__abc____write_post_dialog_n1.title} variant={`soft`}/>
  <RadixThemesText as={`p`} css={{"marginTop": "1em"}} size={`2`} weight={`medium`}>
  {`Contenu`}
</RadixThemesText>
  <TextareaAutosize className={`autosize-textarea`} css={{"@media screen and (min-width: 0)": {"fontSize": "0.9em"}, "@media screen and (min-width: 30em)": {"fontSize": "1em"}}} id={`content`} ref={ref_content}/>
</RadixThemesFlex>
  <RadixThemesFlex css={{"marginTop": "16px"}} justify={`end`} gap={`3`}>
  <RadixThemesDialog.Close>
  <RadixThemesButton color={`gray`} variant={`soft`}>
  {`Annuler`}
</RadixThemesButton>
</RadixThemesDialog.Close>
  <Fragment>
  {isTrue(reflex___state____state__abc____write_post_dialog_n1.title) ? (
  <Fragment>
  <RadixThemesDialog.Close>
  <RadixFormSubmit className={`Submit `}>
  <RadixThemesButton onClick={(_e) => addEvents([Event("reflex___state____state.abc____write_post_dialog_n1.clear_fields", {})], (_e), {})} type={`submit`}>
  {`Publier`}
</RadixThemesButton>
</RadixFormSubmit>
</RadixThemesDialog.Close>
</Fragment>
) : (
  <Fragment>
  <RadixThemesButton disabled={true}>
  {`Publier`}
</RadixThemesButton>
</Fragment>
)}
</Fragment>
</RadixThemesFlex>
</RadixFormRoot>
</RadixThemesDialog.Content>
</RadixThemesDialog.Root>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesFlex css={{"flex": 1, "justifySelf": "stretch", "alignSelf": "stretch"}} gap={`2`}/>
</RadixThemesBox>
  <RadixThemesGrid columns={`1`} css={{"width": "100%"}} gap={`3`}>
  {reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state.posts_displayed.map((post, index_da1e7eafb151fa8f) => (
  <RadixThemesDialog.Root key={index_da1e7eafb151fa8f}>
  <RadixThemesDialog.Trigger onClick={(_e) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___home____home_state.load_post_details", {post_id:post.at(0).id})], (_e), {})}>
  <RadixThemesCard css={{"@media screen and (min-width: 0)": {"padding": "1em"}, "@media screen and (min-width: 30em)": {"padding": "1.2em"}, "cursor": "pointer"}}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"width": "100%"}} direction={`column`} gap={`3`}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} direction={`row`} gap={`3`}>
  <Fragment>
  {isTrue(post.at(3)) ? (
  <Fragment>
  <img css={{"border": "0.5px solid #ccc", "width": "2.5em", "height": "2.5em", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/${post.at(2).id}_profile_picture.png`}/>
</Fragment>
) : (
  <Fragment>
  <img css={{"border": "0.5px solid #ccc", "width": "2.5em", "height": "2.5em", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/blank_profile_picture`}/>
</Fragment>
)}
</Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`0`}>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesText as={`p`} weight={`medium`}>
  {post.at(2).username}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesText as={`p`} size={`2`} weight={`medium`}>
  {post.at(2).username}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesText as={`p`} color={`gray`} size={`1`}>
  {post.at(1)}
</RadixThemesText>
</RadixThemesFlex>
</RadixThemesFlex>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesText as={`p`} css={{"marginBottom": "0.5em"}} size={`4`} weight={`bold`}>
  {post.at(0).title}
</RadixThemesText>
  <RadixThemesText as={`p`}>
  {post.at(0).content}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesText as={`p`} css={{"marginBottom": "0.3em"}} size={`2`} weight={`bold`}>
  {post.at(0).title}
</RadixThemesText>
  <RadixThemesText as={`p`} css={{"@media screen and (min-width: 0)": {"fontSize": "0.8em"}, "@media screen and (min-width: 30em)": {"fontSize": "1em"}}}>
  {post.at(0).content}
</RadixThemesText>
</RadixThemesBox>
</RadixThemesFlex>
</RadixThemesCard>
</RadixThemesDialog.Trigger>
  <RadixThemesDialog.Content css={{"@media screen and (min-width: 0)": {"padding": "0em 0em"}, "@media screen and (min-width: 30em)": {"padding": "0em"}}}>
  <RadixThemesFlex css={{"@media screen and (min-width: 0)": {"padding": "1em 0.5em"}, "@media screen and (min-width: 30em)": {"padding": "1.5em"}}} direction={`column`} gap={`4`}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} direction={`row`} gap={`3`}>
  <Fragment>
  {isTrue(post.at(3)) ? (
  <Fragment>
  <img css={{"border": "0.5px solid #ccc", "width": "2.5em", "height": "2.5em", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/${post.at(2).id}_profile_picture.png`}/>
</Fragment>
) : (
  <Fragment>
  <img css={{"border": "0.5px solid #ccc", "width": "2.5em", "height": "2.5em", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/blank_profile_picture`}/>
</Fragment>
)}
</Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`0`}>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesText as={`p`} weight={`medium`}>
  {post.at(2).username}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesText as={`p`} size={`2`} weight={`medium`}>
  {post.at(2).username}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesText as={`p`} color={`gray`} size={`1`}>
  {post.at(1)}
</RadixThemesText>
</RadixThemesFlex>
</RadixThemesFlex>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`3`}>
  <RadixThemesText as={`p`} size={`5`} weight={`bold`}>
  {post.at(0).title}
</RadixThemesText>
  <RadixThemesText as={`p`} css={{"fontSize": "1em"}}>
  {post.at(0).content}
</RadixThemesText>
</RadixThemesFlex>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`1`}>
  <RadixThemesText as={`p`} size={`3`} weight={`bold`}>
  {post.at(0).title}
</RadixThemesText>
  <RadixThemesText as={`p`} css={{"fontSize": "0.9em"}}>
  {post.at(0).content}
</RadixThemesText>
</RadixThemesFlex>
</RadixThemesBox>
</RadixThemesFlex>
  <RadixThemesSeparator css={{"marginBottom": "1em"}} size={`4`}/>
  <Fragment>
  <RadixThemesGrid columns={`1`} css={{"width": "100%"}} gap={`3`}>
  {reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state.post_comments.map((comment, index_949767992f7bfad6) => (
  <RadixThemesCard css={{"width": "100%", "backgroundColor": isTrue(((resolvedColorMode) === (`light`))) ? `#e9e9e9` : `#191918`, "@media screen and (min-width: 0)": {"padding": "1em 0.5em"}, "@media screen and (min-width: 30em)": {"padding": "1em"}}} key={index_949767992f7bfad6}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`row`} gap={`3`}>
  <Fragment>
  {isTrue(comment.at(3)) ? (
  <Fragment>
  <img css={{"border": "0.5px solid #ccc", "width": "4vh", "height": "4vh", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/${comment.at(0).author_id}_profile_picture.png`}/>
</Fragment>
) : (
  <Fragment>
  <img css={{"border": "0.5px solid #ccc", "width": "4vh", "height": "4vh", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/blank_profile_picture`}/>
</Fragment>
)}
</Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`0`}>
  <RadixThemesFlex align={`end`} className={`rx-Stack`} direction={`row`} gap={`1`}>
  <RadixThemesText as={`p`} css={{"@media screen and (min-width: 0)": {"fontSize": "0.9em"}, "@media screen and (min-width: 30em)": {"fontSize": "1em"}}} trim={`both`} weight={`medium`}>
  {comment.at(2).username}
</RadixThemesText>
  <RadixThemesText as={`p`} color={`gray`} size={`1`} trim={`both`}>
  {`•`}
</RadixThemesText>
  <RadixThemesText as={`p`} color={`gray`} size={`1`} trim={`both`}>
  {comment.at(1)}
</RadixThemesText>
</RadixThemesFlex>
  <RadixThemesText as={`p`} css={{"marginTop": "0.5em", "@media screen and (min-width: 0)": {"fontSize": "0.9em"}, "@media screen and (min-width: 30em)": {"fontSize": "1em"}}}>
  {comment.at(0).content}
</RadixThemesText>
</RadixThemesFlex>
</RadixThemesFlex>
</RadixThemesCard>
))}
</RadixThemesGrid>
</Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"@media screen and (min-width: 0)": {"padding": "1em 0.5em"}, "@media screen and (min-width: 30em)": {"padding": "1.5em"}}} direction={`column`} gap={`4`}>
  <RadixFormRoot className={`Root `} css={{"width": "100%"}} onSubmit={handleSubmit_63ada62a9d0c97f0ae91e82f3952d4a8}>
  <RadixThemesTextField.Root css={{"display": "none"}} name={`post_id`} value={post.at(0).id}/>
  <DebounceInput css={{"width": "100%", "@media screen and (min-width: 0)": {"fontSize": "0.9em"}, "@media screen and (min-width: 30em)": {"fontSize": "1em"}}} debounceTimeout={300} element={RadixThemesTextField.Root} name={`content`} onChange={(_e0) => addEvents([Event("reflex___state____state.abc____write_comment_form_n1.set_comment_value", {value:_e0.target.value})], (_e0), {})} placeholder={`Commente...`} radius={`large`} size={`3`} value={reflex___state____state__abc____write_comment_form_n1.comment_value}/>
  <RadixThemesFlex css={{"marginTop": "16px"}} justify={`end`} gap={`3`}>
  <RadixThemesDialog.Close>
  <RadixThemesButton color={`gray`} variant={`soft`}>
  {`Annuler`}
</RadixThemesButton>
</RadixThemesDialog.Close>
  <Fragment>
  {isTrue(reflex___state____state__abc____write_comment_form_n1.comment_value) ? (
  <Fragment>
  <RadixFormSubmit className={`Submit `}>
  <RadixThemesButton onClick={(_e) => addEvents([Event("reflex___state____state.abc____write_comment_form_n1.set_comment_value", {value:``})], (_e), {})} type={`submit`}>
  {`Commenter`}
</RadixThemesButton>
</RadixFormSubmit>
</Fragment>
) : (
  <Fragment>
  <RadixThemesButton disabled={true}>
  {`Commenter`}
</RadixThemesButton>
</Fragment>
)}
</Fragment>
</RadixThemesFlex>
</RadixFormRoot>
</RadixThemesFlex>
</RadixThemesDialog.Content>
</RadixThemesDialog.Root>
))}
</RadixThemesGrid>
</RadixThemesFlex>
</Fragment>
) : (
  <Fragment>
  <RadixThemesBox css={{"position": "absolute", "top": "50%", "left": "50%", "transform": "translateX(-50%) translateY(-50%)", "@media screen and (min-width: 0)": {"width": "80%"}, "@media screen and (min-width: 30em)": {"width": "80%"}, "@media screen and (min-width: 48em)": {"width": "70%"}, "@media screen and (min-width: 62em)": {"width": "60%"}, "@media screen and (min-width: 80em)": {"width": "50%"}}}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} justify={`center`} gap={`5`}>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesHeading css={{"letter-spacing": "1px"}} size={`9`} trim={`start`}>
  {`Reseau`}
</RadixThemesHeading>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesHeading css={{"letter-spacing": "1px"}} size={`8`} trim={`start`}>
  {`Reseau`}
</RadixThemesHeading>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesText as={`p`} size={`5`}>
  {`La première plateforme pour connecter avec `}
  {`des gars en développement personnel`}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesText as={`p`} size={`3`}>
  {`La première plateforme pour connecter avec `}
  {`des gars en développement personnel`}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesLink asChild={true} css={{"&:hover": {"color": "var(--accent-8)"}}} target={isTrue(false) ? `_blank` : ``}>
  <NextLink href={`/rejoindre`} passHref={true}>
  <RadixThemesButton size={`3`}>
  {`Rejoindre`}
</RadixThemesButton>
</NextLink>
</RadixThemesLink>
</RadixThemesFlex>
</RadixThemesBox>
</Fragment>
)}
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
</RadixThemesContainer>
</RadixThemesBox>
</Fragment>
) : (
  <Fragment>
  <RadixThemesBox>
  <Fragment>
  {isTrue(reflex___state____state.is_hydrated) ? (
  <Fragment>
  {isTrue(reflex___state____state__reseau___common___base_state____base_state.is_authenticated) ? (
  <Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"width": "100%"}} direction={`column`} gap={`3`}>
  <RadixThemesHeading css={{"marginBottom": "0.5em"}} size={`5`}>
  {`Communauté`}
</RadixThemesHeading>
  <RadixThemesDialog.Root>
  <RadixThemesDialog.Trigger>
  <RadixThemesButton color={`gray`} css={{"justifyContent": "start", "backgroundColor": "white", "@media screen and (min-width: 0)": {"fontSize": "0.9em"}, "@media screen and (min-width: 30em)": {"fontSize": "1em"}, "cursor": "pointer", "width": "100%"}} radius={`large`} size={`3`} variant={`outline`}>
  {`Écris quelque chose`}
</RadixThemesButton>
</RadixThemesDialog.Trigger>
  <RadixThemesDialog.Content css={{"@media screen and (min-width: 0)": {"padding": "1em 0.5em"}, "@media screen and (min-width: 30em)": {"padding": "1.5em"}}}>
  <RadixFormRoot className={`Root `} css={{"width": "100%"}} onSubmit={handleSubmit_bbb455c8ea3dabf9a7e7359eb493a88c}>
  <RadixThemesFlex direction={`column`} gap={`2`}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"marginBottom": "0.5em"}} direction={`row`} gap={`3`}>
  <Fragment>
  {isTrue(reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state.own_profile_picture_exists) ? (
  <Fragment>
  <img css={{"width": "4vh", "height": "4vh", "border": "0.5px solid #ccc", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/${reflex___state____state__reseau___common___base_state____base_state.authenticated_user.id}_profile_picture.png`}/>
</Fragment>
) : (
  <Fragment>
  <img css={{"width": "4vh", "height": "4vh", "border": "0.5px solid #ccc", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/blank_profile_picture`}/>
</Fragment>
)}
</Fragment>
  <RadixThemesText as={`p`} weight={`medium`}>
  {reflex___state____state__reseau___common___base_state____base_state.authenticated_user.username}
</RadixThemesText>
</RadixThemesFlex>
  <RadixThemesText as={`p`} size={`2`} weight={`medium`}>
  {`Titre`}
</RadixThemesText>
  <DebounceInput color={`gray`} css={{"border": "0.5px solid #ccc", "@media screen and (min-width: 0)": {"fontSize": "0.9em"}, "@media screen and (min-width: 30em)": {"fontSize": "1em"}, "width": "100%", "backgroundColor": isTrue(((resolvedColorMode) === (`light`))) ? `white` : `#121212`, "color": isTrue(((resolvedColorMode) === (`light`))) ? `black` : `white`}} debounceTimeout={300} element={RadixThemesTextField.Root} id={`title`} inputRef={ref_title} name={`title`} onChange={(_e0) => addEvents([Event("reflex___state____state.abc____write_post_dialog_n2.set_title", {value:_e0.target.value})], (_e0), {})} size={`3`} value={reflex___state____state__abc____write_post_dialog_n2.title} variant={`soft`}/>
  <RadixThemesText as={`p`} css={{"marginTop": "1em"}} size={`2`} weight={`medium`}>
  {`Contenu`}
</RadixThemesText>
  <TextareaAutosize className={`autosize-textarea`} css={{"@media screen and (min-width: 0)": {"fontSize": "0.9em"}, "@media screen and (min-width: 30em)": {"fontSize": "1em"}}} id={`content`} ref={ref_content}/>
</RadixThemesFlex>
  <RadixThemesFlex css={{"marginTop": "16px"}} justify={`end`} gap={`3`}>
  <RadixThemesDialog.Close>
  <RadixThemesButton color={`gray`} variant={`soft`}>
  {`Annuler`}
</RadixThemesButton>
</RadixThemesDialog.Close>
  <Fragment>
  {isTrue(reflex___state____state__abc____write_post_dialog_n2.title) ? (
  <Fragment>
  <RadixThemesDialog.Close>
  <RadixFormSubmit className={`Submit `}>
  <RadixThemesButton onClick={(_e) => addEvents([Event("reflex___state____state.abc____write_post_dialog_n2.clear_fields", {})], (_e), {})} type={`submit`}>
  {`Publier`}
</RadixThemesButton>
</RadixFormSubmit>
</RadixThemesDialog.Close>
</Fragment>
) : (
  <Fragment>
  <RadixThemesButton disabled={true}>
  {`Publier`}
</RadixThemesButton>
</Fragment>
)}
</Fragment>
</RadixThemesFlex>
</RadixFormRoot>
</RadixThemesDialog.Content>
</RadixThemesDialog.Root>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesFlex css={{"flex": 1, "justifySelf": "stretch", "alignSelf": "stretch"}} gap={`2`}/>
</RadixThemesBox>
  <RadixThemesGrid columns={`1`} css={{"width": "100%"}} gap={`3`}>
  {reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state.posts_displayed.map((post, index_da1e7eafb151fa8f) => (
  <RadixThemesDialog.Root key={index_da1e7eafb151fa8f}>
  <RadixThemesDialog.Trigger onClick={(_e) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___home____home_state.load_post_details", {post_id:post.at(0).id})], (_e), {})}>
  <RadixThemesCard css={{"@media screen and (min-width: 0)": {"padding": "1em"}, "@media screen and (min-width: 30em)": {"padding": "1.2em"}, "cursor": "pointer"}}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"width": "100%"}} direction={`column`} gap={`3`}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} direction={`row`} gap={`3`}>
  <Fragment>
  {isTrue(post.at(3)) ? (
  <Fragment>
  <img css={{"border": "0.5px solid #ccc", "width": "2.5em", "height": "2.5em", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/${post.at(2).id}_profile_picture.png`}/>
</Fragment>
) : (
  <Fragment>
  <img css={{"border": "0.5px solid #ccc", "width": "2.5em", "height": "2.5em", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/blank_profile_picture`}/>
</Fragment>
)}
</Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`0`}>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesText as={`p`} weight={`medium`}>
  {post.at(2).username}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesText as={`p`} size={`2`} weight={`medium`}>
  {post.at(2).username}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesText as={`p`} color={`gray`} size={`1`}>
  {post.at(1)}
</RadixThemesText>
</RadixThemesFlex>
</RadixThemesFlex>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesText as={`p`} css={{"marginBottom": "0.5em"}} size={`4`} weight={`bold`}>
  {post.at(0).title}
</RadixThemesText>
  <RadixThemesText as={`p`}>
  {post.at(0).content}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesText as={`p`} css={{"marginBottom": "0.3em"}} size={`2`} weight={`bold`}>
  {post.at(0).title}
</RadixThemesText>
  <RadixThemesText as={`p`} css={{"@media screen and (min-width: 0)": {"fontSize": "0.8em"}, "@media screen and (min-width: 30em)": {"fontSize": "1em"}}}>
  {post.at(0).content}
</RadixThemesText>
</RadixThemesBox>
</RadixThemesFlex>
</RadixThemesCard>
</RadixThemesDialog.Trigger>
  <RadixThemesDialog.Content css={{"@media screen and (min-width: 0)": {"padding": "0em 0em"}, "@media screen and (min-width: 30em)": {"padding": "0em"}}}>
  <RadixThemesFlex css={{"@media screen and (min-width: 0)": {"padding": "1em 0.5em"}, "@media screen and (min-width: 30em)": {"padding": "1.5em"}}} direction={`column`} gap={`4`}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} direction={`row`} gap={`3`}>
  <Fragment>
  {isTrue(post.at(3)) ? (
  <Fragment>
  <img css={{"border": "0.5px solid #ccc", "width": "2.5em", "height": "2.5em", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/${post.at(2).id}_profile_picture.png`}/>
</Fragment>
) : (
  <Fragment>
  <img css={{"border": "0.5px solid #ccc", "width": "2.5em", "height": "2.5em", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/blank_profile_picture`}/>
</Fragment>
)}
</Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`0`}>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesText as={`p`} weight={`medium`}>
  {post.at(2).username}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesText as={`p`} size={`2`} weight={`medium`}>
  {post.at(2).username}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesText as={`p`} color={`gray`} size={`1`}>
  {post.at(1)}
</RadixThemesText>
</RadixThemesFlex>
</RadixThemesFlex>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`3`}>
  <RadixThemesText as={`p`} size={`5`} weight={`bold`}>
  {post.at(0).title}
</RadixThemesText>
  <RadixThemesText as={`p`} css={{"fontSize": "1em"}}>
  {post.at(0).content}
</RadixThemesText>
</RadixThemesFlex>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`1`}>
  <RadixThemesText as={`p`} size={`3`} weight={`bold`}>
  {post.at(0).title}
</RadixThemesText>
  <RadixThemesText as={`p`} css={{"fontSize": "0.9em"}}>
  {post.at(0).content}
</RadixThemesText>
</RadixThemesFlex>
</RadixThemesBox>
</RadixThemesFlex>
  <RadixThemesSeparator css={{"marginBottom": "1em"}} size={`4`}/>
  <Fragment>
  <RadixThemesGrid columns={`1`} css={{"width": "100%"}} gap={`3`}>
  {reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state.post_comments.map((comment, index_949767992f7bfad6) => (
  <RadixThemesCard css={{"width": "100%", "backgroundColor": isTrue(((resolvedColorMode) === (`light`))) ? `#e9e9e9` : `#191918`, "@media screen and (min-width: 0)": {"padding": "1em 0.5em"}, "@media screen and (min-width: 30em)": {"padding": "1em"}}} key={index_949767992f7bfad6}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`row`} gap={`3`}>
  <Fragment>
  {isTrue(comment.at(3)) ? (
  <Fragment>
  <img css={{"border": "0.5px solid #ccc", "width": "4vh", "height": "4vh", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/${comment.at(0).author_id}_profile_picture.png`}/>
</Fragment>
) : (
  <Fragment>
  <img css={{"border": "0.5px solid #ccc", "width": "4vh", "height": "4vh", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/blank_profile_picture`}/>
</Fragment>
)}
</Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`0`}>
  <RadixThemesFlex align={`end`} className={`rx-Stack`} direction={`row`} gap={`1`}>
  <RadixThemesText as={`p`} css={{"@media screen and (min-width: 0)": {"fontSize": "0.9em"}, "@media screen and (min-width: 30em)": {"fontSize": "1em"}}} trim={`both`} weight={`medium`}>
  {comment.at(2).username}
</RadixThemesText>
  <RadixThemesText as={`p`} color={`gray`} size={`1`} trim={`both`}>
  {`•`}
</RadixThemesText>
  <RadixThemesText as={`p`} color={`gray`} size={`1`} trim={`both`}>
  {comment.at(1)}
</RadixThemesText>
</RadixThemesFlex>
  <RadixThemesText as={`p`} css={{"marginTop": "0.5em", "@media screen and (min-width: 0)": {"fontSize": "0.9em"}, "@media screen and (min-width: 30em)": {"fontSize": "1em"}}}>
  {comment.at(0).content}
</RadixThemesText>
</RadixThemesFlex>
</RadixThemesFlex>
</RadixThemesCard>
))}
</RadixThemesGrid>
</Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"@media screen and (min-width: 0)": {"padding": "1em 0.5em"}, "@media screen and (min-width: 30em)": {"padding": "1.5em"}}} direction={`column`} gap={`4`}>
  <RadixFormRoot className={`Root `} css={{"width": "100%"}} onSubmit={handleSubmit_bbf334e0e085825f4b15f3f707f6649e}>
  <RadixThemesTextField.Root css={{"display": "none"}} name={`post_id`} value={post.at(0).id}/>
  <DebounceInput css={{"width": "100%", "@media screen and (min-width: 0)": {"fontSize": "0.9em"}, "@media screen and (min-width: 30em)": {"fontSize": "1em"}}} debounceTimeout={300} element={RadixThemesTextField.Root} name={`content`} onChange={(_e0) => addEvents([Event("reflex___state____state.abc____write_comment_form_n2.set_comment_value", {value:_e0.target.value})], (_e0), {})} placeholder={`Commente...`} radius={`large`} size={`3`} value={reflex___state____state__abc____write_comment_form_n2.comment_value}/>
  <RadixThemesFlex css={{"marginTop": "16px"}} justify={`end`} gap={`3`}>
  <RadixThemesDialog.Close>
  <RadixThemesButton color={`gray`} variant={`soft`}>
  {`Annuler`}
</RadixThemesButton>
</RadixThemesDialog.Close>
  <Fragment>
  {isTrue(reflex___state____state__abc____write_comment_form_n2.comment_value) ? (
  <Fragment>
  <RadixFormSubmit className={`Submit `}>
  <RadixThemesButton onClick={(_e) => addEvents([Event("reflex___state____state.abc____write_comment_form_n2.set_comment_value", {value:``})], (_e), {})} type={`submit`}>
  {`Commenter`}
</RadixThemesButton>
</RadixFormSubmit>
</Fragment>
) : (
  <Fragment>
  <RadixThemesButton disabled={true}>
  {`Commenter`}
</RadixThemesButton>
</Fragment>
)}
</Fragment>
</RadixThemesFlex>
</RadixFormRoot>
</RadixThemesFlex>
</RadixThemesDialog.Content>
</RadixThemesDialog.Root>
))}
</RadixThemesGrid>
</RadixThemesFlex>
</Fragment>
) : (
  <Fragment>
  <RadixThemesBox css={{"position": "absolute", "top": "50%", "left": "50%", "transform": "translateX(-50%) translateY(-50%)", "@media screen and (min-width: 0)": {"width": "80%"}, "@media screen and (min-width: 30em)": {"width": "80%"}, "@media screen and (min-width: 48em)": {"width": "70%"}, "@media screen and (min-width: 62em)": {"width": "60%"}, "@media screen and (min-width: 80em)": {"width": "50%"}}}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} justify={`center`} gap={`5`}>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesHeading css={{"letter-spacing": "1px"}} size={`9`} trim={`start`}>
  {`Reseau`}
</RadixThemesHeading>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesHeading css={{"letter-spacing": "1px"}} size={`8`} trim={`start`}>
  {`Reseau`}
</RadixThemesHeading>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesText as={`p`} size={`5`}>
  {`La première plateforme pour connecter avec `}
  {`des gars en développement personnel`}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesText as={`p`} size={`3`}>
  {`La première plateforme pour connecter avec `}
  {`des gars en développement personnel`}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesLink asChild={true} css={{"&:hover": {"color": "var(--accent-8)"}}} target={isTrue(false) ? `_blank` : ``}>
  <NextLink href={`/rejoindre`} passHref={true}>
  <RadixThemesButton size={`3`}>
  {`Rejoindre`}
</RadixThemesButton>
</NextLink>
</RadixThemesLink>
</RadixThemesFlex>
</RadixThemesBox>
</Fragment>
)}
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
</RadixThemesBox>
</Fragment>
)}
</Fragment>
  )
}

export function Fragment_cf53a535ae2e610a113dd361eb6ac95b () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    <Fragment>
  {isTrue(connectErrors.length > 0) ? (
  <Fragment>
  <LucideWifiOffIcon css={{"color": "crimson", "zIndex": 9999, "position": "fixed", "bottom": "33px", "right": "33px", "animation": `${pulse} 1s infinite`}} size={32}/>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  )
}

                function Fallback({ error, resetErrorBoundary }) {
                    return (
                        <div>
  <p>
  {`Ooops...Unknown Reflex error has occured:`}
</p>
  <p css={{"color": "red"}}>
  {error.message}
</p>
  <p>
  {`Please contact the support.`}
</p>
</div>
                    );
                }
            

const pulse = keyframes`
    0% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
`


export function Toaster_6e90e5e87a1cac8c96c683214079bef3 () {
  const { resolvedColorMode } = useContext(ColorModeContext)


  refs['__toast'] = toast
  const [addEvents, connectErrors] = useContext(EventLoopContext);
  
const toast_props = {"description": `Check if server is reachable at ${getBackendURL(env.EVENT).href}`, "closeButton": true, "duration": 120000, "id": "websocket-error"};
const [userDismissed, setUserDismissed] = useState(false);
useEffect(() => {
    if (connectErrors.length >= 2) {
        if (!userDismissed) {
            toast.error(
                `Cannot connect to server: ${(connectErrors.length > 0) ? connectErrors[connectErrors.length - 1].message : ''}.`,
                {...toast_props, onDismiss: () => setUserDismissed(true)},
            )
        }
    } else {
        toast.dismiss("websocket-error");
        setUserDismissed(false);  // after reconnection reset dismissed state
    }
}, [connectErrors]);

  return (
    <Toaster closeButton={false} expand={true} position={`bottom-right`} richColors={true} theme={resolvedColorMode}/>
  )
}

export function Div_ac2a89ea84667d600a059f034bd91dfe () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    <div css={{"position": "fixed", "width": "100vw", "height": "0"}} title={`Connection Error: ${(connectErrors.length > 0) ? connectErrors[connectErrors.length - 1].message : ''}`}>
  <Fragment_cf53a535ae2e610a113dd361eb6ac95b/>
</div>
  )
}

export function Fragment_6cb8c6d0d8b0e63639dac29a3aec04f1 () {
  const reflex___state____state__reseau___common___base_state____base_state = useContext(StateContexts.reflex___state____state__reseau___common___base_state____base_state)
  const reflex___state____state__reseau___common___base_state____base_state__reseau___components___feedback_dialog____feedback_dialog_state = useContext(StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___components___feedback_dialog____feedback_dialog_state)
  const [addEvents, connectErrors] = useContext(EventLoopContext);


  
    const handleSubmit_d9df1725b0c537008dabe692e58f8735 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...{}}

        addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___components___feedback_dialog____feedback_dialog_state.on_submit", {form_data:form_data})])

        if (false) {
            $form.reset()
        }
    })
    

  return (
    <Fragment>
  {isTrue(reflex___state____state__reseau___common___base_state____base_state.is_authenticated) ? (
  <Fragment>
  <RadixThemesDialog.Root>
  <RadixThemesDialog.Trigger>
  <RadixThemesButton color={`gray`} css={{"border-radius": "50%", "width": "48px", "height": "48px", "position": "fixed", "@media screen and (min-width: 0)": {"bottom": "2em", "right": "2em"}, "@media screen and (min-width: 30em)": {"bottom": "2em", "right": "2em"}, "@media screen and (min-width: 48em)": {"bottom": "2em", "right": "2em"}, "@media screen and (min-width: 62em)": {"bottom": "2em", "right": "2em"}, "@media screen and (min-width: 80em)": {"bottom": "100px", "right": "100px"}}}>
  <LucideMessageSquareQuoteIcon css={{"color": "var(--current-color)"}}/>
</RadixThemesButton>
</RadixThemesDialog.Trigger>
  <RadixThemesDialog.Content>
  <RadixThemesDialog.Title>
  {`Feedback`}
</RadixThemesDialog.Title>
  <RadixThemesFlex direction={`column`} gap={`4`}>
  <RadixThemesText as={`p`}>
  {`Qu'est-ce qu'il manque ou pourraît être mieux sur la plateforme selon toi ?`}
</RadixThemesText>
  <RadixFormRoot className={`Root `} css={{"width": "100%"}} onSubmit={handleSubmit_d9df1725b0c537008dabe692e58f8735}>
  <DebounceInput css={{"multiline": true, "width": "100%"}} debounceTimeout={1000} element={RadixThemesTextArea} name={`feedback`} onChange={(_e0) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___components___feedback_dialog____feedback_dialog_state.set_message", {value:_e0.target.value})], (_e0), {})} placeholder={`Ton message ici...`} rows={`5`} value={reflex___state____state__reseau___common___base_state____base_state__reseau___components___feedback_dialog____feedback_dialog_state.message}/>
  <RadixThemesFlex css={{"marginTop": "16px"}} justify={`end`} gap={`3`}>
  <RadixThemesDialog.Close>
  <RadixThemesButton color={`gray`} variant={`soft`}>
  {`Annuler`}
</RadixThemesButton>
</RadixThemesDialog.Close>
  <Fragment>
  {isTrue(reflex___state____state__reseau___common___base_state____base_state__reseau___components___feedback_dialog____feedback_dialog_state.message) ? (
  <Fragment>
  <RadixThemesDialog.Close>
  <RadixThemesButton type={`submit`}>
  {`Envoyer`}
</RadixThemesButton>
</RadixThemesDialog.Close>
</Fragment>
) : (
  <Fragment>
  <RadixThemesDialog.Close>
  <RadixThemesButton disabled={true} type={`submit`}>
  {`Envoyer`}
</RadixThemesButton>
</RadixThemesDialog.Close>
</Fragment>
)}
</Fragment>
</RadixThemesFlex>
</RadixFormRoot>
</RadixThemesFlex>
</RadixThemesDialog.Content>
</RadixThemesDialog.Root>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  )
}

export default function Component() {
  const [addEvents, connectErrors] = useContext(EventLoopContext);
  
    const logFrontendError = (error, info) => {
        if (process.env.NODE_ENV === "production") {
            addEvents([Event("reflex___state____state.reflex___state____frontend_event_exception_state.handle_frontend_exception", {
                stack: error.stack,
            })])
        }
    }
    

  return (
    <ErrorBoundary FallbackComponent={Fallback} onError={logFrontendError}>
  <Fragment>
  <Div_ac2a89ea84667d600a059f034bd91dfe/>
  <Toaster_6e90e5e87a1cac8c96c683214079bef3/>
</Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"width": "100%"}} direction={`column`} gap={`3`}>
  <Fragment_4ce3d32fe06533f833330f03365137ed/>
  <Fragment_6cb8c6d0d8b0e63639dac29a3aec04f1/>
</RadixThemesFlex>
  <NextHead>
  <title>
  {`Reseau`}
</title>
  <meta content={`favicon.ico`} property={`og:image`}/>
</NextHead>
</ErrorBoundary>
  )
}
