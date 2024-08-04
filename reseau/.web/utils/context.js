import { createContext, useContext, useMemo, useReducer, useState } from "react"
import { applyDelta, Event, hydrateClientStorage, useEventLoop, refs } from "/utils/state.js"

export const initialState = {"reflex___state____state": {"is_hydrated": false, "router": {"session": {"client_token": "", "client_ip": "", "session_id": ""}, "headers": {"host": "", "origin": "", "upgrade": "", "connection": "", "pragma": "", "cache_control": "", "user_agent": "", "sec_websocket_version": "", "sec_websocket_key": "", "sec_websocket_extensions": "", "accept_encoding": "", "accept_language": ""}, "page": {"host": "", "path": "", "raw_path": "", "full_path": "", "full_raw_path": "", "params": {}}}}, "reflex___state____state.abc____site_name_n7": {}, "reflex___state____state.abc____write_post_dialog_n1": {"content": "", "title": ""}, "reflex___state____state.abc____user_card_n5": {}, "reflex___state____state.abc____site_name_n4": {}, "reflex___state____state.abc____user_card_n6": {}, "reflex___state____state.reflex___state____update_vars_internal_state": {}, "reflex___state____state.abc____profile_chips_n1": {}, "reflex___state____state.abc____user_card_n3": {}, "reflex___state____state.abc____site_name_n9": {}, "reflex___state____state.abc____write_comment_form_n2": {"comment_value": ""}, "reflex___state____state.abc____site_name_n5": {}, "reflex___state____state.abc____write_post_dialog_n2": {"content": "", "title": ""}, "reflex___state____state.abc____site_name_n2": {}, "reflex___state____state.abc____user_card_n1": {}, "reflex___state____state.abc____user_card_n2": {}, "reflex___state____state.abc____post_dialog_n1": {}, "reflex___state____state.reflex___state____on_load_internal_state": {}, "reflex___state____state.reseau___common___base_state____base_state": {"auth_token": "", "authenticated_user": {"id": -1, "username": null, "email": null, "password_hash": null, "profile_text": null, "enabled": true, "city_id": null, "city": null, "interest_list": [], "post_list": [], "comment_list": [], "auth_session": null}, "is_authenticated": false}, "reflex___state____state.reseau___common___base_state____base_state.reseau___pages___home____home_state": {"own_profile_picture_exists": false, "post_author": null, "post_comments": [], "posts_displayed": [], "profile_pictures_exist": []}, "reflex___state____state.reseau___common___base_state____base_state.reseau___pages___members____members_state": {"city_searched": null, "search_term": "", "users_displayed": []}, "reflex___state____state.reseau___common___base_state____base_state.reseau___components___feedback_dialog____feedback_dialog_state": {"message": ""}, "reflex___state____state.reseau___common___base_state____base_state.reseau___pages___registration____registration_state": {"cities_as_str": [], "profile_img": "", "success": false}, "reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state": {"profile_img": "", "profile_text": "", "selected_interests_names": []}, "reflex___state____state.reseau___common___base_state____base_state.reseau___pages___log_in____log_in_state": {"redirect_to": "", "success": false}, "reflex___state____state.abc____navbar_n3": {}, "reflex___state____state.abc____user_card_n4": {}, "reflex___state____state.abc____profile_chips_n2": {}, "reflex___state____state.abc____site_name_n6": {}, "reflex___state____state.abc____post_dialog_n2": {}, "reflex___state____state.abc____navbar_n1": {}, "reflex___state____state.reflex___state____frontend_event_exception_state": {}, "reflex___state____state.abc____navbar_n5": {}, "reflex___state____state.abc____site_name_n1": {}, "reflex___state____state.abc____site_name_n8": {}, "reflex___state____state.abc____site_name_n10": {}, "reflex___state____state.abc____write_comment_form_n1": {"comment_value": ""}, "reflex___state____state.abc____navbar_n4": {}, "reflex___state____state.abc____navbar_n2": {}, "reflex___state____state.abc____site_name_n3": {}}

