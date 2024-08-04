/** @jsxImportSource @emotion/react */


import { ErrorBoundary } from "react-error-boundary"
import { Fragment, useCallback, useContext, useEffect, useRef, useState } from "react"
import { ColorModeContext, EventLoopContext, StateContexts } from "/utils/context"
import { Event, getBackendURL, getRefValue, getRefValues, isTrue, refs } from "/utils/state"
import { CirclePlusIcon as LucideCirclePlusIcon, CircleXIcon as LucideCircleXIcon, HandHeartIcon as LucideHandHeartIcon, MessageSquareQuoteIcon as LucideMessageSquareQuoteIcon, MoonIcon as LucideMoonIcon, SunIcon as LucideSunIcon, UserSearchIcon as LucideUserSearchIcon, WifiOffIcon as LucideWifiOffIcon } from "lucide-react"
import { keyframes } from "@emotion/react"
import { toast, Toaster } from "sonner"
import env from "/env.json"
import { Badge as RadixThemesBadge, Box as RadixThemesBox, Button as RadixThemesButton, Container as RadixThemesContainer, Dialog as RadixThemesDialog, Flex as RadixThemesFlex, Heading as RadixThemesHeading, IconButton as RadixThemesIconButton, Link as RadixThemesLink, Separator as RadixThemesSeparator, Text as RadixThemesText, TextArea as RadixThemesTextArea } from "@radix-ui/themes"
import NextLink from "next/link"
import ReactDropzone from "react-dropzone"
import { DebounceInput } from "react-debounce-input"
import { Root as RadixFormRoot } from "@radix-ui/react-form"
import NextHead from "next/head"



const pulse = keyframes`
    0% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
`


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

export function Fragment_840509c07b74195c8e95dddd16385a86 () {
  const reflex___state____state__reseau___common___base_state____base_state = useContext(StateContexts.reflex___state____state__reseau___common___base_state____base_state)
  const { resolvedColorMode } = useContext(ColorModeContext)
  const reflex___state____state = useContext(StateContexts.reflex___state____state)
  const { toggleColorMode } = useContext(ColorModeContext)
  const [addEvents, connectErrors] = useContext(EventLoopContext);
  const ref_profile_img = useRef(null); refs['ref_profile_img'] = ref_profile_img;
  const reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state = useContext(StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state)



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
  <Fragment>
  {isTrue(reflex___state____state.is_hydrated) ? (
  <Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`3`}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"width": "100%"}} direction={`row`} justify={`between`} gap={`3`}>
  <RadixThemesHeading css={{"marginBottom": "0.5em"}} size={`5`}>
  {`Ton profil`}
