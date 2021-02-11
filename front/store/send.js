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
    progress: 0,
    complete: false,
    complete_num: null,
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
      state.attachments = [];
      if (!payload.length) {
        return;
      }
      for (let i  = 0; i < payload.length; i++) {
        this._vm.$set(state.attachments, i, payload[i])
      }
    },
    validate(state) {
      state.validate_clicked = true;
    },
    onUpload(state, payload) {
      state.progress = Math.floor((payload.loaded * 100) / payload.total);
    },
    onComplete(state, payload) {
      state.complete = true;
      state.complete_num = payload.total_send_num;
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
      axios.get("/api/board/send/togroups/")
        .then(res => {
          context.commit('setToGroups', res.data.togropus)
        })
    },
    getFROMs(context) {
      axios.get("/api/board/send/froms/")
        .then(res => {
          // console.log(res.data)
          context.commit('setWriterFroms', res.data)
        })
    },
    send (context) {
      if (!context.getters.isAllValid) {
        console.log('validation error')
      }
      console.log("validaion OK")
      let data = new FormData();
      data.append("title", context.state.title)
      data.append("writer", context.state.writer_id)
      for (let i = 0; i < context.state.to.length; i++) {
        data.append("to", context.state.to[i])
      }
      data.append("content", context.state.content)
      for (let i = 0; i < context.state.attachments.length; i++) {
        data.append("attachments", context.state.attachments[i])
      }
      // upload progress
      axios.post("/api/board/send/send/", data, {onUploadProgress: e => context.commit('onUpload', e) })
      .then(res => {
        // console.log(res)
        context.commit('onComplete', res.data)
      })
    }
  }
}