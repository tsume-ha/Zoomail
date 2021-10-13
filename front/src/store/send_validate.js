export function titleValidation(text) {
  let result = [];
  if (text.length < 1) {
    result.push("タイトルを入力してください")
  }
  if (text.length > 200) {
    result.push("タイトルが長すぎます")
  }
  return result;
}

export function contentValidation(content) {
  let result = [];
  if (content.length < 1) {
    result.push("本文を入力してください")
  }
  return result;
}

export function writerValidation(writer_id) {
  let result = [];
  if (!writer_id) {
    result.push("差出人を指定してください")
  }
  return result;
}

export function tosValidation(to_list) {
  let result = [];
  if (to_list === null) {
    return ["宛先を指定してください"];
  }
  if (!to_list || to_list.length === 0) {
    result.push("宛先を指定してください")
  }
  return result;
}

export function attachmentsValidation(files) {
  let result = [];
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
      result.push("ファイルサイズが上限(10MB)を超えています：" + file.name)
    }
    totalFileSize += file.size;
  }
  if (totalFileSize > 20*1024*1024) {
    result.push("合計のファイルサイズが上限(20MB)を超えています")
  }
  // 1ファイルmax 10*1000*1000
  // ファイル合計 20MBまで
  return result;
}

// export function send_atValidation(send_at) {
//   return []
// }
