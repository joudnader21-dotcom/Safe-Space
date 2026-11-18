import streamlit as st
import streamlit.components.v1 as components
import random

# --- 1. إعداد الصفحة ---
st.set_page_config(layout="wide", page_title="Safe Space | مساحتك الهادئة")

# --- 2. تهيئة متغيرات الجلسة ---
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "step" not in st.session_state:
    st.session_state.step = "welcome"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. قاموس الترجمة والأسئلة ---
TEXTS = {
    "ar": {
        "dir": "rtl",
        "align": "right",
        "title": "🌊 أهلاً بك في مساحتك الهادئة (Safe Space)",
        "subtitle": "بيئة ذكية ومريحة لقياس التوتر، ومراقبة النبض الحي، والتحدث مع المرافق الذكي.",
        "name_label": "ما هو اسمك الكريم؟",
        "name_ph": "اكتب اسمك هنا...",
        "start_btn": "ابدأ رحلة الهدوء 🚀",
        "name_err": "يرجى كتابة اسمك للمتابعة.",
        "quiz_welcome": "مرحباً بك يا",
        "quiz_intro": "بناءً على مقياس الضغط النفسي العالمي (PSS)، أجب عن هذه الأسئلة الـ 8 حسب شعورك خلال الأسبوع الماضي (0 = أبداً، 4 = دائماً):",
        "questions": [
            "1. كم مرة شعرت بالانزعاج بسبب حدث غير متوقع؟",
            "2. كم مرة شعرت بعدم القدرة على التحكم في الأمور المهمة بحياتك؟",
            "3. كم مرة شعرت بالتوتر أو الضغط العصبي؟",
            "4. كم مرة شعرت بالثقة في قدرتك على حل مشاكلك الشخصية؟ (0 = دائماً، 4 = أبداً)",
            "5. كم مرة شعرت أن الأمور تسير كما تخطط لها؟ (0 = دائماً، 4 = أبداً)",
            "6. كم مرة وجدت نفسك عاجزاً عن إنجاز كل المهام المطلوبة منك؟",
            "7. كم مرة تمكنت من السيطرة على انفعالاتك وغضبك؟ (0 = دائماً، 4 = أبداً)",
            "8. كم مرة شعرت أن الصعوبات تتراكم لدرجة يصعب تجاوزها؟"
        ],
        "submit_quiz": "عرض النتيجة والانتقال للمساحة الحية 🎯",
        "dash_title": "لوحة المراقبة الحية والمرافق الذكي",
        "class_label": "تصنيفك وفق المعيار العالمي:",
        "low_stress": "مستوى توتر منخفض ومتوازن (Low Stress - Balanced)",
        "mod_stress": "مستوى توتر متوسط - يُنصح بالاسترخاء (Moderate Stress)",
        "high_stress": "مستوى توتر مرتفع - يحتاج لتمارين تنفس ودعم (High Stress)",
        "chat_header": "💬 المرافق الذكي (فقاعات محادثة تفاعلية)",
        "chat_ph": "احكيلي شو بيصير معك أو بشو حابب تفضفض...",
        "thinking": "بيفكر وبحلل كلامك...",
        "footer_tips_title": "💡 فقاعات إرشادية لحل التوتر والاسترخاء:",
        "refresh_btn": "🔄 تحديث النصائح الفورية"
    },
    "en": {
        "dir": "ltr",
        "align": "left",
        "title": "🌊 Welcome to Your Safe Space",
        "subtitle": "A calm environment to assess stress, monitor live pulse, and chat with the AI companion.",
        "name_label": "What is your name?",
        "name_ph": "Enter your name here...",
        "start_btn": "Enter Safe Space 🚀",
        "name_err": "Please enter your name to continue.",
        "quiz_welcome": "Welcome,",
        "quiz_intro": "Based on the global Perceived Stress Scale (PSS), answer these 8 questions based on the past week (0 = Never, 4 = Very Often):",
        "questions": [
            "1. How often have you been upset because of something unexpected?",
            "2. How often have you felt unable to control the important things in your life?",
            "3. How often have you felt nervous and stressed?",
            "4. How often have you felt confident about handling personal problems? (0 = Very Often, 4 = Never)",
            "5. How often have you felt that things were going your way? (0 = Very Often, 4 = Never)",
            "6. How often have you found that you could not cope with all the things you had to do?",
            "7. How often have you been able to control irritations in your life? (0 = Very Often, 4 = Never)",
            "8. How often have you felt difficulties were piling up so high you could not overcome them?"
        ],
        "submit_quiz": "See Results & Enter Live Dashboard 🎯",
        "dash_title": "Live Bio-Monitor & AI Companion",
        "class_label": "Global Standard Classification:",
        "low_stress": "Low & Balanced Stress Level",
        "mod_stress": "Moderate Stress Level - Self-care advised",
        "high_stress": "High Stress Level - Breathing & relaxation recommended",
        "chat_header": "💬 Smart Companion (Chat Bubbles)",
        "chat_ph": "Tell me what's on your mind...",
        "thinking": "Thinking...",
        "footer_tips_title": "💡 Stress Relief & Relaxation Bubbles:",
        "refresh_btn": "🔄 Refresh Tips"
    }
}

