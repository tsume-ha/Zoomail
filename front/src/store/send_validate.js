export function titleValidation(text) {
  const result = [];
  if (text.length < 1) {
    result.push("タイトルを入力してください");
  }
  if (text.length > 200) {
    result.push("タイトルが長すぎます");
  }
  return result;
}

export function contentValidation(content) {
  const result = [];
  if (content.length < 1) {
    result.push("本文を入力してください");
  }
  const mailAddressReg = /[\w\-._]+@[\w\-._]+\.[A-Za-z]+/;
  const urlReg = /https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]]+/;
  if (content.search(mailAddressReg) > 0) {
    const index = content.search(mailAddressReg);
    if (content[index - 1] !== "\n" && content[index - 1] !== " ") {
      result.push("メールアドレスの前後には改行または半角スペースを入れてください");
    }
  }
  if (content.search(urlReg) > 0) {
    const index = content.search(urlReg);
    if (content[index - 1] !== "\n" && content[index - 1] !== " ") {
      result.push("URLの前後には半角スペースを入れてください");
    }
  }
  return result;
}

export function writerValidation(writer) {
  const result = [];
  if (!writer) {
    result.push("差出人を指定してください");
  }
  return result;
}

export function tosValidation(to_list) {
  const result = [];
  if (to_list === null) {
    return ["宛先を指定してください"];
  }
  if (!to_list || to_list.length === 0) {
    result.push("宛先を指定してください");
  }
  return result;
}

export function attachmentsValidation(files) {
  const result = [];
  if (files.length === 0) {
    return [];
  }
  let totalFileSize = 0;
  for (const file of files) {
    if (!file.size) {
      result.push("ファイルが無効です");
    }
    if (file.size < 0) {
      result.push("ファイルが無効です(zero file size)");
    }
    if (file.size > 10*1000*1000) {// 1000*1000 < 1024*1024
      result.push(`ファイルサイズが上限(10MB)を超えています：${file.name}`);
    }
    totalFileSize += file.size;
  }
  if (totalFileSize > 20*1024*1024) {
    result.push("合計のファイルサイズが上限(20MB)を超えています");
  }
  // 1ファイルmax 10*1000*1000
  // ファイル合計 20MBまで
  return result;
}

// export function send_atValidation(send_at) {
//   return []
// }
