import moment from "@/utils/moment.js";

export const md = (date) => moment(date).format("M/DD (dd)");

export const dayColor = (date) => {
  const day = moment(date).format("d");
  if (day === "0") {
    return "text-danger";
  } else if (day === "6") {
    return "text-primary";
  } else {
    return "";
  }
};

export const room = (room) => {
  if (room === null) {
    return "例会教室は未登録";
  } else {
    return room;
  }
};

export const roomColor = (room) => {
  switch (room) {
    case "終日使用不可":
    case "使用不可":
      return "text-danger";
    case null:
      return "text-muted";
    case "(20時まで音出し不可)":
      return "text-success";
    default:
      return "";
  }
};