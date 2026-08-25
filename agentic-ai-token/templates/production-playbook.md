# Token-Efficient Agent Production Playbook

## 1. 任務與 SLO

- 任務類型與真實流量比例：
- Must-have 成功門檻：
- 每成功任務成本目標：
- P50／P95 延遲目標：
- 不可降級的安全與授權規則：

## 2. Budget Envelope

| 階段 | Token | 工具呼叫 | 時間 | 重試 | 到頂行為 |
|---|---:|---:|---:|---:|---|
| 理解 | | | | | |
| 檢索 | | | | | |
| 執行 | | | | | |
| 驗證 | | | | | |
| 輸出 | | | | | |

## 3. 路由與控制

- Context Manifest：
- Tool Bundle：
- Model／Reasoning Route：
- Multi-agent 啟用門檻：
- Prompt Cache 前綴版本：
- Loop Guard／Retry Budget：

## 4. 降級順序

1. 移除可選詳細度與重複格式
2. 縮小非必要檢索與獨立檢查
3. 使用已通過該任務 Eval 的較低成本路徑
4. 保存 Checkpoint，回傳 partial 與必要缺口

不得降級：安全、授權、必要證據、核心驗證與資料治理。

## 5. 告警與事故

- Context growth：
- No-progress／重複工具：
- Retry／Escalation／Fan-out：
- Cache miss：
- 單任務與 P95 成本：
- 事故 Trace、止損、Root cause、回歸案例與擁有者：

## 6. 30 天計畫

- Week 1：量測與基準
- Week 2：Prompt／Context／Tool reduction
- Week 3：Loop／Routing／Multi-agent／Cache
- Week 4：Dashboard／Alert／Degrade／Regression