</RadixThemesHeading>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesIconButton css={{"padding": "6px", "paddingTop": "0", "background": "transparent", "color": "inherit", "zIndex": "20", "&:hover": {"cursor": "pointer"}}} onClick={toggleColorMode}>
  <Fragment>
  {isTrue(((resolvedColorMode) === (`light`))) ? (
  <Fragment>
  <LucideSunIcon css={{"color": "var(--current-color)"}}/>
</Fragment>
) : (
  <Fragment>
  <LucideMoonIcon css={{"color": "var(--current-color)"}}/>
</Fragment>
)}
</Fragment>
</RadixThemesIconButton>
</RadixThemesBox>
</RadixThemesFlex>
  <RadixThemesBox css={{"width": "100%", "@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"width": "100%"}} direction={`row`} gap={`3`}>
  <ReactDropzone accept={{"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]}} id={`profile_img`} multiple={false} onDrop={(_files) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.handle_upload", {files:_files,upload_id:`profile_img`}, "uploadFiles")], (_files), {})} ref={ref_profile_img}>
  {({ getRootProps, getInputProps }) => (
    <RadixThemesBox className={`rx-Upload`} css={{"padding": "0", "@media screen and (min-width: 0)": {"width": "64px", "height": "64px"}, "@media screen and (min-width: 30em)": {"width": "96px", "height": "80px"}, "border": "none", "textAlign": "center"}} id={`profile_img`} ref={ref_profile_img} {...getRootProps()}>
    <input type={`file`} {...getInputProps()}/>
    <img css={{"@media screen and (min-width: 0)": {"width": "64px", "height": "64px"}, "@media screen and (min-width: 30em)": {"width": "80px", "height": "80px"}, "border": "1px solid #ccc", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/${reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.profile_img}`}/>
  </RadixThemesBox>
  )}
</ReactDropzone>
  <RadixThemesBox css={{"width": "100%"}}>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <DebounceInput css={{"width": "100%", "height": "9vh"}} debounceTimeout={300} element={RadixThemesTextArea} maxLength={300} onChange={(_e0) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.set_profile_text", {value:_e0.target.value})], (_e0), {})} placeholder={`Quelles sont tes passions ?                    
Qu'est-ce qui te fait vibrer ?`} rows={`2`} size={`3`} value={reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.profile_text}/>
</RadixThemesBox>
  <RadixThemesBox css={{"width": "100%", "@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <DebounceInput css={{"width": "100%", "height": "12vh"}} debounceTimeout={300} element={RadixThemesTextArea} maxLength={300} onChange={(_e0) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.set_profile_text", {value:_e0.target.value})], (_e0), {})} placeholder={`Quelles sont tes passions ?                    
Qu'est-ce qui te fait vibrer ?`} rows={`5`} value={reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.profile_text}/>
</RadixThemesBox>
</RadixThemesBox>
</RadixThemesFlex>
</RadixThemesBox>
  <RadixThemesBox css={{"width": "100%", "@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`3`}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"width": "100%"}} direction={`row`} justify={`between`} gap={`3`}>
  <ReactDropzone accept={{"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]}} id={`profile_img`} multiple={false} onDrop={(_files) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.handle_upload", {files:_files,upload_id:`profile_img`}, "uploadFiles")], (_files), {})} ref={ref_profile_img}>
  {({ getRootProps, getInputProps }) => (
    <RadixThemesBox className={`rx-Upload`} css={{"padding": "0", "@media screen and (min-width: 0)": {"height": "4em"}, "border": "none", "textAlign": "center"}} id={`profile_img`} ref={ref_profile_img} {...getRootProps()}>
    <input type={`file`} {...getInputProps()}/>
    <img css={{"@media screen and (min-width: 0)": {"width": "4em", "height": "4em"}, "border": "1px solid #ccc", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/${reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.profile_img}`}/>
  </RadixThemesBox>
  )}
</ReactDropzone>
  <RadixThemesIconButton css={{"padding": "6px", "background": "transparent", "color": "inherit", "zIndex": "20", "&:hover": {"cursor": "pointer"}}} onClick={toggleColorMode}>
  <Fragment>
  {isTrue(((resolvedColorMode) === (`light`))) ? (
  <Fragment>
  <LucideSunIcon css={{"color": "var(--current-color)"}}/>
</Fragment>
) : (
  <Fragment>
  <LucideMoonIcon css={{"color": "var(--current-color)"}}/>
</Fragment>
)}
</Fragment>
</RadixThemesIconButton>
</RadixThemesFlex>
  <RadixThemesBox css={{"width": "100%"}}>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <DebounceInput css={{"width": "100%", "height": "9vh"}} debounceTimeout={300} element={RadixThemesTextArea} maxLength={300} onChange={(_e0) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.set_profile_text", {value:_e0.target.value})], (_e0), {})} placeholder={`Quelles sont tes passions ?                    
Qu'est-ce qui te fait vibrer ?`} rows={`2`} size={`3`} value={reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.profile_text}/>
</RadixThemesBox>
  <RadixThemesBox css={{"width": "100%", "@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <DebounceInput css={{"width": "100%", "height": "12vh"}} debounceTimeout={300} element={RadixThemesTextArea} maxLength={300} onChange={(_e0) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.set_profile_text", {value:_e0.target.value})], (_e0), {})} placeholder={`Quelles sont tes passions ?                    
Qu'est-ce qui te fait vibrer ?`} rows={`5`} value={reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.profile_text}/>
</RadixThemesBox>
</RadixThemesBox>
</RadixThemesFlex>
</RadixThemesBox>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"justifyContent": "start", "alignItems": "start", "width": "100%", "marginTop": "1em"}} direction={`column`} gap={`3`}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"width": "100%", "marginBottom": "0.5em"}} direction={`row`} gap={`1`}>
  <LucideHandHeartIcon css={{"color": "var(--current-color)"}} size={20}/>
  <RadixThemesHeading size={`3`}>
  {`Intérêts`}
