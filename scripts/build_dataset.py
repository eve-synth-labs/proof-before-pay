"""Create reproducible illustrative bilingual synthetic training/evaluation messages.
Not drawn from real inboxes; outputs must not be marketed as real-world performance.
"""
from pathlib import Path
import json, random
ROOT=Path(__file__).resolve().parents[1]

SCAM_EN = [
"Congratulations, your university scholarship is approved. Pay a refundable verification deposit today to unlock the funds.",
"The recruiter selected you for a remote internship. Purchase the training package before we can issue a contract.",
"Campus relief fund: transfer a processing fee to this personal account within two hours or lose your award.",
"For your part-time job, send a clear photo of both sides of your ID and your banking password via chat.",
"Urgent: verify your education grant by sharing the one-time code you just received on your phone.",
"You were selected for a paid research assistant position. Send a security deposit to the coordinator's wallet.",
"This scholarship offer is confidential. Do not contact the university; send your personal details only to me.",
"Your student account will be frozen unless you click this link immediately and enter your password.",
"Guaranteed internship, no interview needed. Wire the document fee before midnight to reserve your seat.",
"A hiring manager needs you to receive money in your bank account and forward it to another account as a trial.",
"You have won a grant. To claim your prize, buy gift cards and send the codes to the staff member.",
"Our exchange program will reimburse you later; first pay the visa fee into my personal e-wallet.",
"Your tuition refund is pending. Enter your bank login and OTP at this unfamiliar site to release it.",
"The campus job group says we can double your money if you invest your scholarship cash this morning.",
"Immediate recruitment for students. The salary is huge and no experience is required, but send your passport scan first.",
"University financial aid selected you. Payment is delayed until you disclose the SMS authentication code.",
"You must keep our application secret and avoid the official careers office while we process your payment.",
"Your professor recommended you for a stipend. The only step is paying the activation charge via crypto.",
"Hello student, your internship is ready but your recruiter demands a bank card photo in a private message.",
"Scholarship approval notice: the offer expires tonight unless you transfer a reservation fee right now.",
"To complete your teaching assistant onboarding, install this unknown remote-control app and share your screen.",
"Official-looking campus message: send your student portal password to the coordinator by direct message.",
"This work-from-home role pays exceptionally well. We require a refundable equipment purchase through a private link.",
"Your scholarship money is blocked. Send a small unlock fee through a QR-code transfer to claim it.",
"Claim a student subsidy today by providing your bank PIN and the six-digit verification code.",
"A student job placement agent asks you to pay an interview booking charge to a personal wallet.",
"Don't verify this offer on the college website. We are handling the application outside official channels.",
"Your grant has already been awarded. Pay a handling cost now; there is no need to check with the school.",
"We require an upfront transfer before giving you the employer name or signed contract.",
"Work abroad opportunity: provide a photo of your national ID, full bank credentials and a deposit immediately.",
]
SAFE_EN = [
"The university careers office posted a summer internship on the official campus portal. Apply through that portal.",
"Reminder: the scholarship application deadline is Friday. Check requirements on the school's official site.",
"The library offers paid student assistant roles. Interviews are scheduled after application review, no fees requested.",
"Please submit your research assistant CV through the university recruitment system before the published deadline.",
"An alumni office notice explains how to review financial aid options using official university contact information.",
"Campus work-study recruitment is open; details and contact information are listed on the institution's website.",
"Your application receipt was issued. Log in using your own saved bookmark to view status updates.",
"The scholarship committee will announce the shortlisted applicants next week through the student portal.",
"A teaching assistant opening requires an application form and an interview, with no deposit or training fees.",
"Join our open information session on internships. See the official calendar for date and Zoom access details.",
"The financial aid office reminds students never to disclose one-time passwords or transfer funds to staff.",
"Recruitment for the lab internship closes next month. All documents go through the authenticated campus portal.",
"The bursary office explains tuition reimbursement policies and warns against unofficial payment requests.",
"This student notice asks you to review a PDF on the official university bulletin board, not an external login page.",
"A volunteer program offers certificates. Registration is free and coordinated by the named campus office.",
"Your campus account maintenance window is scheduled. No password reply or SMS code is required.",
"For the student job fair, employers will verify references during an interview and will never request a fee.",
"A funded fellowship announcement includes department details and a publicly listed administrative email address.",
"Please review the published scholarship eligibility criteria and ask the university office for any clarification.",
"The student union has an event; registration is on their published webpage and payment is not required.",
"Academic tutoring positions pay hourly wages. Applicants may ask questions through the university service desk.",
"This is a confirmation that the university received your application; nothing else is required at this time.",
"An official campus alert advises students to ignore messages asking for wire transfers or private ID scans.",
"Financial assistance is available for part-time students; submit supporting documents through the school portal.",
"Read the internship contract carefully and independently confirm the employer's address before accepting an offer.",
"The university department invites applicants to a free workshop about avoiding scholarship scams.",
"Career services published guidance on evaluating job offers and recognizing suspicious promises of high pay.",
"You may schedule a meeting with a program coordinator through the department's official contact page.",
"The public student research grant lists decision dates and eligibility rules, and requires no money to apply.",
"The internship supervisor asks you to choose an interview slot using the portal you already use for applications.",
]
SCAM_ZH = [
"恭喜獲得學生助學金，請今天先匯入保證金到私人帳戶，才能領取補助。",
"校園兼職錄取通知：請先購買培訓教材並轉帳給招募人員，否則取消資格。",
"急件！你的獎學金即將失效，兩小時內支付驗證費才能入帳。",
"工讀職缺需要驗證身分，請在LINE提供身分證正反面和網銀密碼。",
"學費退費已核准，請把手機收到的一次性驗證碼傳給客服。",
"保證錄取高薪實習，不必面試，只需先支付登記費就能開始工作。",
"獎學金審核是機密，請不要聯絡學校，只在私人群組提交個資。",
"系統偵測你的學生帳號異常，請立即點擊陌生連結並輸入密碼避免停權。",
"研究助理錄取後須先付押金，請轉入主管的個人電子錢包。",
"學校補助發放作業需要確認，請提供銀行帳密與簡訊認證碼。",
"海外實習名額很少，今晚前匯款保留費到指定個人帳戶。",
"我們可以幫你快速領到政府補助，先購買點數卡並拍下序號。",
"學生徵才群組宣布高薪遠端職缺，請先傳護照照片及完整金融卡資料。",
"獎金發放前請先繳解鎖費，完成 QR Code 私人轉帳即可領取。",
"若你聯繫學校查證，助學金將被取消，請只和我私下聯絡。",
"你已經錄取，先幫我們代收一筆款項再轉出，之後會支付工讀薪資。",
"快領取學雜費退款！請到這個新網址填寫網銀登入資料。",
"面試前請繳交作業處理費，直接匯給招募專員私人銀行帳號。",
"今晚截止的獎學金名單需要你傳送手機 OTP 驗證碼給管理員。",
"想拿到這個實習機會，請立刻安裝遠端控制程式讓我們操作電腦。",
"學校職涯中心推薦高薪工作，但必須先用加密貨幣支付開通費。",
"財務部通知你已中獎，請先支付稅金到私人帳戶才能兌現獎金。",
"急徵在校生打工，日薪超高免經驗，先提供身分證字號和提款卡密碼。",
"有人假冒系辦要求提供校務系統帳號密碼，並說不能向老師確認。",
"兼職錄取需要手續費，請在一小時內匯款給窗口以確認名額。",
"你的獎助金已核發但被凍結，請先付小額金流測試費解鎖。",
"請勿透過官方網站查證，直接把個資傳給這個LINE帳號即可領補助。",
"只要你先入金投資，就能讓這筆學生補助立即翻倍。",
"實習合約會在你支付保證金後才提供，請不要詢問公司名稱。",
"客服要你提供簡訊驗證碼、網銀密碼及帳戶餘額才能領回學費。",
]
SAFE_ZH = [
"學校職涯中心公布暑期實習職缺，請從校方正式徵才系統報名。",
"獎學金申請將於週五截止，資格與表單請至學校官方網站確認。",
"圖書館招募兼職學生助理，經審核後通知面試，不收取任何費用。",
"研究室開放工讀申請，請於公告期限內透過校內系統上傳履歷。",
"學務處提醒同學可向官方獎助學金承辦窗口詢問申請進度。",
"校園工讀職缺已公布於學校網站，包含工作時數、薪資與聯絡方式。",
"您的獎學金申請已收件，後續請至原本的學生資訊系統查詢。",
"獎學金審查結果預計下週公布，學校會在校務系統公告名單。",
"助教甄選需填表並參加面試，不要求繳交保證金或培訓費。",
"歡迎參加實習說明會，活動時間與參加方式可在學校行事曆查詢。",
"學校提醒同學不要把簡訊驗證碼或網銀密碼提供給任何人。",
"研究室招募暑期實習生，請由學校官方入口網站提交相關資料。",
"生活輔導組提供學費補助政策與詐騙防範資訊，請以正式公告為準。",
"本通知邀請你閱讀學校公告欄上的計畫說明，無須輸入陌生網站密碼。",
"志工服務計畫提供參與證明，由校方承辦且全程免費報名。",
"校務系統將於週末維護，不會要求你回覆密碼或一次性驗證碼。",
"校園就業博覽會開放預約面試，所有職缺不應以匯款作為錄取條件。",
"公開的研究獎助計畫附有承辦單位、資格限制以及校方聯絡資訊。",
"如對助學金資格有疑問，請直接透過學務處官網列出的方式詢問。",
"學生會邀請大家參與免費活動，報名頁面刊登在正式學生會網站。",
"校內課輔工讀提供時薪與排班資訊，應徵者可向系辦查證。",
"這是申請收件確認通知，目前不需要提交額外文件或執行付款。",
"學校資安公告提醒大家勿相信要求轉帳或傳送證件照片的私訊。",
"進修部學生可依公告申請相關助學措施，請由官方入口提交文件。",
"接受實習前請閱讀勞動契約，確認職務內容並獨立查詢雇主資料。",
"本校開設免費防詐宣導講座，歡迎同學向校內專責窗口報名。",
"職涯中心發布求職安全指南，教導同學辨識過高薪資與先付款陷阱。",
"可透過系所官網公布的電子郵件，與計畫承辦人員預約諮詢。",
"研究獎助金公告詳列申請資格、決選日期與免費申請程序。",
"實習主管請你使用原本的求職平台選擇面試時段，不需要先匯款。",
]

