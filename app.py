import streamlit as st
import time
import random
from datetime import datetime, timedelta
import json

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OmniChat AI – Multi-Channel Business Automation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #13131a;
    --card: #1a1a26;
    --border: #2a2a3d;
    --accent: #7c3aed;
    --accent2: #06b6d4;
    --accent3: #f59e0b;
    --green: #10b981;
    --red: #ef4444;
    --text: #e2e8f0;
    --muted: #64748b;
}

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

.stApp { background: var(--bg); }

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Hide default header */
header[data-testid="stHeader"] { display: none; }

/* Metric cards */
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin: 8px 0;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: var(--accent);
}
.metric-card.green::before { background: var(--green); }
.metric-card.cyan::before { background: var(--accent2); }
.metric-card.amber::before { background: var(--accent3); }

.metric-val {
    font-family: 'Space Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1;
}
.metric-label { font-size: 0.78rem; color: var(--muted); margin-top: 4px; letter-spacing: 0.08em; text-transform: uppercase; }
.metric-delta { font-size: 0.82rem; margin-top: 6px; }
.delta-up { color: var(--green); }
.delta-down { color: var(--red); }

/* Chat bubbles */
.chat-bubble {
    padding: 12px 16px;
    border-radius: 18px;
    margin: 6px 0;
    max-width: 80%;
    font-size: 0.9rem;
    line-height: 1.5;
    position: relative;
}
.chat-user {
    background: var(--accent);
    margin-left: auto;
    border-bottom-right-radius: 4px;
}
.chat-bot {
    background: var(--card);
    border: 1px solid var(--border);
    border-bottom-left-radius: 4px;
}
.chat-meta {
    font-size: 0.7rem;
    color: var(--muted);
    margin: 2px 4px;
    font-family: 'Space Mono', monospace;
}

