## How to render segname name into the frontend of Ticket System

- 目標：現在 Ticket System 的功能中都是透過 segment_log_id 去 trigger 以獲取 Row Chat History, Call Summarized Content，不過對於 Client 的使用上，用 Segment Name 去查詢會更具意義，並且也能讓使用者能理解 Segment 真正代表的意義，所以這邊要手刻一個 Convert 以讓我們能透過 Segment Name 去查詢相關的資料。
- 技術難點：因為目前拿取 Segment id 以及 Segment Name 的方式是透過 Segment API，所以這邊要透過 Segment API 去取得 Segment id 以及 Segment Name 的對應關係，不過現有 Gradio 並沒有提供這樣的功能，所以這邊要自己實作一個 Convertor 以達到這樣的需求。

因此會需要有個 Map 的結構來存放 Segment Name 與 Segment id 的對應關係，並且要更改現有設計，要讓 Segment Name 變成現在的 Trigger 以獲取 Row Chat History, Call Summarized Content 的方式。因此我們還需要定義一個 Convertor 以達到這樣的需求。

### Cases:

1. 點擊 refresh Button 以獲取 Segment Name 與 Segment id 的對應關係，並且介面上的 Dropdown 會顯示 Segment Name 的列表選項。
2. 新增一個區段 (可透過 gradio.Code) 去儲存可被用來查詢 Segment Name、Segment id 的對應關係。(需要把這個對應關係給 invisible)
3. 更改現有的 Trigger 把原先透過 Segment id 去查詢的方式改成透過 Segment Name 去查詢，並且也要把 Segment id, Segment Name 的對應關係也要當成 Trigger 的一部分。
4. 定義一個 Convertor 以達到透過 Segment Name 去查詢 Segment id 的需求。


所帶來結果：
1. 我們不需要再把 Segment ID 的 Dropdown 顯示在介面上，而是透過 Segment Name 去查詢 Segment id。
2. 可能會造成前端載入時間增加，因為我們要再調查。

需要更改的 cases:
- `segment/get_segments()`
- `summarized_content/get_summarized_ticket_content()`
- `submissions/send_summarized_ticket_content()`
- `chat_history/get_row_chat_history()`



