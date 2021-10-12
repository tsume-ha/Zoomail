import {
  titleValidation,
  textValidation
} from "./send_validate"

export default {
  namespaced: true,
  state: {
    title: {
      value: "",
      is_dirty: false,
      error_messages: []
    },
    text: {
      value: "",
      is_dirty: false,
      error_messages: []
    },
    tos: {
      value: [],
      is_dirty: false,
      error_messages: []
    },
    writer_id: {
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
    setText (state, payload) {
      // payload: String, text value
      state.text.value = payload;
      state.text.error_messages = textValidation(state.text.value);
      state.text.is_dirty = true;
    }
  }
}