const CryptoJS = require("crypto-js");
const JSEncrypt = require("./yencrypt.js"); // 引入模块

// var navigator = {
//     appName: "Netscape",
// };

/////////////////////////////
function get_cb() {
    var pool = {};
    for (var t; (t = Math.random().toString(32).replace("0.", "")) in pool;)
        ;
    return pool[t] = {
        ts: 1 / 0
    },
        t
}

console.log("cb:", get_cb());
/////////////////////////////
st = {}

function data_encrypt(data) {
    t = JSON.stringify(data);
    var e = st.getRandomStr(16)
        , n = st.getRandomStr(16);

//    e = "o03vd7gwqul4dvbk";
//    n = "vb0kvi238a2w0972";

    return {
        i: CryptoJS.AES.encrypt(t, CryptoJS.enc.Latin1.parse(e), {
            iv: CryptoJS.enc.Latin1.parse(n),
        }).toString(),
        k: rsaEncrypt(e + n)
    }
}

st.getRandomStr = function (t) {
    for (var e = ""; e.length < t;)
        e += Math.random().toString(36).substr(2);
    return e = e.slice(0, t)
}

st.getBrowserInfo = function () {
    var t = []
        , e = {
        userAgent: navigator.userAgent,
        language: navigator.language,
        hardware_concurrency: navigator.hardwareConcurrency,
        resolution: [window.screen.width, window.screen.height],
        navigator_platform: navigator.platform
    };
    for (var n in e)
        e.hasOwnProperty(n) && t.push({
            key: n,
            value: e[n]
        });
    return t
}

function rsaEncrypt(t) {
    var RSA_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDnOWe/gs033L/2/xR3oi6SLAMPBY5VledUqqH6dbCNOdrGX4xW+1x6NUfvmwpHRBA2C7xWDDvOIldTl0rMtERTDy9homrVqEcW6/TY+dSVFL3e2Yg2sVaehHv7FhmATkgfC2FcXt8Wvm99QpKRSrGKpcFYJwOj2F8hJh+rTG0IPQIDAQAB-----END PUBLIC KEY-----";
    var e = new JSEncrypt.JSEncrypt();
    return e.setPublicKey(RSA_PUBLIC_KEY),
        e.encrypt(t)
}

data = {
    "browserInfo": [{
        "key": "userAgent",
        "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }, {"key": "language", "value": "zh-CN"}, {"key": "hardware_concurrency", "value": 4}, {
        "key": "resolution",
        "value": [1920, 1080]
    }, {"key": "navigator_platform", "value": "Win32"}],
    "mobile": "",
    "nativeInfo": {},
    "options": {"sdk": "https://www.yunpian.com/static/official/js/libs/riddler-sdk-0.2.2.js"},
    "fp": "c723c98d68b3641085c35891e243e063",
    "address": "https://www.yunpian.com",
    "yp_riddler_id": "1ba912a6-0a30-488f-80fb-9a41735a2b41"
};
console.info(data_encrypt(data));
//////////////轨迹生成//////////////////
function RandomNum(min, max) {

    return Math.floor(Math.random()*(max-min)) + min + 1

}

function RandomChoice(arr) {

    return arr[Math.floor(Math.random()*arr.length)]

}

function get_trace(distance){
    // 返回值 一个表示小于或等于指定数字的最大整数的数字。
    distance = Math.floor(distance);

    var trace = [];

    var sy = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0];

    var st = [15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17,
        18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 14, 16, 17, 18, 16, 17, 18, 19, 20, 17];

    //items[Math.floor(Math.random()*items.length)]

    if (distance < 95) {
        var sx = [1, 2, 1, 2, 1, 2, 1, 1, 2, 1];
    }else{
        var sx = [1, 2, 1, 2, 1, 2, 2, 2, 3, 4];
    }

    var zt = RandomNum(20, 200);

//    var baseX = RandomNum(810, 860),
    var baseX = RandomNum(1110, 1130),

        baseY = RandomNum(1190, 1220),

        zx = 0,

        zy = 0;

    var random_x = RandomNum(9, 14);

    trace.push(["" + baseX, "" + baseY, zt]);

    console.info(trace)

    var n = 0, x = 0, y = 0, t = 0;
    // 前五次都移动1px
    while (true){
        n += 1;
        if (n < 5){
            x = 1;
        }else{
            x = RandomChoice(sx)
        }

        if (distance > 125 && random_x === n){
            x = RandomNum(14, 18)
        }
        y = RandomChoice(sy);
        t = RandomChoice(st);
        zx += x;

        zy += y;

        zt += t;

        trace.push(["" + (zx + baseX), "" + (zy + baseY), zt]);
        if (distance - zx < 6){
            break;
        }
    }

    var value = distance - zx;
    for (var i = 0; i < value; i++){
        t = RandomChoice(st);

        if (value === i + 1){
            t = RandomNum(42, 56)
        }
        if (value === i + 2){
            t = RandomNum(32, 38)
        }
        if (value === i + 3){
            t = RandomNum(30, 36)
        }
        x = 1;
        zx += x;

        zt += t;

        trace.push([""+(zx + baseX), ""+ (zy + baseY), zt]);
    }

    t = RandomNum(100, 200);

    zt += t;

    trace.push([""+(zx + baseX), ""+ (zy + baseY), zt]);

	return trace;
}

