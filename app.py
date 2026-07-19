import streamlit as st
import time
import requests

class MatrixAPI:
    WF005_URL = "https://eoj9ly7gnug54z4.m.pipedream.net" 
    TIMEOUT = 30

    def call(self, operation: str, **kwargs):
        request = {"operation": operation}
        request.update(kwargs)
        try:
            response = requests.post(self.WF005_URL, json=request, timeout=self.TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": str(e)}

matrix = MatrixAPI()

st.set_page_config(page_title="MATRIX Mobile", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .main .block-container {
        max-width: 420px !important;
        padding: 1rem 1rem 6rem 1rem !important;
        margin: 0 auto !important;
        background: #FFFFFF;
        min-height: 100vh;
        box-shadow: 0px 4px 24px rgba(0,0,0,0.06);
        border-radius: 24px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    #MainMenu, header, footer {visibility: hidden;}
    
    .app-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
    .app-logo { font-size: 20px; font-weight: 800; color: #4F46E5; letter-spacing: -0.5px; }
    
    .queue-header { display: flex; justify-content: space-between; align-items: baseline; font-size: 14px; margin-bottom: 2px; }
    .queue-title { font-weight: 700; color: #111827; }
    .queue-count { color: #6B7280; font-size: 12px; }
    
    .matrix-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 18px;
        padding: 16px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.03);
    }
    .badge-priority {
        background: #FEE2E2; color: #DC2626; font-size: 10px; font-weight: 700;
        padding: 2px 6px; border-radius: 6px; text-transform: uppercase;
    }
    .card-counter { float: right; color: #9CA3AF; font-size: 12px; }
    .profile-section { display: flex; align-items: center; margin: 12px 0; }
    .profile-avatar { width: 52px; height: 52px; border-radius: 50%; background: #E5E7EB; margin-right: 12px; object-fit: cover; }
    .profile-name { font-size: 18px; font-weight: 700; color: #111827; }
    .profile-loc { font-size: 12px; color: #6B7280; margin-top: 2px; }
    
    .ai-box { background: #F5F3FF; border: 1px solid #DDD6FE; border-radius: 12px; padding: 12px; margin-bottom: 12px; }
    .ai-header { font-size: 12px; font-weight: 700; color: #6D28D9; display: flex; align-items: center; gap: 4px; }
    .ai-body { font-size: 13px; color: #4B5563; line-height: 1.4; margin-top: 6px; }
    
    .bottom-nav {
        position: fixed; bottom: 0; left: 50%; transform: translateX(-50%);
        width: 100%; max-width: 420px; background: #FFFFFF;
        border-top: 1px solid #E5E7EB; padding: 6px 0; z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

CURRENT_VOLUNTEER_ID = "PER-001"

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Actions"

if "queue_ptr" not in st.session_state:
    st.session_state.queue_ptr = 0

if "show_more" not in st.session_state:
    st.session_state.show_more = False

def handle_action_commit(action_id, outcome_value):
    result = matrix.call(
        operation="COMPLETE_ACTION",
        personId=CURRENT_VOLUNTEER_ID,
        actionId=action_id,
        outcome=outcome_value
    )
    if result.get("success", True):
        st.toast("✅ Action Synced Successfully!")
    else:
        st.toast(f"❌ Error: {result.get('message', 'Failed to update backend')}")
    st.session_state.queue_ptr += 1
    st.session_state.show_more = False
@st.fragment
def draw_viewport():
    st.markdown("""
        <div class="app-header">
            <div style="color:#6B7280; font-size:20px;">☰</div>
            <div class="app-logo">MATRIX</div>
            <div style="position:relative; color:#6B7280; font-size:20px;">🔔</div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.active_tab == "Home":
        data = matrix.call(operation="HOME", personId=CURRENT_VOLUNTEER_ID)
        st.markdown("### Today's Mission")
        st.caption(data.get("Mission", "General Mobilization Campaign"))
        st.metric(
            label="Situation Summary", 
            value=data.get("SituationSummary", "Active Processing"),
            delta=f"{data.get('CompletedActions', 0)} Done"
        )
        st.info(f"📋 **AI Priorities:**\n1. {data.get('Priority1', 'Review High Priority Leads')}\n2. {data.get('Priority2', 'Follow up on Telegram open requests')}")

    elif st.session_state.active_tab == "Actions":
        res = matrix.call(operation="ACTION_QUEUE", personId=CURRENT_VOLUNTEER_ID)
        records = res.get("actions", [])
        
        if not records:
            records = [{
                "ActionID": "ACT-001", "ProspectID": "PRO-001", "PersonID": "PER-101",
                "FullName": "Sokha Chenda", "City": "Phnom Penh", "Country": "Cambodia",
                "Priority": "High Priority", "AISummary": "Sokha is experiencing high stress due to work pressure and overthinking. Shows openness to mindfulness practices.",
                "RecommendedAction": "Share Calm Survey", "Objective": "Help her understand her stress pattern better."
            }]
            
        total_cards = len(records)
        current_idx = st.session_state.queue_ptr
        
        if current_idx >= total_cards:
            st.markdown("""
                <div style='text-align:center; padding:40px 10px; color:#6B7280;'>
                    <h3>🎉 Queue Clear!</h3>
                    <p style='font-size:13px;'>All assigned tasks have been executed successfully.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Reset Action Deck Pointer"):
                st.session_state.queue_ptr = 0
                st.rerun()
        else:
            item = records[current_idx]
            st.markdown(f"""
                <div class="queue-header">
                    <div class="queue-title">Today's Queue</div>
                    <div class="queue-count">{total_cards - current_idx} remaining</div>
                </div>
            """, unsafe_allow_html=True)
            st.progress((current_idx) / total_cards)
            
            card_html = f"""
                <div class="matrix-card">
                    <div>
                        <span class="badge-priority">⚠️ {item.get('Priority', 'Normal')}</span>
                        <span class="card-counter">{current_idx + 1}/{total_cards}</span>
                    </div>
                    <div class="profile-section">
                        <div class="profile-avatar" style="background-image: linear-gradient(135deg, #6EE7B7 0%, #3B82F6 100%);"></div>
                        <div>
                            <div class="profile-name">{item.get('FullName', 'Unknown Lead')}</div>
                            <div class="profile-loc">📍 {item.get('City', 'Unknown Loc')}, {item.get('Country', 'KH')}</div>
                        </div>
                    </div>
                    <div class="ai-box">
                        <div class="ai-header">✨ AI Summary</div>
                        <div class="ai-body">{item.get('AISummary', 'No summary data compiled.')}</div>
                    </div>
                    <div class="matrix-card" style="background-color: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 12px; padding: 12px; margin-bottom: 12px;">
                        <div style="font-size: 11px; font-weight: 600; color: #16A34A; text-transform: uppercase;">Recommended Action</div>
                        <div style="font-size: 15px; font-weight: 700; color: #14532D;">{item.get('RecommendedAction', 'Contact Lead')}</div>
                        <div style="font-size: 12px; color: #166534;">{item.get('Objective', 'Execute follow up sequence.')}</div>
                    </div>
                </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            channel_cols = st.columns(4)
            with channel_cols: st.button("💬 WA", key="c_wa", use_container_width=True)
            with channel_cols: st.button("✈️ TG", key="c_tg", use_container_width=True)
            with channel_cols: st.button("📞 Call", key="c_ph", use_container_width=True)
            with channel_cols: st.button("📋 Copy", key="c_cp", use_container_width=True)
            
            st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
            
            act_cols = st.columns(3)
            with act_cols:
                if st.button("◀\nLater", key="act_skip", use_container_width=True):
                    st.session_state.queue_ptr = (st.session_state.queue_ptr + 1) % total_cards
                    st.rerun()
            with act_cols:
                if st.button("🔼\nMore", key="act_drawer", use_container_width=True):
                    st.session_state.show_more = not st.session_state.show_more
                    st.rerun()
            with act_cols:
                st.button("🟢\nDone", key="act_done", type="primary", use_container_width=True, 
                          on_click=handle_action_commit, args=(item.get("ActionID"), "Completed"))
            
            if st.session_state.show_more:
                st.markdown("---")
                drawer_cols = st.columns(3)
                with drawer_cols:
                    if st.button("💤 Snooze", use_container_width=True):
                        handle_action_commit(item.get("ActionID"), "Snoozed")
                with drawer_cols:
                    if st.button("🔄 Escalate", use_container_width=True):
                        handle_action_commit(item.get("ActionID"), "Escalated")
                with drawer_cols:
                    if st.button("❌ Drop", use_container_width=True):
                        handle_action_commit(item.get("ActionID"), "Dropped")

    else:
        st.markdown(f"### Management Center: {st.session_state.active_tab}")
        st.caption("Standard system record access console view panel container layout.")

    st.markdown('<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)
    
    footer_cols = st.columns(5)
    navigation_schema = [("🏠", "Home"), ("👥", "Leads"), ("✔", "Actions"), ("📂", "Programs"), ("⚙", "More")]
    
    for idx, (icon, name) in enumerate(navigation_schema):
        with footer_cols[idx]:
            is_selected = st.session_state.active_tab == name
            btn_text = f"**{icon}\n{name}**" if is_selected else f"{icon}\n{name}"
            if st.button(btn_text, key=f"nav_target_{name}", use_container_width=True):
                st.session_state.active_tab = name
                st.rerun()

draw_viewport()
