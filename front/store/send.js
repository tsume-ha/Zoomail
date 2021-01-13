import * as validations from "../send-form-validations";

export default {
  namespaced: true,
  state: {
    title: "",
    content: "",
    to: null,
    writer_id: 1,
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
    ],
    validate_clicked: false,
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
      if (!payload.length) {
        state.attachments = [];
        return;
      }
      for (let i  = 0; i < payload.length; i++) {
        this._vm.$set(state.attachments, i, payload[i])
      }
    },
    validate(state) {
      state.validate_clicked = true;
    }
  },
  getters: {
    isAllValid(state, getters) {
      return (!getters.validateTitle.length
           && !getters.validateContent.length
           && !getters.validateWriter.length
           && !getters.validateTo.length
           && !getters.validateAttachments.length);
    },
    validateTitle(state) {
      return validations.titleValidation(state.title);
    },
    validateContent(state) {
      return validations.contentValidation(state.content);
    },
    validateWriter(state) {
      return validations.writerValidation(state.writer_id);
    },
    validateTo(state) {
      return validations.toValidation(state.to);
    },
    validateAttachments(state) {
      return validations.attachmentsValidation(state.attachments);
    }
  },
}