t = TEXTS[st.session_state.lang]

# --- مكتبة النصائح بدون أرقام ---
TIPS_AR = [
    "خذ شهيقاً عميقاً من أنفك لـ 4 ثوانٍ، احبسه لـ 4 ثوانٍ، ثم أفرغه ببطء من فمك.",
    "قم بإرخاء كتفيك واجعلهما مبتعدين عن أذنيك، فالترقوة تحمل الكثير من التوتر المخفي.",
    "اشرب رشفة من الماء البارد أو الدافئ لقطع دائرة التفكير السريع وإعادة تركيز الحواس.",
    "اغمض عينيك لثوانٍ معدودة ووجه امتنانك لشيء بسيط وجميل في غرفتك.",
    "حرك رقبتك ورأسك بحركات دائرية بطيئة وناعمة لتخفيف تشنجات العضلات.",
    "تذكر أن اللحظة الحالية هي الوحيدة التي تملكها؛ المستقبل يأتي وحده فلا تقلقه مقدماً.",
    "عدّل جلستك، واجعل قدميك مستقرّتين على الأرض لتشعر بالثبات والاتزان.",
    "افتح النافذة قليلاً واستنشق نفساً من الهواء النقي لتجديد أكسجين الدماغ.",
    "ابتسم لنفسك ولو تصنعاً، فالابتسامة ترسل إشارات للدماغ بخفض هرمون التوتر.",
    "ركز على دقات قلبك ودعها تتناغم مع تنفسك الهادئ البطيء.",
    "قم بتمارين إطالة خفيفة ليديك وأصابعك إذا كنت تقضي وقتاً طويلاً على لوحة المفاتيح.",
    "ابتعد عن الشاشات والتقنية لدقيقة كاملة وتأمل التفاصيل الهادئة من حولك.",
    "اكتب على ورقة صغيرة شيئاً واحداً يزعجك، ثم امزقها كرمز للتخلص منه.",
    "امنح نفسك استراحة قصيرة وعقلية بلا أي شاشات أو مهام ملحة.",
    "استمع إلى صوت تنفسك واجعله إيقاعك الهادئ الوحيد في هذه اللحظة.",
    "لا تضغط على نفسك لإنجاز كل شيء فوراً؛ الأهم هو استمرارك بهدوء وسلام.",
    "تخيل مكاناً طبيعياً ساحراً تحبه وعش تفاصيله الهادئة.",
    "افرخ راحتي يديك ببعضهما حتى تشعر بالدفء، وضعها على وجهك لثوانٍ.",
    "تذكر إنجازاتك السابقة وكيف تجاوزت أوقاتاً أصعب من هذه بكل قوة.",
    "امنح نفسك العذر والرحمة؛ التوتر إشارة طبيعية بأنك تهتم، فلا تقلق."
]

