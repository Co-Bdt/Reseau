/** @jsxImportSource @emotion/react */

import '/styles/styles.css'

import RadixThemesColorModeProvider from "/components/reflex/radix_themes_color_mode_provider.js"
import { Theme as RadixThemesTheme } from "@radix-ui/themes"
import theme from "/utils/theme.js"
import { UploadFilesProvider } from "/utils/context"
import { Fragment } from "react"


import { EventLoopProvider, StateProvider, defaultColorMode } from "/utils/context.js";
import { ThemeProvider } from 'next-themes'


function AppWrap({children}) {


  return (
    <RadixThemesColorModeProvider>
  <RadixThemesTheme accentColor={`amber`} css={{...theme.styles.global[':root'], ...theme.styles.global.body}}>
  <UploadFilesProvider>
  <Fragment>
  {children}
</Fragment>
</UploadFilesProvider>
</RadixThemesTheme>
</RadixThemesColorModeProvider>
  )
}

export default function MyApp({ Component, pageProps }) {
  return (
    <ThemeProvider defaultTheme={ defaultColorMode } storageKey="chakra-ui-color-mode" attribute="class">
      <AppWrap>
        <StateProvider>
          <EventLoopProvider>
            <Component {...pageProps} />
          </EventLoopProvider>
        </StateProvider>
      </AppWrap>
    </ThemeProvider>
  );
}