</RadixThemesHeading>
</RadixThemesFlex>
  <RadixThemesFlex css={{"justifyContent": "start"}} gap={`2`} wrap={`wrap`}>
  {reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.selected_interests_names.map((item, index_6d54c5b91d28e21c) => (
  <RadixThemesBadge color={`green`} css={{"&:hover": {"opacity": 0.75}, "cursor": "pointer"}} key={index_6d54c5b91d28e21c} onClick={(_e) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.remove_selected", {item:item})], (_e), {})} radius={`full`} size={`3`} variant={`surface`}>
  {item}
  <LucideCircleXIcon css={{"color": "var(--current-color)"}} size={18}/>
</RadixThemesBadge>
))}
</RadixThemesFlex>
  <RadixThemesSeparator size={`4`}/>
  <RadixThemesFlex css={{"justifyContent": "start"}} gap={`2`} wrap={`wrap`}>
  {["Business", "Mental", "Physique", "Relations"].map((item, index_51b7d3d901c2803a) => (
  <Fragment key={index_51b7d3d901c2803a}>
  {isTrue(reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.selected_interests_names.includes(item)) ? (
  <Fragment/>
) : (
  <Fragment>
  <RadixThemesBadge color={`gray`} css={{"&:hover": {"opacity": 0.75}, "cursor": "pointer"}} onClick={(_e) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.add_selected", {item:item})], (_e), {})} radius={`full`} size={`3`} variant={`surface`}>
  {item}
  <LucideCirclePlusIcon css={{"color": "var(--current-color)"}} size={18}/>
</RadixThemesBadge>
</Fragment>
)}
</Fragment>
))}
</RadixThemesFlex>
</RadixThemesFlex>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"width": "100%", "marginTop": "1em"}} direction={`row`} justify={`between`} gap={`3`}>
  <RadixThemesButton onClick={(_e) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.save_profile", {})], (_e), {})} size={`3`}>
  {`Valider`}
</RadixThemesButton>
  <RadixThemesLink asChild={true} css={{"&:hover": {"color": "var(--accent-8)"}}} onClick={(_e) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.do_logout", {})], (_e), {})} underline={`none`}>
  <NextLink href={`/`} passHref={true}>
  {`Se déconnecter`}
</NextLink>
</RadixThemesLink>
</RadixThemesFlex>
</RadixThemesFlex>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
</Fragment>
</RadixThemesContainer>
</RadixThemesBox>
</Fragment>
) : (
  <Fragment>
  <RadixThemesBox>
  <Fragment>
  <Fragment>
  {isTrue(reflex___state____state.is_hydrated) ? (
  <Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`3`}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"width": "100%"}} direction={`row`} justify={`between`} gap={`3`}>
  <RadixThemesHeading css={{"marginBottom": "0.5em"}} size={`5`}>
  {`Ton profil`}
</RadixThemesHeading>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesIconButton css={{"padding": "6px", "paddingTop": "0", "background": "transparent", "color": "inherit", "zIndex": "20", "&:hover": {"cursor": "pointer"}}} onClick={toggleColorMode}>
  <Fragment>
  {isTrue(((resolvedColorMode) === (`light`))) ? (
  <Fragment>
  <LucideSunIcon css={{"color": "var(--current-color)"}}/>
</Fragment>
) : (
  <Fragment>
  <LucideMoonIcon css={{"color": "var(--current-color)"}}/>
</Fragment>
)}
</Fragment>
</RadixThemesIconButton>
</RadixThemesBox>
</RadixThemesFlex>
  <RadixThemesBox css={{"width": "100%", "@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"width": "100%"}} direction={`row`} gap={`3`}>
  <ReactDropzone accept={{"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]}} id={`profile_img`} multiple={false} onDrop={(_files) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.handle_upload", {files:_files,upload_id:`profile_img`}, "uploadFiles")], (_files), {})} ref={ref_profile_img}>
  {({ getRootProps, getInputProps }) => (
    <RadixThemesBox className={`rx-Upload`} css={{"padding": "0", "@media screen and (min-width: 0)": {"width": "64px", "height": "64px"}, "@media screen and (min-width: 30em)": {"width": "96px", "height": "80px"}, "border": "none", "textAlign": "center"}} id={`profile_img`} ref={ref_profile_img} {...getRootProps()}>
    <input type={`file`} {...getInputProps()}/>
    <img css={{"@media screen and (min-width: 0)": {"width": "64px", "height": "64px"}, "@media screen and (min-width: 30em)": {"width": "80px", "height": "80px"}, "border": "1px solid #ccc", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/${reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.profile_img}`}/>
  </RadixThemesBox>
  )}
</ReactDropzone>
  <RadixThemesBox css={{"width": "100%"}}>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <DebounceInput css={{"width": "100%", "height": "9vh"}} debounceTimeout={300} element={RadixThemesTextArea} maxLength={300} onChange={(_e0) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.set_profile_text", {value:_e0.target.value})], (_e0), {})} placeholder={`Quelles sont tes passions ?                    
Qu'est-ce qui te fait vibrer ?`} rows={`2`} size={`3`} value={reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.profile_text}/>
</RadixThemesBox>
  <RadixThemesBox css={{"width": "100%", "@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <DebounceInput css={{"width": "100%", "height": "12vh"}} debounceTimeout={300} element={RadixThemesTextArea} maxLength={300} onChange={(_e0) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.set_profile_text", {value:_e0.target.value})], (_e0), {})} placeholder={`Quelles sont tes passions ?                    
Qu'est-ce qui te fait vibrer ?`} rows={`5`} value={reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.profile_text}/>
</RadixThemesBox>
</RadixThemesBox>
</RadixThemesFlex>
</RadixThemesBox>
  <RadixThemesBox css={{"width": "100%", "@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`3`}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"width": "100%"}} direction={`row`} justify={`between`} gap={`3`}>
  <ReactDropzone accept={{"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]}} id={`profile_img`} multiple={false} onDrop={(_files) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.handle_upload", {files:_files,upload_id:`profile_img`}, "uploadFiles")], (_files), {})} ref={ref_profile_img}>
  {({ getRootProps, getInputProps }) => (
    <RadixThemesBox className={`rx-Upload`} css={{"padding": "0", "@media screen and (min-width: 0)": {"height": "4em"}, "border": "none", "textAlign": "center"}} id={`profile_img`} ref={ref_profile_img} {...getRootProps()}>
    <input type={`file`} {...getInputProps()}/>
    <img css={{"@media screen and (min-width: 0)": {"width": "4em", "height": "4em"}, "border": "1px solid #ccc", "borderRadius": "50%"}} src={`${getBackendURL(env.UPLOAD)}/${reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.profile_img}`}/>
  </RadixThemesBox>
  )}
</ReactDropzone>
  <RadixThemesIconButton css={{"padding": "6px", "background": "transparent", "color": "inherit", "zIndex": "20", "&:hover": {"cursor": "pointer"}}} onClick={toggleColorMode}>
  <Fragment>
  {isTrue(((resolvedColorMode) === (`light`))) ? (
  <Fragment>
  <LucideSunIcon css={{"color": "var(--current-color)"}}/>
</Fragment>
) : (
  <Fragment>
  <LucideMoonIcon css={{"color": "var(--current-color)"}}/>
</Fragment>
)}
</Fragment>
</RadixThemesIconButton>
</RadixThemesFlex>
  <RadixThemesBox css={{"width": "100%"}}>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <DebounceInput css={{"width": "100%", "height": "9vh"}} debounceTimeout={300} element={RadixThemesTextArea} maxLength={300} onChange={(_e0) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.set_profile_text", {value:_e0.target.value})], (_e0), {})} placeholder={`Quelles sont tes passions ?                    
Qu'est-ce qui te fait vibrer ?`} rows={`2`} size={`3`} value={reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.profile_text}/>
</RadixThemesBox>
  <RadixThemesBox css={{"width": "100%", "@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <DebounceInput css={{"width": "100%", "height": "12vh"}} debounceTimeout={300} element={RadixThemesTextArea} maxLength={300} onChange={(_e0) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.set_profile_text", {value:_e0.target.value})], (_e0), {})} placeholder={`Quelles sont tes passions ?                    
Qu'est-ce qui te fait vibrer ?`} rows={`5`} value={reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.profile_text}/>
</RadixThemesBox>
</RadixThemesBox>
</RadixThemesFlex>
</RadixThemesBox>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"justifyContent": "start", "alignItems": "start", "width": "100%", "marginTop": "1em"}} direction={`column`} gap={`3`}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"width": "100%", "marginBottom": "0.5em"}} direction={`row`} gap={`1`}>
  <LucideHandHeartIcon css={{"color": "var(--current-color)"}} size={20}/>
  <RadixThemesHeading size={`3`}>
  {`Intérêts`}