TIPS_EN = [
    "Take a deep breath in for 4s, hold for 4s, and exhale slowly through your mouth.",
    "Drop your shoulders away from your ears; we unconsciously hold tension there.",
    "Sip a glass of cold or warm water to interrupt rapid thinking and ground your senses.",
    "Close your eyes for a few seconds and appreciate one simple thing around you.",
    "Gently roll your neck and head in slow circles to release tight muscle knots.",
    "Remember the present moment is all you have; let go of future worries for now.",
    "Adjust your posture and plant both feet firmly on the floor for grounding.",
    "Open a window for a moment and breathe in fresh oxygen to clear your mind.",
    "Give yourself a gentle smile; it tricks your brain into lowering stress hormones.",
    "Focus on your heartbeat and synchronize it with your calm, slow breathing.",
    "Do a quick stretch for your hands and fingers if you've been typing a lot.",
    "Step away from all screens for a full minute and just observe your room.",
    "Write down what's bothering you on a scrap paper, then tear it up as release.",
    "Give yourself a guilt-free mental break with zero tasks or screens.",
    "Listen closely to the sound of your breath as your sole anchor right now.",
    "Don't rush to finish everything at once; steady progress wins the race.",
    "Visualize your favorite peaceful nature spot and embrace its calm.",
    "Rub your palms together until warm, then cup them gently over your eyes.",
    "Recall your past wins and how you overcame harder times with resilience.",
    "Be kind to yourself; stress just means you care. Give yourself grace."
]

# --- دالة التحليل المنطقي للشات ---
def get_logical_response(prompt, lang):
    p = prompt.lower()
    if lang == "ar":
        if any(w in p for w in ["توتر", "ضغوط", "قلق", "شغل", "جامعة", "دراسة", "مهام", "مشروع", "امتحان"]):
            options = [
                "واضح إنه عندك كتير شغلات براسك وضاغطتك. شو رأيك نقسمهم لخطوتين سهلين وما نضغط حالنا بكل إشي دفعة وحدة؟",
                "الضغط بهيك مواقف طبيعي، بس صدقني التفكير الزائد بيستهلك طاقتك. خذ دقيقة افصل فيها، وبدنا نركز على أهم شغلة وبس.",
                "حاسس بحجم المسؤولية اللي عليك. طيب شاركني، شو هي أكتر شغلة ضاغطتك هسه عشان نشوف كيف نحلها سوا؟"
            ]
        elif any(w in p for w in ["تعب", "مرهق", "نوم", "دايخ", "مش قادر", "طاقة"]):
            options = [
                "جسمك عم ببعتلك إشارة إنه محتاج استراحة حقيقية. اترك كل إشي من إيدك عشر دقائق وريح عيونك تماماً.",
                "الإرهاق الجسدي بأثر مباشرة على المزاج والتفكير. سمح لحالك تفصل وماتضغط على حالك طول ما إنت تعبان."
            ]
        elif any(w in p for w in ["كيف", "أعمل", "اسوي", "حل", "عصبية", "أعصاب", "كسر"]):
            options = [
                "لغو وكسر التوتر، أول خطوة هي نغير وضعية الجلسة، ونأخذ شهيق عميق من الأنف ونطلقه ببطء. جربها معي هسه.",
                "أفضل طريقة لكسر التوتر هي إننا ننقل تركيزنا من التفكير بشو رح يصير، للحظة الحالية. جرب تطلع حواليك وتسمي 3 أشياء واضحة قدامك."
            ]
        else:
            options = [
                "ممتاز.. عم بفهم عليك. طيب كملي لي أكثر، شو أكثر جانب بالموضوع هاد بشغل بالك؟",
                "جميل جداً إنك عم بتشاركي هالأفكار. كيف بتحسي تأثير هالشغلة عليك هالأيام؟",
                "أنا متابع معك بكل إشي بتحكيه. شاركني تفاصيل أكتر لندردش فيها سوا بهدوء."
            ]
    else:
        if any(w in p for w in ["stress", "pressure", "work", "study", "exam"]):
            options = [
                "It sounds like you have a lot on your plate. How about we break things down into small steps?",
                "When things pile up, it's easy to feel overwhelmed. Let's focus on just one important task."
            ]
        elif any(w in p for w in ["tired", "exhausted", "sleep"]):
            options = [
                "Your body is telling you it needs a real break. Step away from everything for ten minutes.",
                "Physical fatigue affects everything. Please don't push yourself too hard."
            ]
        else:
            options = [
                "I see. Tell me a bit more about what's on your mind regarding this.",
                "That makes sense. How has this been making you feel lately?"
            ]
    return random.choice(options)


