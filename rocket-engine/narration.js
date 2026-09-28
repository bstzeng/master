// 由 generate_audio.py 產生，請改 data/narration.json 後重新執行
window.ROCKET_NARRATION = {
  "voice": "zh-TW-HsiaoChenNeural",
  "scenes": [
    {
      "title": "牛頓第三定律",
      "dur": 10,
      "subs": [
        {
          "start": 0,
          "end": 4.8,
          "text": "放開吹飽的氣球：空氣往後衝，氣球就往前飛。",
          "audio": "audio/s1-1.mp3",
          "duration": 4.176
        },
        {
          "start": 4.8,
          "end": 10,
          "text": "火箭也一樣：把氣體往後推，氣體就把火箭往前推。",
          "audio": "audio/s1-2.mp3",
          "duration": 4.344
        }
      ]
    },
    {
      "title": "推進劑供應",
      "dur": 12,
      "subs": [
        {
          "start": 0,
          "end": 4,
          "text": "太空沒有氧氣，火箭要自己帶燃料和氧化劑。",
          "audio": "audio/s2-1.mp3",
          "duration": 3.696
        },
        {
          "start": 4,
          "end": 8,
          "text": "渦輪泵把兩種推進劑加壓，高速送進噴注器。",
          "audio": "audio/s2-2.mp3",
          "duration": 3.672
        },
        {
          "start": 8,
          "end": 12,
          "text": "推進劑在燃燒室混合點火，再從噴嘴高速噴出。",
          "audio": "audio/s2-3.mp3",
          "duration": 3.384
        }
      ]
    },
    {
      "title": "燃燒室：壓力不平衡",
      "dur": 13,
      "subs": [
        {
          "start": 0,
          "end": 4,
          "text": "燃燒產生 3000°C 以上的高溫氣體，壓力急速上升。",
          "audio": "audio/s3-1.mp3",
          "duration": 3.528
        },
        {
          "start": 4,
          "end": 8,
          "text": "上下兩側的壓力互相抵消……",
          "audio": "audio/s3-2.mp3",
          "duration": 3.168
        },
        {
          "start": 8,
          "end": 13,
          "text": "但前壁被推、後方是開口 → 留下向前的淨力，這就是推力。",
          "audio": "audio/s3-3.mp3",
          "duration": 3.96
        }
      ]
    },
    {
      "title": "拉瓦爾噴嘴",
      "dur": 14,
      "subs": [
        {
          "start": 0,
          "end": 4.5,
          "text": "收斂段：通道變窄，次音速氣體被擠得越來越快。",
          "audio": "audio/s4-1.mp3",
          "duration": 3.768
        },
        {
          "start": 4.5,
          "end": 9,
          "text": "喉部：最窄的地方，氣流剛好達到音速 Mach 1。",
          "audio": "audio/s4-2.mp3",
          "duration": 3.384
        },
        {
          "start": 9,
          "end": 14,
          "text": "擴張段：超音速氣體膨脹，壓力與溫度下降，速度繼續上升。",
          "audio": "audio/s4-3.mp3",
          "duration": 4.728
        }
      ]
    },
    {
      "title": "推力公式",
      "dur": 12,
      "subs": [
        {
          "start": 0,
          "end": 4,
          "text": "推力來自兩部分：動量推力，加上壓力推力。",
          "audio": "audio/s5-1.mp3",
          "duration": 3.072
        },
        {
          "start": 4,
          "end": 8,
          "text": "例如每秒噴出 300 kg、速度 3000 m/s……",
          "audio": "audio/s5-2.mp3",
          "duration": 3.36
        },
        {
          "start": 8,
          "end": 12,
          "text": "推力約 900 kN，相當於舉起約 92 噸的重量。",
          "audio": "audio/s5-3.mp3",
          "duration": 3.456
        }
      ]
    },
    {
      "title": "升空",
      "dur": 14,
      "subs": [
        {
          "start": 0,
          "end": 3,
          "text": "點火倒數……",
          "audio": "audio/s6-1.mp3",
          "duration": 2.712
        },
        {
          "start": 3,
          "end": 8,
          "text": "推力大於重量，多出來的力讓火箭向上加速。",
          "audio": "audio/s6-2.mp3",
          "duration": 4.128
        },
        {
          "start": 8.5,
          "end": 14,
          "text": "把推進劑燒成高溫高壓氣體，再用噴嘴加速往後噴 —— 這就是火箭發動機。",
          "audio": "audio/s6-3.mp3",
          "duration": 4.56
        }
      ]
    }
  ]
};
