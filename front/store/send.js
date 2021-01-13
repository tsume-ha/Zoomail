import * as validations from "../send-form-validations";

export default {
  namespaced: true,
  state: {
    title: "",
    content: "",
    to: null,
    writer_id: null,
    writer_year: null,
    attachments: [],
    send_at: null,
    writer_choices: [
      {
        year: 2020,
        members: [
          {name: "京大太郎", furigana: "きょうだいたろう"},
          {name: "京大次郎", furigana: "きょうだいじろう"},
        ]
      },
    ]
  },
  mutations: {
    titleInput (state, payload) {
        state.title = payload;
    },
    fromInput(state, payload) {
      state.writer_id = payload;
    },
    toInput(state, payload) {
      state.to = payload;
    },
    contentInput(state, payload) {
      state.content = payload;
    },
    fileInput(state, payload) {
      for (let i  = 0; i < payload.length; i++) {
        this._vm.$set(state.attachments, i, payload[i])
      }
    }
  },
  getters: {
    validateTitle(state) {
      return validations.titleValidation(state.title);
    },
    validateContent(state) {
      return validations.contentValidation(state.content);
    },
    validateAttachments(state) {
      return validations.attachmentsValidation(state.attachments);
    }
  },
}