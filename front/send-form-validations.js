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