# Examples are original, illustrative and deliberately balanced; not real-world evidence.
INTRO_EN = ["", "Forwarded message: ", "A student received this notice: "]
INTRO_ZH = ["", "轉傳訊息：", "收到這則通知："]

def main():
    groups = []
    for label,lang,lines in ((1,'en',SCAM_EN),(0,'en',SAFE_EN),(1,'zh-TW',SCAM_ZH),(0,'zh-TW',SAFE_ZH)):
        for i,text in enumerate(lines):
            groups.append((label,lang,i,text))
    rng=random.Random(20261125)
    byclass={}
    for g in groups: byclass.setdefault((g[0],g[1]),[]).append(g)
    train=[]; holdout=[]
    for (_,lang),items in byclass.items():
        rng.shuffle(items)
        ntest=7
        for j,(label,language,idx,msg) in enumerate(items):
            to=holdout if j<ntest else train
            # Holdout base phrases are entirely unseen groups; no variants leak.
            variants=[msg] if to is holdout else [prefix+msg for prefix in (INTRO_ZH if lang=='zh-TW' else INTRO_EN)]
            for k,t in enumerate(variants):
                to.append({"text":t,"label":label,"language":language,"source":"original synthetic scenario","group":f"{label}-{lang}-{idx}","variant":k})
    rng.shuffle(train);rng.shuffle(holdout)
    for name,rows in [('train',train),('holdout',holdout)]:
        (ROOT/'data'/f'{name}.jsonl').write_text(''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in rows),encoding='utf8')
    print('train',len(train),'holdout',len(holdout),'(group-disjoint)')

if __name__=='__main__':main()
