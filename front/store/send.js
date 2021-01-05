import * as validations from "../send-form-validations";

export default {
  namespaced: true,
  state: {
    title: "",
    content: "",
    to: [],
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
      // const validation = validations.titleValidation(payload);
      // if (validation.length === 0) {
      //   console.log('validated!')
        state.title = payload;
      // }
      // return validation;
    }
  },
  getters: {
    validateTitle(state) {
      const result = validations.titleValidation(state.title);
      console.log(result)
      return result
    }
  }
}