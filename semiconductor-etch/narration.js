// 由 generate_audio.py 產生，請改 data/narration.json 後重新執行
window.ETCH_NARRATION = {
  "voice": "zh-TW-HsiaoChenNeural",
  "scenes": [
    {
      "title": "開場 Two Ways to Etch",
      "dur": 8.0,
      "subs": [
        {
          "start": 0.0,
          "end": 8.0,
          "text": "同樣是把矽 Si 吃掉，蝕刻機有兩種吃法：用電場推著吃，和純靠化學慢慢吃。",
          "audio": "audio/s1-1.mp3",
          "duration": 6.816
        }
      ]
    },
    {
      "title": "進氣與點燃電漿 Plasma Ignition",
      "dur": 17.33,
      "subs": [
        {
          "start": 0.0,
          "end": 5.67,
          "text": "六氟化硫 SF₆ 氣體從上方的噴氣頭 showerhead，進入低壓腔體。",
          "audio": "audio/s2-1.mp3",
          "duration": 4.464
        },
        {
          "start": 5.67,
          "end": 11.33,
          "text": "射頻 RF 電場加速電子 e⁻，電子撞上分子，把它拆開。",
          "audio": "audio/s2-2.mp3",
          "duration": 4.656
        },
        {
          "start": 11.33,
          "end": 17.33,
          "text": "拆出兩種主角：帶正電的離子 ion，和不帶電的氟自由基 radical。",
          "audio": "audio/s2-3.mp3",
          "duration": 4.968
        }
      ]
    },
    {
      "title": "偏壓與鞘層 Bias & Sheath",
      "dur": 18.0,
      "subs": [
        {
          "start": 0.0,
          "end": 5.5,
          "text": "在晶圓底座 chuck 加上射頻偏壓 RF bias，晶圓表面累積負電。",
          "audio": "audio/s3-1.mp3",
          "duration": 4.464
        },
        {
          "start": 5.5,
          "end": 11.0,
          "text": "晶圓上方形成一層鞘層 sheath，裡面是強大的垂直電場。",
          "audio": "audio/s3-2.mp3",
          "duration": 4.776
        },
        {
          "start": 11.0,
          "end": 18.0,
          "text": "正離子 ion 被拉直、垂直往下加速；自由基 radical 不帶電，照樣到處亂飄。",
          "audio": "audio/s3-3.mp3",
          "duration": 5.856
        }
      ]
    },
    {
      "title": "表面反應 Surface Reaction",
      "dur": 22.25,
      "subs": [
        {
          "start": 0.0,
          "end": 5.5,
          "text": "離子撞擊溝槽底部 trench bottom，把矽原子之間的鍵結 bond 打鬆。",
          "audio": "audio/s4-1.mp3",
          "duration": 4.368
        },
        {
          "start": 5.5,
          "end": 10.5,
          "text": "氟自由基 F* 趁機抓住矽，生成四氟化矽 SiF₄ 氣體。",
          "audio": "audio/s4-2.mp3",
          "duration": 4.224
        },
        {
          "start": 10.5,
          "end": 15.25,
          "text": "四氟化矽 SiF₄ 飄離表面，被抽氣泵 pump 抽走。",
          "audio": "audio/s4-3.mp3",
          "duration": 3.72
        },
        {
          "start": 15.25,
          "end": 22.25,
          "text": "側壁 sidewall 沒被離子打到，幾乎不動，溝槽又深又直，這叫非等向性蝕刻 anisotropic etch。",
          "audio": "audio/s4-4.mp3",
          "duration": 6.168
        }
      ]
    },
    {
      "title": "遠端電漿 Remote Plasma",
      "dur": 16.5,
      "subs": [
        {
          "start": 0.0,
          "end": 5.5,
          "text": "化學蝕刻常把電漿放在晶圓上游，叫做遠端電漿 remote plasma。",
          "audio": "audio/s5-1.mp3",
          "duration": 4.728
        },
        {
          "start": 5.5,
          "end": 11.0,
          "text": "往下流的途中，離子和電子重新結合 recombination、消失。",
          "audio": "audio/s5-2.mp3",
          "duration": 4.584
        },
        {
          "start": 11.0,
          "end": 16.5,
          "text": "抵達晶圓的只剩氟自由基 F*，而且沒有偏壓電場 no bias。",
          "audio": "audio/s5-3.mp3",
          "duration": 4.368
        }
      ]
    },
    {
      "title": "等向性反應 Isotropic Reaction",
      "dur": 21.5,
      "subs": [
        {
          "start": 0.0,
          "end": 5.0,
          "text": "自由基 radical 沒有方向，從四面八方碰到矽表面。",
          "audio": "audio/s6-1.mp3",
          "duration": 4.128
        },
        {
          "start": 5.0,
          "end": 10.5,
          "text": "反應還是一樣：矽加四個氟 Si + 4F，變成四氟化矽 SiF₄ 飄走。",
          "audio": "audio/s6-2.mp3",
          "duration": 4.8
        },
        {
          "start": 10.5,
          "end": 17.0,
          "text": "往下吃多深，往旁邊就吃多寬，鑽到光阻 photoresist 底下形成底切 undercut。",
          "audio": "audio/s6-3.mp3",
          "duration": 5.376
        },
        {
          "start": 17.0,
          "end": 21.5,
          "text": "這就是等向性蝕刻 isotropic etch。",
          "audio": "audio/s6-4.mp3",
          "duration": 2.352
        }
      ]
    },
    {
      "title": "對照與總結 Summary",
      "dur": 13.0,
      "subs": [
        {
          "start": 0.0,
          "end": 6.0,
          "text": "偏壓蝕刻 bias etch 靠離子決定方向，適合細線寬和深溝槽。",
          "audio": "audio/s7-1.mp3",
          "duration": 4.8
        },
        {
          "start": 6.0,
          "end": 13.0,
          "text": "化學蝕刻 chemical etch 溫和、損傷小、選擇比 selectivity 高，適合整片移除或掏空結構。",
          "audio": "audio/s7-2.mp3",
          "duration": 6.168
        }
      ]
    }
  ]
};