export const defaultColorMode = "light"
export const ColorModeContext = createContext(null);
export const UploadFilesContext = createContext(null);
export const DispatchContext = createContext(null);
export const StateContexts = {
  reflex___state____state: createContext(null),
  reflex___state____state__abc____site_name_n7: createContext(null),
  reflex___state____state__abc____write_post_dialog_n1: createContext(null),
  reflex___state____state__abc____user_card_n5: createContext(null),
  reflex___state____state__abc____site_name_n4: createContext(null),
  reflex___state____state__abc____user_card_n6: createContext(null),
  reflex___state____state__reflex___state____update_vars_internal_state: createContext(null),
  reflex___state____state__abc____profile_chips_n1: createContext(null),
  reflex___state____state__abc____user_card_n3: createContext(null),
  reflex___state____state__abc____site_name_n9: createContext(null),
  reflex___state____state__abc____write_comment_form_n2: createContext(null),
  reflex___state____state__abc____site_name_n5: createContext(null),
  reflex___state____state__abc____write_post_dialog_n2: createContext(null),
  reflex___state____state__abc____site_name_n2: createContext(null),
  reflex___state____state__abc____user_card_n1: createContext(null),
  reflex___state____state__abc____user_card_n2: createContext(null),
  reflex___state____state__abc____post_dialog_n1: createContext(null),
  reflex___state____state__reflex___state____on_load_internal_state: createContext(null),
  reflex___state____state__reseau___common___base_state____base_state: createContext(null),
  reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state: createContext(null),
  reflex___state____state__reseau___common___base_state____base_state__reseau___pages___members____members_state: createContext(null),
  reflex___state____state__reseau___common___base_state____base_state__reseau___components___feedback_dialog____feedback_dialog_state: createContext(null),
  reflex___state____state__reseau___common___base_state____base_state__reseau___pages___registration____registration_state: createContext(null),
  reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state: createContext(null),
  reflex___state____state__reseau___common___base_state____base_state__reseau___pages___log_in____log_in_state: createContext(null),
  reflex___state____state__abc____navbar_n3: createContext(null),
  reflex___state____state__abc____user_card_n4: createContext(null),
  reflex___state____state__abc____profile_chips_n2: createContext(null),
  reflex___state____state__abc____site_name_n6: createContext(null),
  reflex___state____state__abc____post_dialog_n2: createContext(null),
  reflex___state____state__abc____navbar_n1: createContext(null),
  reflex___state____state__reflex___state____frontend_event_exception_state: createContext(null),
  reflex___state____state__abc____navbar_n5: createContext(null),
  reflex___state____state__abc____site_name_n1: createContext(null),
  reflex___state____state__abc____site_name_n8: createContext(null),
  reflex___state____state__abc____site_name_n10: createContext(null),
  reflex___state____state__abc____write_comment_form_n1: createContext(null),
  reflex___state____state__abc____navbar_n4: createContext(null),
  reflex___state____state__abc____navbar_n2: createContext(null),
  reflex___state____state__abc____site_name_n3: createContext(null),
}
export const EventLoopContext = createContext(null);
export const clientStorage = {"cookies": {}, "local_storage": {"reflex___state____state.reseau___common___base_state____base_state.auth_token": {"name": "_auth_tokens", "sync": false}}, "session_storage": {}}

export const state_name = "reflex___state____state"

export const exception_state_name = "reflex___state____state.reflex___state____frontend_event_exception_state"

// Theses events are triggered on initial load and each page navigation.
export const onLoadInternalEvent = () => {
    const internal_events = [];

    // Get tracked cookie and local storage vars to send to the backend.
    const client_storage_vars = hydrateClientStorage(clientStorage);
    // But only send the vars if any are actually set in the browser.
    if (client_storage_vars && Object.keys(client_storage_vars).length !== 0) {
        internal_events.push(
            Event(
                'reflex___state____state.reflex___state____update_vars_internal_state.update_vars_internal',
                {vars: client_storage_vars},
            ),
        );
    }

    // `on_load_internal` triggers the correct on_load event(s) for the current page.
    // If the page does not define any on_load event, this will just set `is_hydrated = true`.
    internal_events.push(Event('reflex___state____state.reflex___state____on_load_internal_state.on_load_internal'));

    return internal_events;
}

