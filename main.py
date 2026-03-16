from curl_cffi import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time
import random

def send_vote(vote_id):
    try:
        # إضافة تأخير عشوائي للتمويه عشان السيرفر ميحسش إننا سكريبت
        sleep_time = random.uniform(1.0, 3.5)
        time.sleep(sleep_time)
        
        session = requests.Session(impersonate="chrome")
        
        url_get = "https://www.radionrjfm.com/vote/20"
        response = session.get(url_get)
        
        # لو رجع 429 من أولها، نخرج بكرامتنا
        if response.status_code == 429:
            print(f"[-] التصويت {vote_id}: السيرفر عمل بلوك مؤقت (429)")
            return 0
            
        soup = BeautifulSoup(response.text, "html.parser")
        token_element = soup.find("input", {"name": "_token"})
        
        if not token_element:
            print(f"[-] التصويت {vote_id}: فشل في العثور على التوكن")
            return 0
            
        csrf_token = token_element["value"]
        
        url_post = "https://www.radionrjfm.com/pvote"
        session.get(url_post)
        
        headers = {
            "authority": "www.radionrjfm.com",
            "method": "POST",
            "path": "/pvote",
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.radionrjfm.com",
            "referer": "https://www.radionrjfm.com/vote/20",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        
        payload = {
            "gidvnrj": "20",
            "sex": "1",
            "age": "3",
            "_token": csrf_token,
            "answers[435]": "1"
        }
        
        res2 = session.post(url_post, headers=headers, data=payload, allow_redirects=False)
        
        if res2.status_code == 302:
            print(f"[+] التصويت {vote_id} نجح! ✅")
            return 1
        else:
            print(f"[-] التصويت {vote_id} فشل! (Status: {res2.status_code}) ❌")
            return 0
            
    except Exception as e:
        print(f"[!] خطأ في التصويت {vote_id}: Timeout أو مشكلة اتصال")
        return 0

if __name__ == "__main__":
  while True:
    start_time = time.time()
    print("🚀 جاري بدء 100 تصويت (النسخة البطيئة للتمويه)...")
    
    # قللنا العدد لـ 5 بس في نفس الوقت عشان نتفادى الـ 429
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(send_vote, range(1, 101)))
        
    end_time = time.time()
    
    success_count = sum(results)
    print("\n" + "="*30)
    print(f"📊 التقرير النهائي:")
    print(f"✅ التصويتات الناجحة: {success_count} من 100")
    print(f"⏱️ الوقت الإجمالي: {end_time - start_time:.2f} ثانية")
    print("="*30)
