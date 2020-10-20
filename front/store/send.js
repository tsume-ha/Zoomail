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
}