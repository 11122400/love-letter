import streamlit as st
import time
from streamlit_extras.let_it_rain import rain
from PIL import Image
import os
import random
import base64
from io import BytesIO

st.set_page_config(
    page_title="💌 生日快乐",
    page_icon="💝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container { padding: 0 !important; max-width: 100% !important; }
    .stApp { background: linear-gradient(135deg, #fce4ec 0%, #fff0f5 30%, #f8e8ff 60%, #ffe0ec 100%) !important; }
    
    .letter-card {
        background: white; border-radius: 30px; padding: 45px 50px;
        box-shadow: 0 20px 60px rgba(233,30,99,0.15); max-width: 520px;
        margin: 0 auto; text-align: center; border: 2px solid rgba(233,30,99,0.15);
        position: relative; z-index: 10;
    }
    .letter-card::before {
        content: "💌"; position: absolute; top: -30px; left: 50%;
        transform: translateX(-50%); font-size: 40px; animation: bounce 2s infinite;
    }
    @keyframes bounce {
        0%,100% { transform: translateX(-50%) translateY(0); }
        50% { transform: translateX(-50%) translateY(-8px); }
    }
    .letter-title { font-size: 26px; color: #e91e63; margin-bottom: 25px; margin-top: 8px; font-weight: bold; }
    .letter-body { font-size: 15px; line-height: 2.2; color: #5d4037; text-align: left; white-space: pre-line; }
    .signature { text-align: right; font-style: italic; font-size: 15px; margin-top: 25px; color: #e91e63; }
    
    .decorative-divider { text-align: center; margin: 15px 0; font-size: 16px; letter-spacing: 6px; }
    
    .stButton > button {
        background: linear-gradient(135deg, #fce4ec, #f8bbd0) !important;
        border: 1px solid rgba(233,30,99,0.3) !important;
        color: #c2185b !important;
        font-style: italic !important;
        border-radius: 25px !important;
        font-size: 14px !important;
        padding: 10px 16px !important;
        cursor: pointer !important;
        transition: all 0.3s !important;
        box-shadow: 0 3px 10px rgba(233,30,99,0.15) !important;
        white-space: normal !important;
        line-height: 1.5 !important;
        min-height: auto !important;
        height: auto !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #f8bbd0, #f48fb1) !important;
        border-color: rgba(233,30,99,0.5) !important;
        box-shadow: 0 5px 18px rgba(233,30,99,0.25) !important;
        transform: translateY(-2px) !important;
        color: #880e4f !important;
    }
    
    .media-overlay {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background: rgba(0,0,0,0.85);
        z-index: 999;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        animation: overlayIn var(--dur) ease-in-out forwards;
        pointer-events: none;
    }
    
    .media-overlay img {
        max-width: 55vw; max-height: 55vh;
        border-radius: 20px; border: 4px solid white;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    
    .media-overlay video {
        max-width: 35vw; max-height: 35vh;
        border-radius: 20px; border: 4px solid white;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    
    .media-caption {
        color: #333; background: rgba(255,255,255,0.9);
        padding: 12px 24px; border-radius: 15px;
        font-size: 20px; margin-top: 15px; text-align: center; font-style: italic;
    }
    
    @keyframes overlayIn {
        0% { opacity: 0; }
        10% { opacity: 1; }
        85% { opacity: 1; }
        100% { opacity: 0; }
    }
</style>
""", unsafe_allow_html=True)

def safe_load_media(file_path, media_type="image"):
    try:
        if os.path.exists(file_path):
            if media_type == "image": return Image.open(file_path)
            elif media_type == "video":
                with open(file_path, 'rb') as f: return f.read()
    except: pass
    return None

def img_to_base64(img, fmt="JPEG"):
    try:
        b = BytesIO(); img.save(b, format=fmt)
        return base64.b64encode(b.getvalue()).decode()
    except: return None

@st.cache_data
def get_cached_photo(file):
    img = safe_load_media(file)
    if img:
        return img_to_base64(img)
    return None

@st.cache_data
def get_cached_video(file):
    vb = safe_load_media(file, "video")
    if vb:
        return base64.b64encode(vb).decode()
    return None

def check_password():
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False
    if not st.session_state.authenticated:
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            st.markdown("<h1 style='text-align:center;color:#e91e63;margin-top:100px;'>💕 生日快乐 💕</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center;color:#666;margin-bottom:30px;'>这是只属于你的秘密花园 💝</p>", unsafe_allow_html=True)
            pwd = st.text_input("请输入我们的纪念日（格式：MMDD）", type="password")
            if st.button("💌 打开情书", type="primary", use_container_width=True):
                if pwd == "0718": st.session_state.authenticated = True; st.rerun()
                else: st.error("密码不对哦～再想想我们的特别日子 💕")
        return False
    return True

def main():
    if not check_password(): return
    for k in ['envelope_opened','show_surprise','floating_media','float_start_time']:
        if k not in st.session_state: 
            st.session_state[k] = False if k != 'float_start_time' else 0
    
    if st.session_state.show_surprise:
        show_surprise(); return
    
    letter = """亲爱的宝贝：

今天是特别的一天，因为遇见了你，我的世界变得如此美好。

还记得我们第一次见面的时候吗？那一刻，我就知道你是特别的人。你的笑容像阳光一样温暖，你的眼睛像星星一样明亮。

和你在一起的每一天都是最好的礼物。我喜欢和你一起看电影，一起散步，一起分享生活的点点滴滴。

谢谢你出现在我的生命里，让我懂得了什么是爱。未来的路还很长，我希望一直牵着你的手走下去。

我爱你，不仅仅是在今天，而是每一天。"""

    if not st.session_state.envelope_opened: show_envelope()
    else: show_main(letter)

def show_envelope():
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<h1 style='text-align:center;font-size:120px;margin-top:80px;'>💌</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;color:#e91e63;'>给我最爱的你</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#666;font-size:18px;'>有一封信和美好的回忆在等你...</p>", unsafe_allow_html=True)
        if st.button("💝 轻轻滑动拆开信封", type="primary", use_container_width=True):
            st.session_state.envelope_opened = True
            st.balloons(); rain(emoji="💕", font_size=20, falling_speed=3, animation_length="infinite")
            time.sleep(0.5); st.rerun()

def show_main(letter):
    rain(emoji="💗", font_size=10, falling_speed=4, animation_length="infinite")
    
    photos = [
        {"poem": "那日人间风恰好\n辛得世间有你存", "file": "photo1.jpg", "label": "💕 第一次线下庆生", "key": "p1"},
        {"poem": "容颜恰是人间绝\n唯憾未能伴身侧", "file": "photo2.jpg", "label": "🌟 第一次拍写真", "key": "p2"},
        {"poem": "仗剑同迎千万难\n护卿岁岁无波澜", "file": "photo3.jpg", "label": "🎉 第一次一起拍写真", "key": "p3"},
        {"poem": "揽卿入怀\n愿卿无忧", "file": "photo4.jpg", "label": "💝 第一次揽你入怀", "key": "p4"},
    ]
    
    videos = [
        {"poem": "共踏山巅云尽处\n长相厮守伴余生", "file": "video1.mp4", "label": "💕 第一次爬雪山", "key": "v1"},
        {"poem": "每一个平凡的日子\n都因为你而特别", "file": "video2.mp4", "label": "🌟 你觉得可爱的", "key": "v2"},
    ]
    
    if st.session_state.floating_media:
        show_floating_media()
    
    st.markdown('<p class="decorative-divider">📸 💝 回忆按钮 💝 📸</p>', unsafe_allow_html=True)
    
    cols = st.columns(4)
    for i, p in enumerate(photos):
        with cols[i]:
            if st.button(p["poem"], key=p["key"], use_container_width=True):
                st.session_state.floating_media = {
                    "type": "image", "file": p["file"], "label": p["label"], 
                    "poem": p["poem"].replace("\n","，"), "duration": 3
                }
                st.session_state.float_start_time = time.time()
                st.rerun()
    
    cols2 = st.columns(2)
    for i, v in enumerate(videos):
        with cols2[i]:
            if st.button(v["poem"], key=v["key"], use_container_width=True):
                st.session_state.floating_media = {
                    "type": "video", "file": v["file"], "label": v["label"], 
                    "poem": v["poem"].replace("\n","，"), "duration": 3
                }
                st.session_state.float_start_time = time.time()
                st.rerun()
    
    st.markdown('<p class="decorative-divider">💕 ✨ 💕 ✨ 💕</p>', unsafe_allow_html=True)
    cl, cc, cr = st.columns([0.8, 2.4, 0.8])
    with cc:
        st.markdown(f'<div class="letter-card"><div class="letter-title">💌 写给你的信</div><div class="letter-body">{letter}</div><div class="signature">永远爱你的<br>你的男孩 💝<br>{time.strftime("%Y年%m月%d日")}</div></div>', unsafe_allow_html=True)
    
    st.markdown('<p class="decorative-divider">✨ 💝 ✨ 💝 ✨</p>', unsafe_allow_html=True)
    _, cb, _ = st.columns([1, 1, 1])
    with cb:
        if st.button("🎁 点我有惊喜 ✨", type="primary", use_container_width=True):
            st.session_state.show_surprise = True; st.rerun()
    
    with st.sidebar:
        if st.button("🔄 重新开始"):
            for k in ['envelope_opened','authenticated','show_surprise','floating_media','float_start_time']:
                if k in st.session_state: del st.session_state[k]
            st.rerun()

def show_floating_media():
    media = st.session_state.floating_media
    file = media.get("file", "")
    label = media.get("label", "")
    poem = media.get("poem", "")
    media_type = media.get("type", "image")
    duration = media.get("duration", 3)
    elapsed = time.time() - st.session_state.float_start_time
    
    if elapsed > duration:
        st.session_state.floating_media = None
        st.rerun()
    
    if media_type == "image":
        b64 = get_cached_photo(file)
        if b64:
            st.markdown(
                '<div class="media-overlay" style="--dur:' + str(duration) + 's;">'
                '<img src="data:image/jpeg;base64,' + b64 + '">'
                '<div class="media-caption"><b>' + label + '</b><br><span style="font-size:16px;">' + poem + '</span></div>'
                '</div>', unsafe_allow_html=True)
    
    elif media_type == "video":
        video_b64 = get_cached_video(file)
        if video_b64:
            st.markdown(
                '<div class="media-overlay" style="--dur:' + str(duration) + 's;">'
                '<video autoplay muted playsinline style="max-width:35vw;max-height:35vh;border-radius:20px;border:4px solid white;box-shadow:0 20px 60px rgba(0,0,0,0.5);">'
                '<source src="data:video/mp4;base64,' + video_b64 + '" type="video/mp4">'
                '</video>'
                '<div class="media-caption"><b>' + label + '</b><br><span style="font-size:16px;">' + poem + '</span></div>'
                '</div>', unsafe_allow_html=True)

def show_surprise():
    starry = safe_load_media("starry_sky.jpg", "image")
    if starry:
        b64 = img_to_base64(starry, "JPEG")
        bg_html = '<img src="data:image/jpeg;base64,' + b64 + '" style="position:fixed;top:0;left:0;width:100vw;height:100vh;object-fit:cover;z-index:1;">'
    else:
        bg_html = '<div style="position:fixed;top:0;left:0;width:100vw;height:100vh;background:linear-gradient(to bottom,#0a0a2e,#1a1a4e,#2a1a4e);z-index:1;"></div>'
    
    stars = ""
    for _ in range(100):
        sl = random.randint(0, 100); stp = random.randint(0, 100)
        ss = random.randint(1, 3); sd = random.random() * 4
        sdr = 1.5 + random.random() * 4
        stars += '<div style="position:fixed;left:' + str(sl) + '%;top:' + str(stp) + '%;width:' + str(ss) + 'px;height:' + str(ss) + 'px;background:white;border-radius:50%;z-index:2;animation:twinkle ' + str(sdr) + 's ease-in-out ' + str(sd) + 's infinite;"></div>'
    
    floating_particles = ""
    for _ in range(50):
        fl = random.randint(0, 100); ft = random.randint(0, 100)
        fs = random.randint(1, 2); fd = random.random() * 8
        fdr = 3 + random.random() * 6
        fX = random.randint(-30, 30); fY = random.randint(-30, 30)
        floating_particles += (
            '<div style="position:fixed;left:' + str(fl) + '%;top:' + str(ft) + '%;width:' + str(fs) + 'px;height:' + str(fs) + 'px;'
            'background:white;border-radius:50%;z-index:2;opacity:0;'
            'animation:float' + str(fdr) + 's ease-in-out ' + str(fd) + 's infinite;'
            '--fX:' + str(fX) + ';--fY:' + str(fY) + ';"></div>'
        )
    
    meteor_keyframes = ""
    for i in range(5):
        mx = random.randint(-800, -600); my = random.randint(400, 600)
        meteor_keyframes += '@keyframes fly' + str(i) + '{0%{transform:translate(0,0);opacity:0;}5%{opacity:1;}80%{opacity:0.4;}100%{transform:translate(' + str(mx) + 'px,' + str(my) + 'px);opacity:0;}}'
    
    particle_keyframes = ""
    for i in range(5):
        particle_keyframes += '@keyframes part' + str(i) + '{0%{transform:translate(0,0) scale(1);opacity:0.9;}100%{transform:translate(var(--px' + str(i) + '),var(--py' + str(i) + ')) scale(0);opacity:0;}}'
    
    meteors = ""
    for i in range(5):
        dur = round(3.5 + random.random() * 5, 2)
        delay = round(random.random() * 25, 2)
        top_start = random.randint(5, 28)
        left_start = random.randint(65, 95)
        tail_len = 60 + random.randint(30, 70)
        tail_angle = -30
        
        particles = ""
        for j in range(30):
            px = random.randint(10, 80); py = random.randint(-80, -10)
            psize = random.randint(1, 3)
            pdelay = round(random.random() * 3, 2)
            pdur = round(0.8 + random.random() * 1.5, 2)
            particles += (
                '<div style="position:absolute;width:' + str(psize) + 'px;height:' + str(psize) + 'px;'
                'background:white;border-radius:50%;top:0px;left:0px;'
                'box-shadow:0 0 ' + str(psize+3) + 'px ' + str(psize+1) + 'px rgba(255,255,255,0.6);'
                'animation:part' + str(i) + ' ' + str(pdur) + 's ease-out ' + str(pdelay) + 's infinite;'
                '--px' + str(i) + ':' + str(px) + 'px;--py' + str(i) + ':' + str(py) + 'px;'
                'transform:rotate(' + str(tail_angle) + 'deg);transform-origin:left center;z-index:4;opacity:0;"></div>'
            )
        
        meteors += (
            '<div style="position:fixed;top:' + str(top_start) + '%;left:' + str(left_start) + '%;z-index:3;pointer-events:none;animation:fly' + str(i) + ' ' + str(dur) + 's cubic-bezier(0.3,0,0.7,1) ' + str(delay) + 's infinite;opacity:0;">'
            '<div style="position:absolute;width:' + str(tail_len) + 'px;height:6px;background:linear-gradient(to left,rgba(255,255,255,0.01),rgba(180,200,255,0.15));top:-2px;left:0px;border-radius:3px;filter:blur(4px);transform:rotate(' + str(tail_angle) + 'deg);transform-origin:left center;"></div>'
            '<div style="position:absolute;width:' + str(tail_len) + 'px;height:2px;background:linear-gradient(to left,rgba(255,255,255,0.01),rgba(200,220,255,0.35));top:0px;left:0px;border-radius:1px;filter:blur(1px);transform:rotate(' + str(tail_angle) + 'deg);transform-origin:left center;"></div>'
            '<div style="position:absolute;width:' + str(tail_len) + 'px;height:1.5px;background:linear-gradient(to left,rgba(255,255,255,0.02),rgba(255,255,255,0.9));top:0px;left:0px;border-radius:1px;transform:rotate(' + str(tail_angle) + 'deg);transform-origin:left center;"></div>'
            + particles +
            '<div style="position:absolute;width:4px;height:4px;background:white;border-radius:50%;box-shadow:0 0 4px 2px rgba(255,255,255,1),0 0 8px 4px rgba(255,255,255,0.8),0 0 16px 6px rgba(200,220,255,0.5);top:0px;left:0px;z-index:5;"></div>'
            '</div>'
        )
    
    float_keyframes = ""
    for _ in range(50):
        fX = random.randint(-40, 40); fY = random.randint(-40, 40)
        float_keyframes += (
            '@keyframes float' + str(3 + random.random() * 6) + 's {'
            '0%,100% { opacity:0.1; transform:translate(0,0); }'
            '25% { opacity:0.6; transform:translate(' + str(fX) + 'px,' + str(fY) + 'px); }'
            '50% { opacity:0.2; transform:translate(' + str(-fX) + 'px,' + str(-fY) + 'px); }'
            '75% { opacity:0.5; transform:translate(' + str(fY) + 'px,' + str(-fX) + 'px); }'
            '}'
        )
    
    full_html = (
        bg_html + stars + floating_particles + meteors +
        '<style>'
        '@keyframes twinkle{0%,100%{opacity:0.2;transform:scale(1);}50%{opacity:1;transform:scale(2);}}'
        + float_keyframes + meteor_keyframes + particle_keyframes +
        '@keyframes f1{0%{opacity:0;transform:translateY(25px);}10%{opacity:1;transform:translateY(0);}80%{opacity:1;}100%{opacity:0;transform:translateY(-25px);}}'
        '@keyframes f2{0%{opacity:0;transform:translateY(25px);}10%{opacity:1;transform:translateY(0);}80%{opacity:1;}100%{opacity:0;transform:translateY(-25px);}}'
        '@keyframes f3{0%{opacity:0;transform:translateY(25px);}10%{opacity:1;transform:translateY(0);}80%{opacity:1;}100%{opacity:0;transform:translateY(-25px);}}'
        '@keyframes f4{0%{opacity:0;transform:translateY(25px);}10%{opacity:1;transform:translateY(0);}80%{opacity:1;}100%{opacity:0;transform:translateY(-25px);}}'
        '@keyframes f5{0%{opacity:0;transform:translateY(25px);}10%{opacity:1;transform:translateY(0);}80%{opacity:1;}100%{opacity:0;transform:translateY(-25px);}}'
        '</style>'
        '<div style="position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:10;text-align:center;pointer-events:none;width:100%;">'
        '<p style="color:white;font-size:52px;font-weight:bold;text-shadow:0 0 40px rgba(255,215,0,0.8);margin:0;animation:f1 5s ease-in-out both;">✨ 你是我最亮的星 ✨</p>'
        '<p style="color:white;font-size:30px;text-shadow:0 0 30px rgba(255,215,0,0.6);margin:0;animation:f2 5s ease-in-out 5s both;">在茫茫人海中遇见你</p>'
        '<p style="color:#ffd700;font-size:38px;font-weight:bold;text-shadow:0 0 35px rgba(255,215,0,0.7);margin:0;animation:f3 5s ease-in-out 10s both;">就像在浩瀚宇宙中<br>发现了最亮的星 💫</p>'
        '<p style="color:white;font-size:28px;text-shadow:0 0 25px rgba(255,215,0,0.5);margin:0;animation:f4 5s ease-in-out 15s both;">愿我们的爱情<br>如同这璀璨星空<br>永恒而美丽 🌟</p>'
        '<p style="color:#ffd700;font-size:46px;font-weight:bold;text-shadow:0 0 45px rgba(255,215,0,0.9);margin:0;animation:f5 5s ease-in-out 20s both;">💝 生日快乐，永远爱你 💝</p>'
        '</div>'
    )
    
    st.markdown(full_html, unsafe_allow_html=True)
    
    rain(emoji="💖", font_size=25, falling_speed=2, animation_length="infinite")
    rain(emoji="💕", font_size=20, falling_speed=3, animation_length="infinite")
    rain(emoji="💗", font_size=15, falling_speed=4, animation_length="infinite")
    
    st.markdown('<div style="position:fixed;bottom:30px;left:50%;transform:translateX(-50%);z-index:9999;">', unsafe_allow_html=True)
    if st.button("💌 返回情书", key="back_surprise"):
        st.session_state.show_surprise = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        if st.button("🏠 回到主页"):
            st.session_state.show_surprise = False
            st.session_state.envelope_opened = False
            st.rerun()

if __name__ == "__main__":
    main()
