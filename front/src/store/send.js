import {
  titleValidation,
  contentValidation,
  tosValidation,
  writerValidation,
  attachmentsValidation
} from "./send_validate";
import axios from '../utils/axios';

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
    validateAll (state) {
      // すべてのフィールドをValidate
      state.title.error_messages = titleValidation(state.title.value);
      state.content.error_messages = contentValidation(state.content.value);
      // state.tos.error_messages = tosValidation(state.tos.value);
      state.writer.error_messages = writerValidation(state.writer.value);
      state.attachments.error_messages = attachmentsValidation(state.attachments.value);
      // 一度入力されたものとしてis_dirtyをtrueに
      state.title.is_dirty = true;
      state.content.is_dirty = true;
      // state.tos.is_dirty = true;
      state.writer.is_dirty = true;
      state.attachments.is_dirty = true;
    }
  },
  getters: {
    isValid (state) {
      return (
        !state.title.error_messages.length &&
        !state.content.error_messages.length &&
        !state.tos.error_messages.length &&
        !state.writer.error_messages.length &&
        !state.attachments.error_messages.length &&
        !state.send_at.error_messages.length
      );
    },
    isValidAndDirty (state, getters) {
      return (
        getters.isValid &&
        state.title.is_dirty &&
        state.content.is_dirty
      );
    }
  },
  actions: {
    send (context) {
      // Validation
      context.commit('validateAll');
      if (!context.getters.isValid) {
        context.commit('message/addMessage', {
          level: "error",
          message: "不正なフィールドがあり、送信できませんでした。",
          appname: "mail/send"
        }, { root: true });
        return Promise.reject(new Error('form validation error'));
      }

      // Form construction
      let form = new FormData();
      form.append("title", context.state.title.value);
      form.append("content", context.state.content.value);
      context.state.tos.value.forEach(obj => {
        form.append("to", obj.year);
      });
      form.append("writer", context.state.writer.value.id);
      context.state.attachments.value.forEach(file => {
        form.append("attachments", file);
      });
      
      // POST
      return axios.post(
          '/api/board/send/send/', form, {onUploadProgress: e => console.log(e) }
        ).then(res => {
          console.log(res);
          context.commit('message/addMessage', {
            level: "info",
            message: "送信されました。",
            appname: "mail/send"
          }, { root: true });
          return res;
        });
    }
  }
};