</RadixThemesHeading>
</RadixThemesFlex>
  <RadixThemesFlex css={{"justifyContent": "start"}} gap={`2`} wrap={`wrap`}>
  {reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.selected_interests_names.map((item, index_6d54c5b91d28e21c) => (
  <RadixThemesBadge color={`green`} css={{"&:hover": {"opacity": 0.75}, "cursor": "pointer"}} key={index_6d54c5b91d28e21c} onClick={(_e) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.remove_selected", {item:item})], (_e), {})} radius={`full`} size={`3`} variant={`surface`}>
  {item}
  <LucideCircleXIcon css={{"color": "var(--current-color)"}} size={18}/>
</RadixThemesBadge>
))}
</RadixThemesFlex>
  <RadixThemesSeparator size={`4`}/>
  <RadixThemesFlex css={{"justifyContent": "start"}} gap={`2`} wrap={`wrap`}>
  {["Business", "Mental", "Physique", "Relations"].map((item, index_51b7d3d901c2803a) => (
  <Fragment key={index_51b7d3d901c2803a}>
  {isTrue(reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.selected_interests_names.includes(item)) ? (
  <Fragment/>
) : (
  <Fragment>
  <RadixThemesBadge color={`gray`} css={{"&:hover": {"opacity": 0.75}, "cursor": "pointer"}} onClick={(_e) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.add_selected", {item:item})], (_e), {})} radius={`full`} size={`3`} variant={`surface`}>
  {item}
  <LucideCirclePlusIcon css={{"color": "var(--current-color)"}} size={18}/>
</RadixThemesBadge>
</Fragment>
)}
</Fragment>
))}
</RadixThemesFlex>
</RadixThemesFlex>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"width": "100%", "marginTop": "1em"}} direction={`row`} justify={`between`} gap={`3`}>
  <RadixThemesButton onClick={(_e) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state.save_profile", {})], (_e), {})} size={`3`}>
  {`Valider`}
</RadixThemesButton>
  <RadixThemesLink asChild={true} css={{"&:hover": {"color": "var(--accent-8)"}}} onClick={(_e) => addEvents([Event("reflex___state____state.reseau___common___base_state____base_state.do_logout", {})], (_e), {})} underline={`none`}>
  <NextLink href={`/`} passHref={true}>
  {`Se déconnecter`}
</NextLink>
</RadixThemesLink>
</RadixThemesFlex>
</RadixThemesFlex>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
</Fragment>
</RadixThemesBox>
</Fragment>
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
            

export function Div_ac2a89ea84667d600a059f034bd91dfe () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    <div css={{"position": "fixed", "width": "100vw", "height": "0"}} title={`Connection Error: ${(connectErrors.length > 0) ? connectErrors[connectErrors.length - 1].message : ''}`}>
  <Fragment_cf53a535ae2e610a113dd361eb6ac95b/>
</div>
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
  <Fragment_840509c07b74195c8e95dddd16385a86/>
  <Fragment_6cb8c6d0d8b0e63639dac29a3aec04f1/>
</RadixThemesFlex>
  <NextHead>
  <title>
  {`Profil`}
</title>
  <meta content={`favicon.ico`} property={`og:image`}/>
</NextHead>
</ErrorBoundary>
  )
}
