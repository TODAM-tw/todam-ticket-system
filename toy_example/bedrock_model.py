import json
import os

import requests
from dotenv import find_dotenv, load_dotenv
from requests.models import Response


row_chat_history = [
    (None, '我們的虛擬機器在 Azure 上運行，配置為 Linux，VM 世代為 V1，架構是 x64，休眠已禁用，公共 IP 地址為 20.253.222.207（網絡接口為 adam-linux580），私有 IP 地址為 10.0.3.4，虛擬網絡/子網絡為 adam-vnet/adam-private-1，規模為標準 B2s（2 vCPUs、4 GiB RAM），磁盤為 adam-disk-linux（主機加密已禁用，未啟用 Azure 磁盤加密），安全類型為標準。我們最近遇到了 504 錯誤，您能幫忙分析問題所在嗎？'),
    (None, """'IMAGE_URL' = 'https://todam-bucket-478977890696-us-east-1.s3.amazonaws.com/jpg/test_azure.png' The image shows the configuration details of a virtual machine (VM) running on a cloud platform, likely Microsoft Azure. Here are the key details: - Operating System: Linux - VM Generation: V1: - VM Architecture: x64: - Hibernation: Disabled: - Public IP Address: 20.253.222.207 (Network interface adam-linux580): - Private IP Address: 10.0.3.4: - Virtual Network/Subnet: adam-vnet/adam-private-- Size: Standard B2s (2 vCPUs, 4 GiB RAM): - Disk: adam-disk-linux (Encryption at host disabled, Azure disk encryption not enabled): - Security Type: Standard, The VM does not appear to be part of any host group, availability set, or scale set. The source image details, disk controller type, and capacity reservation group are not specified. The overall configuration seems to be for a basic Linux VM with standard networking and disk settings on Azure."""), 
    ('很抱歉聽到您遇到 504 錯誤。這可能與您的虛擬機器的性能或連接有關。請確保您的虛擬機器的資源使用合理並且未受到任何限制，特別是在高負載時。同時，請檢查您的網絡設置，確保連接到 Azure 的網絡穩定且無阻礙。您可以查看 Azure 的監控工具來檢視虛擬機器的性能指標和網絡狀態。如果問題仍然存在，您可能需要進一步的調查或聯繫 Azure 技術支援以獲得協助。您有其他需要了解的問題嗎？', None), 
    (None, """感謝您的回答。我們將按照您提供的建議來檢查和解決問題。另外，我們還有一個關於虛擬機器性能調整的問題。我們的 VM 在高負載時表現不佳，您能提供一些性能優化的建議嗎？"""), 
    ("""當虛擬機器在高負載時表現不佳時，您可以考慮以下幾點來進行性能優化：首先，檢查虛擬機器的資源配置，可能需要增加 vCPU 和 RAM 來應對更高的負載；其次，優化應用程序和服務，確保它們能夠有效地利用虛擬機器的資源；另外，可以考慮使用 Azure 的負載均衡器來平衡負載，將流量分配到多個虛擬機器上。最後，監控系統性能並進行持續的優化和調整以確保最佳效能。這些都是可以幫助提升虛擬機器性能的建議，您可以根據實際情況進行調整和實施。您有其他需要幫助的問題嗎？""", None), 
]

message_types = "['text', 'image', 'text', 'text', 'text']"

# 去掉字串的首尾方括號和空白
message_types = message_types.strip("[]").strip()

# 將字串分割為列表
message_types_list = message_types.split(", ")

# 去掉每個元素的引號
message_types_list = [element.strip("'") for element in message_types_list]

result = []
current_user_type = None

for i in range(len(row_chat_history)):
    tam_message, client_message = row_chat_history[i]
    message_type = message_types_list[i]
    if tam_message:
        current_user_type = "TAM"
        content = tam_message
    elif client_message:
        current_user_type = "Client"
        content = client_message
    else:
        # Skip recording messages
        continue
    result.append({
        "message_type": message_type, # "text" or "image
        "user_type": current_user_type,
        "content": content
    })

payload = json.dumps({"input": result})     # 要再包一層 input

_ = load_dotenv(find_dotenv())
bedrock_api_url: str = os.environ['BEDROCK_API_URL']

headers = {
    'Content-Type': 'application/json'
}

response: Response = requests.request(
    "POST", 
    bedrock_api_url,
    headers=headers, 
    data=payload
)

data = []

if response.status_code == 200:
    data: dict = json.loads(response.text)

print(data)
print(type(data))


print(data["statusCode"])
print(data["body"])

body = json.loads(data["body"])

print(body[0]["id"])
print(body[0]["content"])
print(type(body[0]["content"]))
print(body[0]["content"][0])
print(body[0]["content"][0]["text"])
print(type(body[0]["content"][0]["text"]))


