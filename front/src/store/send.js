import {
  titleValidation,
  contentValidation,
  tosValidation,
  writerValidation,
  attachmentsValidation
} from "./send_validate"

export default {
  namespaced: true,
  state: {
    title: {
      value: "",
      is_dirty: false,
      error_messages: []
    },
    content: {
      value: "",
      is_dirty: false,
      error_messages: []
    },
    tos: {
      value: [],
      is_dirty: false,
      error_messages: []
    },
    writer: {
      value: null,
      is_dirty: false,
      error_messages: []
    },
    attachments: {
      value: [],
      is_dirty: false,
      error_messages: []
    },
    send_at: {
      value: null,
      is_dirty: false,
      error_messages: []
    },
  },
  mutations: {
    setTitle (state, payload) {
      // payload: String, title value
      state.title.value = payload;
      state.title.error_messages = titleValidation(state.title.value);
      state.title.is_dirty = true;
    },
    setContent (state, payload) {
      // payload: String, content value
      state.content.value = payload;
      state.content.error_messages = contentValidation(state.content.value);
      state.content.is_dirty = true;
    },
    setTos (state, payload) {
      // payload: List of Number, tos value
      state.tos.value = payload;
      state.tos.error_messages = tosValidation(state.tos.value);
      state.tos.is_dirty = true;
    },
    setWriter (state, payload) {
      // payload: Number, writer value
      state.writer.value = payload;
      state.writer.error_messages = writerValidation(state.writer.value);
      state.writer.is_dirty = true;
    },
    setAttachments (state, payload) {
      // payload: List of File, attachments value
      state.attachments.value = payload;
      state.attachments.error_messages = attachmentsValidation(state.attachments.value);
      state.attachments.is_dirty = true;
    },
  }
}