// The following events are sent when the websocket connects or reconnects.
export const initialEvents = () => [
    Event('reflex___state____state.hydrate'),
    ...onLoadInternalEvent()
]

export const isDevMode = true

export const lastCompiledTimeStamp = "2024-08-03 19:41:31.321696"

export function UploadFilesProvider({ children }) {
  const [filesById, setFilesById] = useState({})
  refs["__clear_selected_files"] = (id) => setFilesById(filesById => {
    const newFilesById = {...filesById}
    delete newFilesById[id]
    return newFilesById
  })
  return (
    <UploadFilesContext.Provider value={[filesById, setFilesById]}>
      {children}
    </UploadFilesContext.Provider>
  )
}

export function EventLoopProvider({ children }) {
  const dispatch = useContext(DispatchContext)
  const [addEvents, connectErrors] = useEventLoop(
    dispatch,
    initialEvents,
    clientStorage,
  )
  return (
    <EventLoopContext.Provider value={[addEvents, connectErrors]}>
      {children}
    </EventLoopContext.Provider>
  )
}

export function StateProvider({ children }) {
  const [reflex___state____state, dispatch_reflex___state____state] = useReducer(applyDelta, initialState["reflex___state____state"])
  const [reflex___state____state__abc____site_name_n7, dispatch_reflex___state____state__abc____site_name_n7] = useReducer(applyDelta, initialState["reflex___state____state.abc____site_name_n7"])
  const [reflex___state____state__abc____write_post_dialog_n1, dispatch_reflex___state____state__abc____write_post_dialog_n1] = useReducer(applyDelta, initialState["reflex___state____state.abc____write_post_dialog_n1"])
  const [reflex___state____state__abc____user_card_n5, dispatch_reflex___state____state__abc____user_card_n5] = useReducer(applyDelta, initialState["reflex___state____state.abc____user_card_n5"])
  const [reflex___state____state__abc____site_name_n4, dispatch_reflex___state____state__abc____site_name_n4] = useReducer(applyDelta, initialState["reflex___state____state.abc____site_name_n4"])
  const [reflex___state____state__abc____user_card_n6, dispatch_reflex___state____state__abc____user_card_n6] = useReducer(applyDelta, initialState["reflex___state____state.abc____user_card_n6"])
  const [reflex___state____state__reflex___state____update_vars_internal_state, dispatch_reflex___state____state__reflex___state____update_vars_internal_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____update_vars_internal_state"])
  const [reflex___state____state__abc____profile_chips_n1, dispatch_reflex___state____state__abc____profile_chips_n1] = useReducer(applyDelta, initialState["reflex___state____state.abc____profile_chips_n1"])
  const [reflex___state____state__abc____user_card_n3, dispatch_reflex___state____state__abc____user_card_n3] = useReducer(applyDelta, initialState["reflex___state____state.abc____user_card_n3"])
  const [reflex___state____state__abc____site_name_n9, dispatch_reflex___state____state__abc____site_name_n9] = useReducer(applyDelta, initialState["reflex___state____state.abc____site_name_n9"])
  const [reflex___state____state__abc____write_comment_form_n2, dispatch_reflex___state____state__abc____write_comment_form_n2] = useReducer(applyDelta, initialState["reflex___state____state.abc____write_comment_form_n2"])
  const [reflex___state____state__abc____site_name_n5, dispatch_reflex___state____state__abc____site_name_n5] = useReducer(applyDelta, initialState["reflex___state____state.abc____site_name_n5"])
  const [reflex___state____state__abc____write_post_dialog_n2, dispatch_reflex___state____state__abc____write_post_dialog_n2] = useReducer(applyDelta, initialState["reflex___state____state.abc____write_post_dialog_n2"])
  const [reflex___state____state__abc____site_name_n2, dispatch_reflex___state____state__abc____site_name_n2] = useReducer(applyDelta, initialState["reflex___state____state.abc____site_name_n2"])
  const [reflex___state____state__abc____user_card_n1, dispatch_reflex___state____state__abc____user_card_n1] = useReducer(applyDelta, initialState["reflex___state____state.abc____user_card_n1"])
  const [reflex___state____state__abc____user_card_n2, dispatch_reflex___state____state__abc____user_card_n2] = useReducer(applyDelta, initialState["reflex___state____state.abc____user_card_n2"])
  const [reflex___state____state__abc____post_dialog_n1, dispatch_reflex___state____state__abc____post_dialog_n1] = useReducer(applyDelta, initialState["reflex___state____state.abc____post_dialog_n1"])
  const [reflex___state____state__reflex___state____on_load_internal_state, dispatch_reflex___state____state__reflex___state____on_load_internal_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____on_load_internal_state"])
  const [reflex___state____state__reseau___common___base_state____base_state, dispatch_reflex___state____state__reseau___common___base_state____base_state] = useReducer(applyDelta, initialState["reflex___state____state.reseau___common___base_state____base_state"])
  const [reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state, dispatch_reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state] = useReducer(applyDelta, initialState["reflex___state____state.reseau___common___base_state____base_state.reseau___pages___home____home_state"])
  const [reflex___state____state__reseau___common___base_state____base_state__reseau___pages___members____members_state, dispatch_reflex___state____state__reseau___common___base_state____base_state__reseau___pages___members____members_state] = useReducer(applyDelta, initialState["reflex___state____state.reseau___common___base_state____base_state.reseau___pages___members____members_state"])
  const [reflex___state____state__reseau___common___base_state____base_state__reseau___components___feedback_dialog____feedback_dialog_state, dispatch_reflex___state____state__reseau___common___base_state____base_state__reseau___components___feedback_dialog____feedback_dialog_state] = useReducer(applyDelta, initialState["reflex___state____state.reseau___common___base_state____base_state.reseau___components___feedback_dialog____feedback_dialog_state"])
  const [reflex___state____state__reseau___common___base_state____base_state__reseau___pages___registration____registration_state, dispatch_reflex___state____state__reseau___common___base_state____base_state__reseau___pages___registration____registration_state] = useReducer(applyDelta, initialState["reflex___state____state.reseau___common___base_state____base_state.reseau___pages___registration____registration_state"])
  const [reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state, dispatch_reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state] = useReducer(applyDelta, initialState["reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state"])
  const [reflex___state____state__reseau___common___base_state____base_state__reseau___pages___log_in____log_in_state, dispatch_reflex___state____state__reseau___common___base_state____base_state__reseau___pages___log_in____log_in_state] = useReducer(applyDelta, initialState["reflex___state____state.reseau___common___base_state____base_state.reseau___pages___log_in____log_in_state"])
  const [reflex___state____state__abc____navbar_n3, dispatch_reflex___state____state__abc____navbar_n3] = useReducer(applyDelta, initialState["reflex___state____state.abc____navbar_n3"])
  const [reflex___state____state__abc____user_card_n4, dispatch_reflex___state____state__abc____user_card_n4] = useReducer(applyDelta, initialState["reflex___state____state.abc____user_card_n4"])
  const [reflex___state____state__abc____profile_chips_n2, dispatch_reflex___state____state__abc____profile_chips_n2] = useReducer(applyDelta, initialState["reflex___state____state.abc____profile_chips_n2"])
  const [reflex___state____state__abc____site_name_n6, dispatch_reflex___state____state__abc____site_name_n6] = useReducer(applyDelta, initialState["reflex___state____state.abc____site_name_n6"])
  const [reflex___state____state__abc____post_dialog_n2, dispatch_reflex___state____state__abc____post_dialog_n2] = useReducer(applyDelta, initialState["reflex___state____state.abc____post_dialog_n2"])
  const [reflex___state____state__abc____navbar_n1, dispatch_reflex___state____state__abc____navbar_n1] = useReducer(applyDelta, initialState["reflex___state____state.abc____navbar_n1"])
  const [reflex___state____state__reflex___state____frontend_event_exception_state, dispatch_reflex___state____state__reflex___state____frontend_event_exception_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____frontend_event_exception_state"])
  const [reflex___state____state__abc____navbar_n5, dispatch_reflex___state____state__abc____navbar_n5] = useReducer(applyDelta, initialState["reflex___state____state.abc____navbar_n5"])
  const [reflex___state____state__abc____site_name_n1, dispatch_reflex___state____state__abc____site_name_n1] = useReducer(applyDelta, initialState["reflex___state____state.abc____site_name_n1"])
  const [reflex___state____state__abc____site_name_n8, dispatch_reflex___state____state__abc____site_name_n8] = useReducer(applyDelta, initialState["reflex___state____state.abc____site_name_n8"])
  const [reflex___state____state__abc____site_name_n10, dispatch_reflex___state____state__abc____site_name_n10] = useReducer(applyDelta, initialState["reflex___state____state.abc____site_name_n10"])
  const [reflex___state____state__abc____write_comment_form_n1, dispatch_reflex___state____state__abc____write_comment_form_n1] = useReducer(applyDelta, initialState["reflex___state____state.abc____write_comment_form_n1"])
  const [reflex___state____state__abc____navbar_n4, dispatch_reflex___state____state__abc____navbar_n4] = useReducer(applyDelta, initialState["reflex___state____state.abc____navbar_n4"])
  const [reflex___state____state__abc____navbar_n2, dispatch_reflex___state____state__abc____navbar_n2] = useReducer(applyDelta, initialState["reflex___state____state.abc____navbar_n2"])
  const [reflex___state____state__abc____site_name_n3, dispatch_reflex___state____state__abc____site_name_n3] = useReducer(applyDelta, initialState["reflex___state____state.abc____site_name_n3"])
  const dispatchers = useMemo(() => {
    return {
      "reflex___state____state": dispatch_reflex___state____state,
      "reflex___state____state.abc____site_name_n7": dispatch_reflex___state____state__abc____site_name_n7,
      "reflex___state____state.abc____write_post_dialog_n1": dispatch_reflex___state____state__abc____write_post_dialog_n1,
      "reflex___state____state.abc____user_card_n5": dispatch_reflex___state____state__abc____user_card_n5,
      "reflex___state____state.abc____site_name_n4": dispatch_reflex___state____state__abc____site_name_n4,
      "reflex___state____state.abc____user_card_n6": dispatch_reflex___state____state__abc____user_card_n6,
      "reflex___state____state.reflex___state____update_vars_internal_state": dispatch_reflex___state____state__reflex___state____update_vars_internal_state,
      "reflex___state____state.abc____profile_chips_n1": dispatch_reflex___state____state__abc____profile_chips_n1,
      "reflex___state____state.abc____user_card_n3": dispatch_reflex___state____state__abc____user_card_n3,
      "reflex___state____state.abc____site_name_n9": dispatch_reflex___state____state__abc____site_name_n9,
      "reflex___state____state.abc____write_comment_form_n2": dispatch_reflex___state____state__abc____write_comment_form_n2,
      "reflex___state____state.abc____site_name_n5": dispatch_reflex___state____state__abc____site_name_n5,
      "reflex___state____state.abc____write_post_dialog_n2": dispatch_reflex___state____state__abc____write_post_dialog_n2,
      "reflex___state____state.abc____site_name_n2": dispatch_reflex___state____state__abc____site_name_n2,
      "reflex___state____state.abc____user_card_n1": dispatch_reflex___state____state__abc____user_card_n1,
      "reflex___state____state.abc____user_card_n2": dispatch_reflex___state____state__abc____user_card_n2,
      "reflex___state____state.abc____post_dialog_n1": dispatch_reflex___state____state__abc____post_dialog_n1,
      "reflex___state____state.reflex___state____on_load_internal_state": dispatch_reflex___state____state__reflex___state____on_load_internal_state,
      "reflex___state____state.reseau___common___base_state____base_state": dispatch_reflex___state____state__reseau___common___base_state____base_state,
      "reflex___state____state.reseau___common___base_state____base_state.reseau___pages___home____home_state": dispatch_reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state,
      "reflex___state____state.reseau___common___base_state____base_state.reseau___pages___members____members_state": dispatch_reflex___state____state__reseau___common___base_state____base_state__reseau___pages___members____members_state,
      "reflex___state____state.reseau___common___base_state____base_state.reseau___components___feedback_dialog____feedback_dialog_state": dispatch_reflex___state____state__reseau___common___base_state____base_state__reseau___components___feedback_dialog____feedback_dialog_state,
      "reflex___state____state.reseau___common___base_state____base_state.reseau___pages___registration____registration_state": dispatch_reflex___state____state__reseau___common___base_state____base_state__reseau___pages___registration____registration_state,
      "reflex___state____state.reseau___common___base_state____base_state.reseau___pages___profile____profile_state": dispatch_reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state,
      "reflex___state____state.reseau___common___base_state____base_state.reseau___pages___log_in____log_in_state": dispatch_reflex___state____state__reseau___common___base_state____base_state__reseau___pages___log_in____log_in_state,
      "reflex___state____state.abc____navbar_n3": dispatch_reflex___state____state__abc____navbar_n3,
      "reflex___state____state.abc____user_card_n4": dispatch_reflex___state____state__abc____user_card_n4,
      "reflex___state____state.abc____profile_chips_n2": dispatch_reflex___state____state__abc____profile_chips_n2,
      "reflex___state____state.abc____site_name_n6": dispatch_reflex___state____state__abc____site_name_n6,
      "reflex___state____state.abc____post_dialog_n2": dispatch_reflex___state____state__abc____post_dialog_n2,
      "reflex___state____state.abc____navbar_n1": dispatch_reflex___state____state__abc____navbar_n1,
      "reflex___state____state.reflex___state____frontend_event_exception_state": dispatch_reflex___state____state__reflex___state____frontend_event_exception_state,
      "reflex___state____state.abc____navbar_n5": dispatch_reflex___state____state__abc____navbar_n5,
      "reflex___state____state.abc____site_name_n1": dispatch_reflex___state____state__abc____site_name_n1,
      "reflex___state____state.abc____site_name_n8": dispatch_reflex___state____state__abc____site_name_n8,
      "reflex___state____state.abc____site_name_n10": dispatch_reflex___state____state__abc____site_name_n10,
      "reflex___state____state.abc____write_comment_form_n1": dispatch_reflex___state____state__abc____write_comment_form_n1,
      "reflex___state____state.abc____navbar_n4": dispatch_reflex___state____state__abc____navbar_n4,
      "reflex___state____state.abc____navbar_n2": dispatch_reflex___state____state__abc____navbar_n2,
      "reflex___state____state.abc____site_name_n3": dispatch_reflex___state____state__abc____site_name_n3,
    }
  }, [])

  return (
    <StateContexts.reflex___state____state.Provider value={ reflex___state____state }>
    <StateContexts.reflex___state____state__abc____site_name_n7.Provider value={ reflex___state____state__abc____site_name_n7 }>
    <StateContexts.reflex___state____state__abc____write_post_dialog_n1.Provider value={ reflex___state____state__abc____write_post_dialog_n1 }>
    <StateContexts.reflex___state____state__abc____user_card_n5.Provider value={ reflex___state____state__abc____user_card_n5 }>
    <StateContexts.reflex___state____state__abc____site_name_n4.Provider value={ reflex___state____state__abc____site_name_n4 }>
    <StateContexts.reflex___state____state__abc____user_card_n6.Provider value={ reflex___state____state__abc____user_card_n6 }>
    <StateContexts.reflex___state____state__reflex___state____update_vars_internal_state.Provider value={ reflex___state____state__reflex___state____update_vars_internal_state }>
    <StateContexts.reflex___state____state__abc____profile_chips_n1.Provider value={ reflex___state____state__abc____profile_chips_n1 }>
    <StateContexts.reflex___state____state__abc____user_card_n3.Provider value={ reflex___state____state__abc____user_card_n3 }>
    <StateContexts.reflex___state____state__abc____site_name_n9.Provider value={ reflex___state____state__abc____site_name_n9 }>
    <StateContexts.reflex___state____state__abc____write_comment_form_n2.Provider value={ reflex___state____state__abc____write_comment_form_n2 }>
    <StateContexts.reflex___state____state__abc____site_name_n5.Provider value={ reflex___state____state__abc____site_name_n5 }>
    <StateContexts.reflex___state____state__abc____write_post_dialog_n2.Provider value={ reflex___state____state__abc____write_post_dialog_n2 }>
    <StateContexts.reflex___state____state__abc____site_name_n2.Provider value={ reflex___state____state__abc____site_name_n2 }>
    <StateContexts.reflex___state____state__abc____user_card_n1.Provider value={ reflex___state____state__abc____user_card_n1 }>
    <StateContexts.reflex___state____state__abc____user_card_n2.Provider value={ reflex___state____state__abc____user_card_n2 }>
    <StateContexts.reflex___state____state__abc____post_dialog_n1.Provider value={ reflex___state____state__abc____post_dialog_n1 }>
    <StateContexts.reflex___state____state__reflex___state____on_load_internal_state.Provider value={ reflex___state____state__reflex___state____on_load_internal_state }>
    <StateContexts.reflex___state____state__reseau___common___base_state____base_state.Provider value={ reflex___state____state__reseau___common___base_state____base_state }>
    <StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state.Provider value={ reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state }>
    <StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___pages___members____members_state.Provider value={ reflex___state____state__reseau___common___base_state____base_state__reseau___pages___members____members_state }>
    <StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___components___feedback_dialog____feedback_dialog_state.Provider value={ reflex___state____state__reseau___common___base_state____base_state__reseau___components___feedback_dialog____feedback_dialog_state }>
    <StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___pages___registration____registration_state.Provider value={ reflex___state____state__reseau___common___base_state____base_state__reseau___pages___registration____registration_state }>
    <StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.Provider value={ reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state }>
    <StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___pages___log_in____log_in_state.Provider value={ reflex___state____state__reseau___common___base_state____base_state__reseau___pages___log_in____log_in_state }>
    <StateContexts.reflex___state____state__abc____navbar_n3.Provider value={ reflex___state____state__abc____navbar_n3 }>
    <StateContexts.reflex___state____state__abc____user_card_n4.Provider value={ reflex___state____state__abc____user_card_n4 }>
    <StateContexts.reflex___state____state__abc____profile_chips_n2.Provider value={ reflex___state____state__abc____profile_chips_n2 }>
    <StateContexts.reflex___state____state__abc____site_name_n6.Provider value={ reflex___state____state__abc____site_name_n6 }>
    <StateContexts.reflex___state____state__abc____post_dialog_n2.Provider value={ reflex___state____state__abc____post_dialog_n2 }>
    <StateContexts.reflex___state____state__abc____navbar_n1.Provider value={ reflex___state____state__abc____navbar_n1 }>
    <StateContexts.reflex___state____state__reflex___state____frontend_event_exception_state.Provider value={ reflex___state____state__reflex___state____frontend_event_exception_state }>
    <StateContexts.reflex___state____state__abc____navbar_n5.Provider value={ reflex___state____state__abc____navbar_n5 }>
    <StateContexts.reflex___state____state__abc____site_name_n1.Provider value={ reflex___state____state__abc____site_name_n1 }>
    <StateContexts.reflex___state____state__abc____site_name_n8.Provider value={ reflex___state____state__abc____site_name_n8 }>
    <StateContexts.reflex___state____state__abc____site_name_n10.Provider value={ reflex___state____state__abc____site_name_n10 }>
    <StateContexts.reflex___state____state__abc____write_comment_form_n1.Provider value={ reflex___state____state__abc____write_comment_form_n1 }>
    <StateContexts.reflex___state____state__abc____navbar_n4.Provider value={ reflex___state____state__abc____navbar_n4 }>
    <StateContexts.reflex___state____state__abc____navbar_n2.Provider value={ reflex___state____state__abc____navbar_n2 }>
    <StateContexts.reflex___state____state__abc____site_name_n3.Provider value={ reflex___state____state__abc____site_name_n3 }>
      <DispatchContext.Provider value={dispatchers}>
        {children}
      </DispatchContext.Provider>
    </StateContexts.reflex___state____state__abc____site_name_n3.Provider>
    </StateContexts.reflex___state____state__abc____navbar_n2.Provider>
    </StateContexts.reflex___state____state__abc____navbar_n4.Provider>
    </StateContexts.reflex___state____state__abc____write_comment_form_n1.Provider>
    </StateContexts.reflex___state____state__abc____site_name_n10.Provider>
    </StateContexts.reflex___state____state__abc____site_name_n8.Provider>
    </StateContexts.reflex___state____state__abc____site_name_n1.Provider>
    </StateContexts.reflex___state____state__abc____navbar_n5.Provider>
    </StateContexts.reflex___state____state__reflex___state____frontend_event_exception_state.Provider>
    </StateContexts.reflex___state____state__abc____navbar_n1.Provider>
    </StateContexts.reflex___state____state__abc____post_dialog_n2.Provider>
    </StateContexts.reflex___state____state__abc____site_name_n6.Provider>
    </StateContexts.reflex___state____state__abc____profile_chips_n2.Provider>
    </StateContexts.reflex___state____state__abc____user_card_n4.Provider>
    </StateContexts.reflex___state____state__abc____navbar_n3.Provider>
    </StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___pages___log_in____log_in_state.Provider>
    </StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___pages___profile____profile_state.Provider>
    </StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___pages___registration____registration_state.Provider>
    </StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___components___feedback_dialog____feedback_dialog_state.Provider>
    </StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___pages___members____members_state.Provider>
    </StateContexts.reflex___state____state__reseau___common___base_state____base_state__reseau___pages___home____home_state.Provider>
    </StateContexts.reflex___state____state__reseau___common___base_state____base_state.Provider>
    </StateContexts.reflex___state____state__reflex___state____on_load_internal_state.Provider>
    </StateContexts.reflex___state____state__abc____post_dialog_n1.Provider>
    </StateContexts.reflex___state____state__abc____user_card_n2.Provider>
    </StateContexts.reflex___state____state__abc____user_card_n1.Provider>
    </StateContexts.reflex___state____state__abc____site_name_n2.Provider>
    </StateContexts.reflex___state____state__abc____write_post_dialog_n2.Provider>
    </StateContexts.reflex___state____state__abc____site_name_n5.Provider>
    </StateContexts.reflex___state____state__abc____write_comment_form_n2.Provider>
    </StateContexts.reflex___state____state__abc____site_name_n9.Provider>
    </StateContexts.reflex___state____state__abc____user_card_n3.Provider>
    </StateContexts.reflex___state____state__abc____profile_chips_n1.Provider>
    </StateContexts.reflex___state____state__reflex___state____update_vars_internal_state.Provider>
    </StateContexts.reflex___state____state__abc____user_card_n6.Provider>
    </StateContexts.reflex___state____state__abc____site_name_n4.Provider>
    </StateContexts.reflex___state____state__abc____user_card_n5.Provider>
    </StateContexts.reflex___state____state__abc____write_post_dialog_n1.Provider>
    </StateContexts.reflex___state____state__abc____site_name_n7.Provider>
    </StateContexts.reflex___state____state.Provider>
  )
}