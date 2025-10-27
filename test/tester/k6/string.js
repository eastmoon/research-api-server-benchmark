// Import libraries

// 匯入 http 模組，來自 k6/http
import http from 'k6/http'
// 匯入 check，sleep 函數工具，來自 k6
import { check, sleep } from 'k6'

// Declare variable
const server_addr = "ENV_SERVER" in __ENV ? __ENV.ENV_SERVER : "server"

// Declare function
function randomInteger(min, max) {
    min = Math.ceil(min); // Ensure min is a whole number
    max = Math.floor(max); // Ensure max is a whole number
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomString(length) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-=+-*{}[]';
    const charactersLength = characters.length;
    let result = ""
    for (let i = 0; i < length; i++) {
      result += characters.charAt(randomInteger(0, charactersLength - 1));
    }
    return result;
}

// 設定 k6 測試選項
export const options = {
    // 設定此測試項要執行的次數
    //iterations: 100,
    // 設定此測試要執行的時間
    duration: "1s",
    // 測試要開啟多少虛擬用戶 ( VUs、Virtual Users )
    vus: 5
};

// Declare function

// 1. 全域變數，每當 k6 運行時皆會執行，例如啟動 VUs、執行 setup 或 teardown 函數
console.log("Initial testcase global variable.");

// 2. 測試項啟動函數，在每個 UVs 執行前，僅執行一次的函數
export function setup() {
    console.log("Setup testcase");
    let topics=[];
    for( let i = 0 ; i < 100 ; i++ ) {
        let s = randomString(200);
        let x = randomString(1);
        let y = randomString(randomInteger(1, 2));
        let ans = s.replaceAll(x, y);
        const topic = { x: x, y: y, s: s, ans: ans };
        topics.push(topic);
    }
    return { topics: topics }
}
// 3. 每個虛擬用戶要反覆執行的函數
export default function (data) {
  const topic = data.topics[randomInteger(data.topics.length - 1, 0)];
  let res = http.get(`http://${server_addr}/api/str/${topic.s}/${topic.x}/${topic.y}`);
  check(res, {
    'success': (r) => r.status === 200,
    'body is not undefined': (r) => r.body !== undefined
  });
  let body = JSON.parse(res.body.replace(/'/g, '"'))
  check(body, {
    'answer correct': (b) => b.result === topic.ans
  });
}
// 4. 測試項完成所有執行次數後，僅執行一次的函數
export function teardown(data) {
    console.log("Teardown testcase");
}
// 5. 處理總結數據
export function handleSummary(data) {
  console.log('Preparing the end-of-test summary...');
  const { setup_data, ...summary } = data;
  return {
    '/tmp/summary.json': JSON.stringify(summary, null, 2), // The 'null, 2' arguments format the JSON for readability
  };
}