# --- التصميم العام ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #bae6fd 100%);
        color: #0f172a;
        direction: {t['dir']};
        text-align: {t['align']};
    }}
    .welcome-box {{
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 40px;
        border-radius: 24px;
        border: 1px solid #7dd3fc;
        box-shadow: 0 10px 25px rgba(2, 132, 199, 0.1);
        text-align: center;
        max-width: 680px;
        margin: 30px auto;
    }}
    .stButton>button {{
        background-color: #0284c7;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #0369a1;
        color: white;
    }}
    [data-testid="stSidebar"] {{ display: none; }}
    
    .bubble-tip {{
        background: linear-gradient(135deg, #fff1f2, #ffe4e6);
        border: 2px solid #fda4af;
        padding: 16px 22px;
        border-radius: 50px;
        margin-bottom: 14px;
        color: #881337;
        font-weight: 600;
        font-size: 15px;
        box-shadow: 0 6px 18px rgba(244, 63, 94, 0.12);
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    .stChatMessage {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-radius: 16px !important;
        padding: 10px 15px !important;
        margin-bottom: 10px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
        border: 1px solid #e0f2fe !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- شريط علوي لتبديل اللغة ---
top_col1, top_col2 = st.columns([6, 1])
with top_col2:
    if st.button("🌐 English" if st.session_state.lang == "ar" else "🌐 العربية"):
        st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"
        st.session_state.messages = []
        st.rerun()

# ==========================================
# الخطوة 1: شاشة الترحيب وإدخال الاسم
# ==========================================
if st.session_state.step == "welcome":
    st.markdown(f"""
        <div class="welcome-box">
            <h1 style='color: #0369a1; margin-bottom: 15px;'>{t['title']}</h1>
            <p style='color: #334155; font-size: 17px; line-height: 1.7;'>{t['subtitle']}</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        name_input = st.text_input(t["name_label"], placeholder=t["name_ph"])
        if st.button(t["start_btn"], use_container_width=True):
            if name_input.strip():
                st.session_state.user_name = name_input.strip()
                st.session_state.step = "quiz"
                st.rerun()
            else:
                st.error(t["name_err"])

# ==========================================
# الخطوة 2: اختبار مقياس الضغط النفسي (PSS)
# ==========================================
elif st.session_state.step == "quiz":
    st.markdown(f"<h2 style='color: #0369a1;'>{t['quiz_welcome']} {st.session_state.user_name} ✨</h2>", unsafe_allow_html=True)
    st.info(t["quiz_intro"])

    with st.form("pss_quiz"):
        answers = []
        for idx, q_text in enumerate(t["questions"]):
            val = st.slider(q_text, 0, 4, 1, key=f"q_{idx}")
            answers.append(val)

        if st.form_submit_button(t["submit_quiz"], use_container_width=True):
            score = (
                answers[0] + answers[1] + answers[2] +
                (4 - answers[3]) + (4 - answers[4]) +
                answers[5] + (4 - answers[6]) + answers[7]
            )
            st.session_state.quiz_score = score
            st.session_state.step = "dashboard"
            st.rerun()

# ==========================================
# الخطوة 3: لوحة المراقبة الحية
# ==========================================
elif st.session_state.step == "dashboard":
    score = st.session_state.quiz_score
    if score <= 10:
        classification = t["low_stress"]
        stress_level = "low"
    elif score <= 20:
        classification = t["mod_stress"]
        stress_level = "moderate"
    else:
        classification = t["high_stress"]
        stress_level = "high"

    st.markdown(f"<h2 style='color: #0369a1; margin-bottom: 5px;'>📊 {t['dash_title']} - {st.session_state.user_name}</h2>", unsafe_allow_html=True)
    st.success(f"**{t['class_label']}** {classification} ({score} / 32)")

    col_chat, col_cam = st.columns([0.8, 1.6], gap="large")

    # --- القسم الأيمن: الشات الذكي بفقاعات المحادثة ---
    with col_chat:
        st.subheader(t["chat_header"])
        chat_container = st.container(height=420)

        if not st.session_state.messages:
            if st.session_state.lang == "ar":
                welcome_msg = f"أهلاً بك يا {st.session_state.user_name} 🌿. نتيجتك تشير إلى **{classification}**. احكيلي، شو أكتر اشي شاغل بالك أو ضاغطك هالفترة؟"
            else:
                welcome_msg = f"Welcome {st.session_state.user_name} 🌿. Your assessment shows **{classification}**. Tell me, what's been on your mind lately?"
            st.session_state.messages.append(
                {"role": "assistant", "content": welcome_msg}
            )

        with chat_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        if user_prompt := st.chat_input(t["chat_ph"], key="smart_chat"):
            st.session_state.messages.append(
                {"role": "user", "content": user_prompt}
            )
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(user_prompt)

            with chat_container:
                with st.chat_message("assistant"):
                    with st.spinner(t["thinking"]):
                        reply_text = get_logical_response(user_prompt, st.session_state.lang)
                        st.markdown(reply_text)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": reply_text}
                        )

    # --- القسم الأيسر: الكاميرا ومخطط المساحة الممتلئة المتغير السرعة ---
    with col_cam:
        cam_btn_text = "تشغيل الكاميرا الحية / Toggle Camera" if st.session_state.lang == "ar" else "Toggle Live Camera"
        cam_off_text = "إيقاف الكاميرا / Turn Off Camera" if st.session_state.lang == "ar" else "Turn Off Camera"
        cam_lbl = "الكاميرا مغلقة حالياً / Camera is OFF - المخطط متوقف" if st.session_state.lang == "ar" else "Camera is OFF - ECG Paused"

        # تمرير المتغيرات بطريقة آمنة داخل كود HTML/JS لعدم حدوث خطأ syntax
        html_code = f"""
        <div style="background: rgba(255,255,255,0.95); padding: 15px; border-radius: 18px; border: 1px solid #7dd3fc; box-shadow: 0 4px 15px rgba(0,0,0,0.05); font-family: sans-serif; text-align: center;">
            <div style="margin-bottom: 12px;">
                <button id="toggleCam" onclick="toggleCamera()" style="background: #0284c7; color: white; border: none; padding: 10px 22px; border-radius: 12px; cursor: pointer; font-weight: bold; font-size: 14px;">{cam_btn_text}</button>
            </div>
            
            <div style="background: #0f172a; border-radius: 14px; overflow: hidden; height: 250px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;" id="camBox">
                <video id="cam" autoplay playsinline style="width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); display: none;"></video>
                <div id="camPlaceholder" style="color: #94a3b8; font-size: 15px;">{cam_lbl}</div>
            </div>

            <div style="width: 100%; background: #0f172a; border-radius: 12px; border: 1px solid #38bdf8; overflow: hidden; padding: 6px;">
                <canvas id="areaChartCanvas" style="width: 100%; height: 150px; display: block;"></canvas>
            </div>
        </div>

        <script>
            const video = document.getElementById('cam');
            const placeholder = document.getElementById('camPlaceholder');
            const btn = document.getElementById('toggleCam');
            const canvas = document.getElementById('areaChartCanvas');
            const ctx = canvas.getContext('2d');

            let streamRef = null;
            let isCamOn = false;
            let stressLevel = "{stress_level}";

            function toggleCamera() {{
                if (!isCamOn) {{
                    navigator.mediaDevices.getUserMedia({{ video: true }})
                        .then(stream => {{
                            streamRef = stream;
                            video.srcObject = stream;
                            video.style.display = 'block';
                            placeholder.style.display = 'none';
                            btn.innerText = "{cam_off_text}";
                            btn.style.background = '#e11d48';
                            isCamOn = true;
                        }})
                        .catch(err => alert("تعذر الوصول للكاميرا: " + err));
                }} else {{
                    if (streamRef) {{
                        streamRef.getTracks().forEach(track => track.stop());
                    }}
                    video.srcObject = null;
                    video.style.display = 'none';
                    placeholder.style.display = 'block';
                    btn.innerText = "{cam_btn_text}";
                    btn.style.background = '#0284c7';
                    isCamOn = false;
                }}
            }}

            let dataPoints = [];
            let maxPoints = 120;
            let stepCounter = 0;

            function drawAreaChart() {{
                if (canvas.width !== canvas.offsetWidth || canvas.height !== 150) {{
                    canvas.width = canvas.offsetWidth || 500;
                    canvas.height = 150;
                }}
                
                const width = canvas.width;
                const height = canvas.height;

                ctx.fillStyle = '#0f172a';
                ctx.fillRect(0, 0, width, height);

                ctx.strokeStyle = 'rgba(56, 189, 248, 0.1)';
                ctx.lineWidth = 1;
                for (let i = 0; i < width; i += 40) {{
                    ctx.beginPath();
                    ctx.moveTo(i, 0);
                    ctx.lineTo(i, height);
                    ctx.stroke();
                }}
                for (let j = 0; j < height; j += 35) {{
                    ctx.beginPath();
                    ctx.moveTo(0, j);
                    ctx.lineTo(width, j);
                    ctx.stroke();
                }}

                if (!isCamOn) {{
                    ctx.beginPath();
                    ctx.strokeStyle = '#38bdf8';
                    ctx.lineWidth = 2.5;
                    ctx.moveTo(0, height / 2);
                    ctx.lineTo(width, height / 2);
                    ctx.stroke();
                    dataPoints = [];
                    requestAnimationFrame(drawAreaChart);
                    return;
                }}

                let speed = 2;
                if (stressLevel === 'high') {{
                    speed = 0.8;
                }} else if (stressLevel === 'low') {{
                    speed = 3.5;
                }} else {{
                    speed = 2;
                }}

                stepCounter += speed;
                if (stepCounter >= 12) {{
                    stepCounter = 0;
                    let newY = height - (30 + Math.random() * 80);
                    dataPoints.push(newY);
                    if (dataPoints.length > maxPoints) {{
                        dataPoints.shift();
                    }}
                }}

                if (dataPoints.length > 1) {{
                    const dx = width / maxPoints;

                    ctx.beginPath();
                    ctx.moveTo(0, height);
                    for (let i = 0; i < dataPoints.length; i++) {{
                        ctx.lineTo(i * dx, dataPoints[i]);
                    }}
                    ctx.lineTo((dataPoints.length - 1) * dx, height);
                    ctx.closePath();

                    let gradient = ctx.createLinearGradient(0, 0, 0, height);
                    gradient.addColorStop(0, 'rgba(56, 189, 248, 0.5)');
                    gradient.addColorStop(1, 'rgba(15, 23, 42, 0.1)');
                    ctx.fillStyle = gradient;
                    ctx.fill();

                    ctx.beginPath();
                    ctx.moveTo(0, dataPoints[0]);
                    for (let i = 0; i < dataPoints.length; i++) {{
                        ctx.lineTo(i * dx, dataPoints[i]);
                    }}
                    ctx.strokeStyle = '#38bdf8';
                    ctx.lineWidth = 2.5;
                    ctx.stroke();
                }}

                requestAnimationFrame(drawAreaChart);
            }}
            drawAreaChart();
        </script>
        """
        components.html(html_code, height=480)

    # ==========================================
    # القسم السفلي: فقاعات النصائح الدائرية اللطيفة (مع زر تحديث)
    # ==========================================
    st.markdown(f"<h4 style='color: #0369a1; margin-top: 25px;'>{t['footer_tips_title']}</h4>", unsafe_allow_html=True)
    
    if st.button(t['refresh_btn']):
        st.rerun()

    active_tips = TIPS_AR if st.session_state.lang == "ar" else TIPS_EN
    selected_footer_tips = random.sample(active_tips, 3)

    for tip in selected_footer_tips:
        st.markdown(f"""
            <div class="bubble-tip">
                🫧 {tip}
            </div>
        """, unsafe_allow_html=True)