/* Channel pills */
.channel-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    margin: 2px;
}
.pill-whatsapp { background: #25d36622; color: #25d366; border: 1px solid #25d36644; }
.pill-instagram { background: #e1306c22; color: #e1306c; border: 1px solid #e1306c44; }
.pill-facebook { background: #1877f222; color: #1877f2; border: 1px solid #1877f244; }
.pill-linkedin { background: #0a66c222; color: #0a66c2; border: 1px solid #0a66c244; }
.pill-voice { background: #f59e0b22; color: #f59e0b; border: 1px solid #f59e0b44; }
.pill-website { background: #06b6d422; color: #06b6d4; border: 1px solid #06b6d444; }

/* Status dot */
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 6px;
}
.dot-online { background: var(--green); box-shadow: 0 0 6px var(--green); }
.dot-busy { background: var(--accent3); }
.dot-offline { background: var(--muted); }

/* Section headers */
.section-header {
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 20px 0 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero-banner::after {
    content: '⚡';
    position: absolute;
    right: 32px; top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.08;
}
.hero-title {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #fff 0%, #7c3aed 50%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}
.hero-sub { color: var(--muted); font-size: 0.95rem; margin-top: 8px; }

/* Inbox table row */
.inbox-row {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 6px 0;
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    transition: border-color 0.2s;
}
.inbox-row:hover { border-color: var(--accent); }

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Input fields */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* Success/Error */
.stSuccess { background: #10b98120 !important; border-color: var(--green) !important; }
.stError { background: #ef444420 !important; }

/* Divider */
hr { border-color: var(--border) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface);
    border-radius: 10px;
    gap: 4px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 7px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: white !important;
}

/* Progress bar */
.stProgress > div > div { background: var(--accent) !important; }

/* Expander */
.streamlit-expanderHeader {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background: var(--card) !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ─────────────────────────────────────────────────────────
if "conversations" not in st.session_state:
    st.session_state.conversations = [
        {"id": 1, "name": "Rahul Sharma", "channel": "WhatsApp", "message": "Hi, I want to book an appointment for tomorrow", "time": "2 min ago", "status": "open", "unread": 2},
        {"id": 2, "name": "Priya Mehta", "channel": "Instagram", "message": "Do you ship to Mumbai?", "time": "5 min ago", "status": "open", "unread": 1},
        {"id": 3, "name": "Arjun Patel", "channel": "Facebook", "message": "What are your business hours?", "time": "12 min ago", "status": "resolved", "unread": 0},
        {"id": 4, "name": "Sarah Johnson", "channel": "LinkedIn", "message": "Interested in your enterprise plan", "time": "25 min ago", "status": "open", "unread": 3},
        {"id": 5, "name": "+91 98765 43210", "channel": "Voice", "message": "Missed call – callback scheduled", "time": "1 hr ago", "status": "pending", "unread": 0},
        {"id": 6, "name": "Website Visitor #4821", "channel": "Website", "message": "How do I reset my password?", "time": "2 hr ago", "status": "resolved", "unread": 0},
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "user", "text": "Hi, I want to book an appointment for tomorrow", "time": "14:22"},
        {"role": "bot", "text": "Hello Rahul! I'd be happy to help you book an appointment. 📅\n\nWe have the following slots available tomorrow:\n• 10:00 AM\n• 2:00 PM\n• 4:30 PM\n\nWhich time works best for you?", "time": "14:22"},
        {"role": "user", "text": "2 PM works for me", "time": "14:23"},
        {"role": "bot", "text": "Perfect! I've booked your appointment for **tomorrow at 2:00 PM**. ✅\n\nYou'll receive a confirmation message shortly. Is there anything else I can help you with?", "time": "14:23"},
    ]

if "leads" not in st.session_state:
    st.session_state.leads = [
        {"name": "Rahul Sharma", "phone": "+91 98765 43210", "email": "rahul@email.com", "channel": "WhatsApp", "status": "Appointment Booked", "value": "₹15,000"},
        {"name": "Priya Mehta", "phone": "+91 87654 32109", "email": "priya@email.com", "channel": "Instagram", "status": "Interested", "value": "₹8,500"},
        {"name": "Sarah Johnson", "phone": "+1 555-0123", "email": "sarah@corp.com", "channel": "LinkedIn", "status": "Enterprise Lead", "value": "₹2,50,000"},
        {"name": "Amit Kumar", "phone": "+91 76543 21098", "email": "amit@startup.io", "channel": "Website", "status": "Trial Signup", "value": "₹5,000"},
        {"name": "Neha Singh", "phone": "+91 65432 10987", "email": "neha@biz.in", "channel": "Facebook", "status": "Qualified", "value": "₹32,000"},
    ]

if "appointments" not in st.session_state:
    today = datetime.now()
    st.session_state.appointments = [
        {"name": "Rahul Sharma", "time": (today + timedelta(days=1)).strftime("%b %d") + " · 2:00 PM", "type": "Demo Call", "channel": "WhatsApp", "status": "Confirmed"},
        {"name": "Priya Mehta", "time": today.strftime("%b %d") + " · 4:30 PM", "type": "Product Inquiry", "channel": "Instagram", "status": "Confirmed"},
        {"name": "Sarah Johnson", "time": (today + timedelta(days=2)).strftime("%b %d") + " · 11:00 AM", "type": "Enterprise Onboarding", "channel": "LinkedIn", "status": "Pending"},
    ]

if "kb_articles" not in st.session_state:
    st.session_state.kb_articles = [
        {"title": "How to reset your password", "category": "Account", "queries": 142},
        {"title": "Shipping policy and delivery times", "category": "Orders", "queries": 98},
        {"title": "Pricing plans and billing", "category": "Billing", "queries": 87},
        {"title": "Return and refund policy", "category": "Orders", "queries": 76},
        {"title": "How to contact human support", "category": "Support", "queries": 65},
    ]

if "selected_conv" not in st.session_state:
    st.session_state.selected_conv = 1

if "auto_reply_enabled" not in st.session_state:
    st.session_state.auto_reply_enabled = True

if "ai_tone" not in st.session_state:
    st.session_state.ai_tone = "Professional"

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 16px 0 24px;">
        <div style="font-family: 'Space Mono', monospace; font-size: 1.1rem; font-weight: 700; color: #7c3aed;">OmniChat AI</div>
        <div style="font-size: 0.72rem; color: #64748b; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 2px;">Business Automation Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Navigation</div>', unsafe_allow_html=True)
    page = st.radio(
        "",
        ["🏠  Dashboard", "💬  Unified Inbox", "🤖  AI Chat Simulator", "📋  Lead Manager", "📅  Appointments", "🧠  Knowledge Base", "📊  Analytics", "⚙️  Settings"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="section-header">Channels Live</div>', unsafe_allow_html=True)
    channels = [
        ("WhatsApp", "dot-online", "14 active"),
        ("Instagram", "dot-online", "8 active"),
        ("Facebook", "dot-busy", "3 active"),
        ("LinkedIn", "dot-online", "2 active"),
        ("Voice", "dot-busy", "1 call"),
        ("Website", "dot-online", "22 sessions"),
    ]
    for ch, dot, count in channels:
        st.markdown(f'<div style="display:flex; justify-content:space-between; align-items:center; padding:6px 0; border-bottom: 1px solid #1a1a26; font-size:0.85rem;"><span><span class="status-dot {dot}"></span>{ch}</span><span style="color:#64748b; font-size:0.75rem;">{count}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">AI Agent</div>', unsafe_allow_html=True)
    st.session_state.auto_reply_enabled = st.toggle("Auto-Reply Active", value=st.session_state.auto_reply_enabled)
    if st.session_state.auto_reply_enabled:
        st.success("✅ AI Agent Online")
    else:
        st.warning("⚠️ Manual Mode")

# ─── Main Content ───────────────────────────────────────────────────────────────
page_key = page.split("  ")[1].strip()

# ── DASHBOARD ──────────────────────────────────────────────────────────────────
if page_key == "Dashboard":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Multi-Channel AI Automation</div>
        <div class="hero-sub">Unify WhatsApp · Instagram · Facebook · LinkedIn · Voice · Website into one intelligent hub</div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="metric-card green">
            <div class="metric-val">1,284</div>
            <div class="metric-label">Messages Today</div>
            <div class="metric-delta delta-up">↑ 18% vs yesterday</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="metric-card cyan">
            <div class="metric-val">94.2%</div>
            <div class="metric-label">Auto-Reply Rate</div>
            <div class="metric-delta delta-up">↑ 3.1% this week</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-card amber">
            <div class="metric-val">47</div>
            <div class="metric-label">Leads Captured</div>
            <div class="metric-delta delta-up">↑ 12 new today</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="metric-card">
            <div class="metric-val">1.4s</div>
            <div class="metric-label">Avg Response Time</div>
            <div class="metric-delta delta-up">↓ 89% faster than manual</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-header">Recent Conversations</div>', unsafe_allow_html=True)
        channel_icons = {"WhatsApp": "💬", "Instagram": "📸", "Facebook": "👤", "LinkedIn": "💼", "Voice": "📞", "Website": "🌐"}
        channel_class = {"WhatsApp": "pill-whatsapp", "Instagram": "pill-instagram", "Facebook": "pill-facebook", "LinkedIn": "pill-linkedin", "Voice": "pill-voice", "Website": "pill-website"}
        status_col = {"open": "#10b981", "resolved": "#64748b", "pending": "#f59e0b"}

        for conv in st.session_state.conversations[:5]:
            icon = channel_icons.get(conv["channel"], "💬")
            pill = channel_class.get(conv["channel"], "")
            sc = status_col.get(conv["status"], "#64748b")
            unread_badge = f'<span style="background:#7c3aed; color:white; font-size:0.65rem; padding:2px 7px; border-radius:999px; font-weight:700;">{conv["unread"]}</span>' if conv["unread"] > 0 else ""
            st.markdown(f"""
            <div class="inbox-row">
                <div style="font-size:1.4rem;">{icon}</div>
                <div style="flex:1; min-width:0;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; font-size:0.9rem;">{conv["name"]}</span>
                        <span style="font-size:0.72rem; color:#64748b;">{conv["time"]}</span>
                    </div>
                    <div style="font-size:0.8rem; color:#64748b; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{conv["message"]}</div>
                    <div style="margin-top:4px; display:flex; gap:6px; align-items:center;">
                        <span class="channel-pill {pill}">{conv["channel"]}</span>
                        <span style="font-size:0.7rem; color:{sc}; font-weight:600;">● {conv["status"].upper()}</span>
                        {unread_badge}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-header">Channel Volume</div>', unsafe_allow_html=True)
        channels_data = {"WhatsApp": 38, "Instagram": 22, "Website": 18, "Facebook": 12, "LinkedIn": 6, "Voice": 4}
        for ch, pct in channels_data.items():
            pill = channel_class.get(ch, "")
            st.markdown(f'<div style="display:flex; justify-content:space-between; font-size:0.82rem; margin-bottom:4px;"><span class="channel-pill {pill}">{ch}</span><span style="color:#64748b;">{pct}%</span></div>', unsafe_allow_html=True)
            st.progress(pct / 100)

        st.markdown('<div class="section-header" style="margin-top:20px;">Today\'s Appointments</div>', unsafe_allow_html=True)
        for appt in st.session_state.appointments[:2]:
            st.markdown(f"""
            <div style="background:#1a1a26; border:1px solid #2a2a3d; border-radius:8px; padding:10px 14px; margin:4px 0;">
                <div style="font-weight:700; font-size:0.85rem;">{appt["name"]}</div>
                <div style="font-size:0.75rem; color:#64748b;">{appt["time"]} · {appt["type"]}</div>
                <div style="font-size:0.7rem; color:#10b981; margin-top:2px;">● {appt["status"]}</div>
            </div>
            """, unsafe_allow_html=True)

# ── UNIFIED INBOX ──────────────────────────────────────────────────────────────
elif page_key == "Unified Inbox":
    st.markdown("## 💬 Unified Inbox")
    st.caption("All conversations across channels in one place")

    filter_col, search_col = st.columns([2, 4])
    with filter_col:
        ch_filter = st.selectbox("Channel", ["All Channels", "WhatsApp", "Instagram", "Facebook", "LinkedIn", "Voice", "Website"])
    with search_col:
        search = st.text_input("Search conversations...", placeholder="Name, message, or keyword")

    channel_icons = {"WhatsApp": "💬", "Instagram": "📸", "Facebook": "👤", "LinkedIn": "💼", "Voice": "📞", "Website": "🌐"}
    channel_class = {"WhatsApp": "pill-whatsapp", "Instagram": "pill-instagram", "Facebook": "pill-facebook", "LinkedIn": "pill-linkedin", "Voice": "pill-voice", "Website": "pill-website"}
    status_col = {"open": "#10b981", "resolved": "#64748b", "pending": "#f59e0b"}

    filtered = st.session_state.conversations
    if ch_filter != "All Channels":
        filtered = [c for c in filtered if c["channel"] == ch_filter]
    if search:
        filtered = [c for c in filtered if search.lower() in c["name"].lower() or search.lower() in c["message"].lower()]

    for conv in filtered:
        icon = channel_icons.get(conv["channel"], "💬")
        pill = channel_class.get(conv["channel"], "")
        sc = status_col.get(conv["status"], "#64748b")
        if st.button(f"{icon}  {conv['name']}  ·  {conv['time']}", key=f"conv_{conv['id']}"):
            st.session_state.selected_conv = conv["id"]
            st.rerun()

        st.markdown(f"""
        <div style="background:#1a1a26; border:1px solid #2a2a3d; border-radius:10px; padding:12px 16px; margin:-8px 0 8px 0;">
            <div style="font-size:0.82rem; color:#a0aec0;">{conv["message"]}</div>
            <div style="margin-top:6px;">
                <span class="channel-pill {pill}">{conv["channel"]}</span>
                <span style="font-size:0.7rem; color:{sc}; margin-left:8px;">● {conv["status"].upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── AI CHAT SIMULATOR ──────────────────────────────────────────────────────────
elif page_key == "AI Chat Simulator":
    st.markdown("## 🤖 AI Chat Simulator")
    st.caption("Test your AI agent's responses in real-time")

    col_config, col_chat = st.columns([1, 2])

    with col_config:
        st.markdown('<div class="section-header">Agent Config</div>', unsafe_allow_html=True)
        channel_sim = st.selectbox("Simulating channel", ["WhatsApp", "Instagram", "Facebook", "LinkedIn", "Website"])
        tone = st.selectbox("AI Tone", ["Professional", "Friendly", "Concise", "Detailed"])
        st.session_state.ai_tone = tone

        st.markdown('<div class="section-header">Capabilities</div>', unsafe_allow_html=True)
        caps = {
            "Answer FAQs": True,
            "Book Appointments": True,
            "Capture Leads": True,
            "Escalate to Human": True,
            "Send Media": False,
        }
        for cap, default in caps.items():
            st.checkbox(cap, value=default)

        if st.button("🔄 Reset Chat"):
            st.session_state.chat_history = []
            st.rerun()

    with col_chat:
        st.markdown('<div class="section-header">Conversation</div>', unsafe_allow_html=True)
        chat_container = st.container()

        with chat_container:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div style="display:flex; justify-content:flex-end; margin:6px 0;">
                        <div>
                            <div class="chat-bubble chat-user">{msg["text"]}</div>
                            <div class="chat-meta" style="text-align:right;">{msg["time"]}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="display:flex; gap:8px; margin:6px 0;">
                        <div style="font-size:1.2rem; margin-top:4px;">🤖</div>
                        <div>
                            <div class="chat-bubble chat-bot">{msg["text"]}</div>
                            <div class="chat-meta">{msg["time"]} · AI Agent</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        msg_col, btn_col = st.columns([5, 1])
        with msg_col:
            user_input = st.text_input("Type a message...", key="user_msg", placeholder="e.g. I want to book an appointment")
        with btn_col:
            st.markdown("<br>", unsafe_allow_html=True)
            send_btn = st.button("Send ➤")

        # Quick test prompts
        st.markdown('<div class="section-header">Quick Test Prompts</div>', unsafe_allow_html=True)
        quick_cols = st.columns(3)
        quick_prompts = [
            "Book an appointment",
            "What are your prices?",
            "Speak to a human",
            "Business hours?",
            "Track my order",
            "Cancel subscription",
        ]
        for i, prompt in enumerate(quick_prompts):
            with quick_cols[i % 3]:
                if st.button(prompt, key=f"qp_{i}"):
                    user_input = prompt
                    send_btn = True

        if send_btn and user_input:
            now = datetime.now().strftime("%H:%M")
            st.session_state.chat_history.append({"role": "user", "text": user_input, "time": now})

            # Simulated AI responses
            responses = {
                "appointment": "I'd love to help schedule that for you! 📅\n\nAvailable slots:\n• Today 4:00 PM\n• Tomorrow 10:00 AM\n• Tomorrow 2:00 PM\n\nWhich works best?",
                "price": "Here's our pricing overview 💰\n\n• **Starter** – ₹999/mo (3 channels)\n• **Growth** – ₹2,499/mo (all channels)\n• **Enterprise** – Custom pricing\n\nWant me to connect you with our sales team?",
                "human": "Connecting you to a live agent now 👤\n\nEstimated wait: ~2 minutes\nYour ticket ID: #TKT-4821\n\nA team member will join this chat shortly.",
                "hour": "Our business hours are:\n⏰ Mon–Fri: 9:00 AM – 7:00 PM\n⏰ Sat: 10:00 AM – 4:00 PM\n🔴 Sun: Closed\n\nOutside hours, I (AI) am available 24/7!",
                "order": "Sure! Please share your Order ID and I'll pull up the latest tracking info right away 📦",
                "cancel": "I'm sorry to hear that! Before we proceed, may I ask what's prompting the cancellation? We'd love to help resolve any issues 🙏",
            }

            ai_text = "Thanks for reaching out! Let me check that for you...\n\nIs there anything specific you'd like to know more about? I'm here 24/7 to assist! 😊"
            for kw, resp in responses.items():
                if kw in user_input.lower():
                    ai_text = resp
                    break

            time.sleep(0.5)
            st.session_state.chat_history.append({"role": "bot", "text": ai_text, "time": now})
            st.rerun()

# ── LEAD MANAGER ───────────────────────────────────────────────────────────────
elif page_key == "Lead Manager":
    st.markdown("## 📋 Lead Manager")
    st.caption("All captured leads from every channel")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="metric-card green"><div class="metric-val">47</div><div class="metric-label">Total Leads</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="metric-card cyan"><div class="metric-val">12</div><div class="metric-label">New Today</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="metric-card amber"><div class="metric-val">₹3.1L</div><div class="metric-label">Pipeline Value</div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Lead Pipeline</div>', unsafe_allow_html=True)

    add_col, _ = st.columns([3, 3])
    with add_col:
        with st.expander("➕ Add New Lead Manually"):
            n1, n2 = st.columns(2)
            with n1:
                new_name = st.text_input("Full Name")
                new_phone = st.text_input("Phone")
            with n2:
                new_email = st.text_input("Email")
                new_channel = st.selectbox("Channel", ["WhatsApp", "Instagram", "Facebook", "LinkedIn", "Voice", "Website"])
            if st.button("Add Lead"):
                if new_name:
                    st.session_state.leads.append({
                        "name": new_name, "phone": new_phone, "email": new_email,
                        "channel": new_channel, "status": "New", "value": "₹0"
                    })
                    st.success(f"✅ Lead '{new_name}' added!")
                    st.rerun()

    channel_class = {"WhatsApp": "pill-whatsapp", "Instagram": "pill-instagram", "Facebook": "pill-facebook", "LinkedIn": "pill-linkedin", "Voice": "pill-voice", "Website": "pill-website"}
    status_colors = {"Appointment Booked": "#10b981", "Interested": "#06b6d4", "Enterprise Lead": "#7c3aed", "Trial Signup": "#f59e0b", "Qualified": "#10b981", "New": "#64748b"}

    for i, lead in enumerate(st.session_state.leads):
        pill = channel_class.get(lead["channel"], "")
        sc = status_colors.get(lead["status"], "#64748b")
        cols = st.columns([3, 2, 2, 2, 2, 1])
        with cols[0]:
            st.markdown(f"**{lead['name']}**")
            st.caption(lead.get("email", ""))
        with cols[1]:
            st.markdown(f'<span class="channel-pill {pill}">{lead["channel"]}</span>', unsafe_allow_html=True)
        with cols[2]:
            st.caption(lead.get("phone", ""))
        with cols[3]:
            st.markdown(f'<span style="color:{sc}; font-weight:600; font-size:0.82rem;">{lead["status"]}</span>', unsafe_allow_html=True)
        with cols[4]:
            st.markdown(f'**{lead["value"]}**')
        with cols[5]:
            if st.button("✉️", key=f"lead_{i}"):
                st.toast(f"Message sent to {lead['name']}!")
        st.divider()

# ── APPOINTMENTS ───────────────────────────────────────────────────────────────
elif page_key == "Appointments":
    st.markdown("## 📅 Appointment Manager")
    st.caption("AI-booked appointments from all channels")

    tab1, tab2 = st.tabs(["📋 Upcoming", "➕ Book New"])

    with tab1:
        channel_class = {"WhatsApp": "pill-whatsapp", "Instagram": "pill-instagram", "Facebook": "pill-facebook", "LinkedIn": "pill-linkedin"}
        for appt in st.session_state.appointments:
            pill = channel_class.get(appt["channel"], "pill-whatsapp")
            sc = "#10b981" if appt["status"] == "Confirmed" else "#f59e0b"
            st.markdown(f"""
            <div style="background:#1a1a26; border:1px solid #2a2a3d; border-radius:12px; padding:18px 20px; margin:8px 0; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-weight:700; font-size:1rem;">{appt["name"]}</div>
                    <div style="font-size:0.82rem; color:#64748b; margin-top:2px;">🗓️ {appt["time"]} · {appt["type"]}</div>
                    <div style="margin-top:6px;"><span class="channel-pill {pill}">{appt["channel"]}</span></div>
                </div>
                <div style="text-align:right;">
                    <div style="color:{sc}; font-weight:700; font-size:0.85rem;">● {appt["status"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            client_name = st.text_input("Client Name")
            appt_type = st.selectbox("Appointment Type", ["Demo Call", "Product Inquiry", "Support Call", "Enterprise Onboarding", "Follow-up"])
        with c2:
            appt_date = st.date_input("Date", min_value=datetime.now().date())
            appt_time = st.selectbox("Time Slot", ["9:00 AM", "10:00 AM", "11:00 AM", "2:00 PM", "3:00 PM", "4:30 PM"])
        appt_channel = st.selectbox("Channel", ["WhatsApp", "Instagram", "Facebook", "LinkedIn", "Website"])
        if st.button("📅 Book Appointment"):
            if client_name:
                st.session_state.appointments.append({
                    "name": client_name,
                    "time": f"{appt_date.strftime('%b %d')} · {appt_time}",
                    "type": appt_type,
                    "channel": appt_channel,
                    "status": "Confirmed"
                })
                st.success(f"✅ Appointment booked for {client_name} on {appt_date} at {appt_time}!")
                st.balloons()
                st.rerun()

# ── KNOWLEDGE BASE ─────────────────────────────────────────────────────────────
elif page_key == "Knowledge Base":
    st.markdown("## 🧠 Knowledge Base")
    st.caption("Train your AI with your business information")

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<div class="section-header">Top Articles (by query volume)</div>', unsafe_allow_html=True)
        for art in st.session_state.kb_articles:
            st.markdown(f"""
            <div style="background:#1a1a26; border:1px solid #2a2a3d; border-radius:10px; padding:14px 18px; margin:6px 0; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-weight:600;">{art["title"]}</div>
                    <div style="font-size:0.75rem; color:#64748b; margin-top:2px;">{art["category"]}</div>
                </div>
                <div style="font-family: 'Space Mono', monospace; color:#7c3aed; font-size:0.9rem;">{art["queries"]} queries</div>
            </div>
            """, unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-header">Add Article</div>', unsafe_allow_html=True)
        art_title = st.text_input("Article Title")
        art_cat = st.selectbox("Category", ["Account", "Orders", "Billing", "Support", "Products", "Technical"])
        art_content = st.text_area("Content", height=150, placeholder="Enter the FAQ or knowledge article content here...")
        if st.button("➕ Add to KB"):
            if art_title and art_content:
                st.session_state.kb_articles.append({"title": art_title, "category": art_cat, "queries": 0})
                st.success("✅ Article added to Knowledge Base!")
                st.rerun()

    st.markdown('<div class="section-header">Training Status</div>', unsafe_allow_html=True)
    training_items = [
        ("Business FAQs", 95),
        ("Product Catalog", 78),
        ("Pricing Information", 100),
        ("Shipping & Returns", 88),
        ("Support Procedures", 62),
    ]
    for item, pct in training_items:
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.caption(item)
            st.progress(pct / 100)
        with col_b:
            st.markdown(f'<div style="font-family:Space Mono,monospace; font-size:0.85rem; color:#7c3aed; padding-top:20px;">{pct}%</div>', unsafe_allow_html=True)

# ── ANALYTICS ──────────────────────────────────────────────────────────────────
elif page_key == "Analytics":
    st.markdown("## 📊 Analytics Dashboard")
    st.caption("7-day performance overview")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""<div class="metric-card green"><div class="metric-val">8,921</div><div class="metric-label">Messages (7d)</div><div class="metric-delta delta-up">↑ 22%</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="metric-card cyan"><div class="metric-val">312</div><div class="metric-label">Leads (7d)</div><div class="metric-delta delta-up">↑ 31%</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="metric-card amber"><div class="metric-val">87</div><div class="metric-label">Appointments (7d)</div><div class="metric-delta delta-up">↑ 15%</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class="metric-card"><div class="metric-val">4.8★</div><div class="metric-label">CSAT Score</div><div class="metric-delta delta-up">↑ 0.3 pts</div></div>""", unsafe_allow_html=True)

    import pandas as pd
    import numpy as np

    st.markdown('<div class="section-header" style="margin-top:24px;">Message Volume (Last 7 Days)</div>', unsafe_allow_html=True)
    dates = [(datetime.now() - timedelta(days=i)).strftime("%b %d") for i in range(6, -1, -1)]
    msg_data = pd.DataFrame({
        "Date": dates,
        "WhatsApp": [320, 280, 350, 410, 290, 380, 420],
        "Instagram": [120, 100, 140, 160, 110, 130, 150],
        "Facebook": [80, 70, 90, 100, 75, 85, 95],
        "LinkedIn": [30, 25, 35, 40, 28, 32, 38],
    }).set_index("Date")
    st.bar_chart(msg_data)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="section-header">Response Time Trend</div>', unsafe_allow_html=True)
        rt_data = pd.DataFrame({
            "Date": dates,
            "Avg Response (s)": [4.2, 3.8, 2.9, 2.1, 1.8, 1.5, 1.4]
        }).set_index("Date")
        st.line_chart(rt_data)

    with col_r:
        st.markdown('<div class="section-header">Lead Conversion Rate</div>', unsafe_allow_html=True)
        conv_data = pd.DataFrame({
            "Date": dates,
            "Conversion %": [12, 14, 15, 18, 17, 21, 23]
        }).set_index("Date")
        st.line_chart(conv_data)

# ── SETTINGS ──────────────────────────────────────────────────────────────────
elif page_key == "Settings":
    st.markdown("## ⚙️ Platform Settings")

    tab1, tab2, tab3 = st.tabs(["🔗 Channels", "🤖 AI Config", "🔔 Notifications"])

    with tab1:
        st.markdown('<div class="section-header">Connected Channels</div>', unsafe_allow_html=True)
        channels_config = [
            ("WhatsApp Business API", "✅ Connected", "Meta Cloud API", "#10b981"),
            ("Instagram Direct", "✅ Connected", "Meta Graph API v18", "#10b981"),
            ("Facebook Messenger", "✅ Connected", "Meta Graph API v18", "#10b981"),
            ("LinkedIn Messaging", "⚠️ Limited", "LinkedIn API v2", "#f59e0b"),
            ("Voice (Twilio)", "✅ Connected", "Twilio Voice SDK", "#10b981"),
            ("Website Chat Widget", "✅ Connected", "WebSocket v3", "#10b981"),
        ]
        for name, status, api, color in channels_config:
            c1, c2, c3 = st.columns([3, 2, 2])
            with c1:
                st.markdown(f"**{name}**")
            with c2:
                st.markdown(f'<span style="color:{color}; font-size:0.82rem;">{status}</span>', unsafe_allow_html=True)
            with c3:
                st.caption(api)
            st.divider()

    with tab2:
        st.markdown('<div class="section-header">AI Agent Configuration</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("LLM Model", ["GPT-4o", "Claude Sonnet", "Gemini Pro"])
            st.selectbox("Response Tone", ["Professional", "Friendly", "Concise"])
            st.slider("Response Confidence Threshold", 0.0, 1.0, 0.75)
        with c2:
            st.selectbox("Fallback Action", ["Escalate to Human", "Send Canned Response", "Collect Contact"])
            st.number_input("Max Auto-Reply per User/Day", value=50, min_value=1)
            st.toggle("Enable Sentiment Analysis", value=True)
        if st.button("💾 Save AI Config"):
            st.success("✅ AI configuration saved!")

    with tab3:
        st.markdown('<div class="section-header">Notification Preferences</div>', unsafe_allow_html=True)
        st.toggle("New lead notification (Email)", value=True)
        st.toggle("New appointment notification (WhatsApp)", value=True)
        st.toggle("Escalation alert (SMS)", value=True)
        st.toggle("Daily summary report (Email)", value=False)
        st.toggle("Weekly analytics digest", value=True)
        if st.button("💾 Save Notifications"):
            st.success("✅ Notification settings saved!")
