import axios from 'axios';
import * as validations from "../send-form-validations";

export default {
  namespaced: true,
  state: {
    title: "",
    content: "",
    to: null,
    writer_id: 1,
    writer_year: null,
    writer_years: [],
    attachments: [],
    send_at: null,
    to_groups: [],
    writer_choices: [
      {
        year: 0,
        list: [
          {name: "読み込み中", id: "0"},
        ]
      },
    ],
    validate_clicked: false,
  },
  mutations: {
    setToGroups (state, payload) {
      state.to_groups = payload;
    },
    setWriterFroms (state, payload) {
      state.writer_choices = payload.members;
      state.writer_years = payload.years;
      state.writer_id = payload.user.id;
      state.writer_year = payload.user.year;
    },
    setWriterYear(state, payload) {
      state.writer_year = payload;
    },
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
  actions: {
    // 呼ぶのはsend-input.vueから
    getToGroups (context) {
      axios.get("/read/api/send/togroups/")
        .then(res => {
          context.commit('setToGroups', res.data.togropus)
        })
    },
    getFROMs(context) {
      axios.get("/read/api/send/froms/")
        .then(res => {
          console.log(res.data)
          context.commit('setWriterFroms', res.data)
        })
    }
  }
}