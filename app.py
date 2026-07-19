import streamlit as st
import requests
from matrix_styles import inject_styles

class MatrixAPI:
    WF005_URL = "https://pipedream.net" 
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
inject_styles()

CURRENT_VOLUNTEER_ID = "PER-001"
if "active_tab" not in st.session_state: st.session_state.active_tab = "Actions"
if "queue_ptr" not in st.session_state: st.session_state.queue_ptr = 0
if "show_more" not in st.session_state: st.session_state.show_more = False

def handle_action_commit(action_id, outcome_value):
    result = matrix.call(operation="COMPLETE_ACTION", personId=CURRENT_VOLUNTEER_ID, actionId=action_id, outcome=outcome_value)
    if result.get("success", True): st.toast("✅ Action Synced!")
    else: st.toast("❌ Sync Error")
    st.session_state.queue_ptr += 1
    st.session_state.show_more = False

@st.fragment
def draw_viewport():
    st.markdown('<div class="app-header"><div style="color:#9CA3AF; font-size:22px; font-weight:300;">☰</div><div class="app-logo">MATRIX</div><div style="color:#F59E0B; font-size:22px;">🔔</div></div>', unsafe_allow_html=True)
    
    if st.session_state.active_tab == "Home":
        data = matrix.call(operation="HOME", personId=CURRENT_VOLUNTEER_ID)
        st.markdown("### Today's Mission")
        st.caption(data.get("Mission", "Campaign"))
        st.metric(label="Situation Summary", value=data.get("SituationSummary", "Active"), delta=f"{data.get('CompletedActions', 0)} Done")
        st.info(f"📋 AI Priorities:\n1. {data.get('Priority1', 'Review High Priority Leads')}\n2. {data.get('Priority2', 'Follow up')}")
        
    elif st.session_state.active_tab == "Actions":
        res = matrix.call(operation="ACTION_QUEUE", personId=CURRENT_VOLUNTEER_ID)
        records = res.get("actions", [])
        if not records:
            records = [{"ActionID": "ACT-001", "FullName": "Sokha Chenda", "City": "Phnom Penh", "Country": "Cambodia", "Priority": "High Priority", "AISummary": "Sokha is experiencing high stress due to work pressure and overthinking. Shows openness to mindfulness practices.", "RecommendedAction": "Share Calm Survey", "Objective": "Help her understand her stress pattern better."}]
        
        total_cards = len(records)
        current_idx = st.session_state.queue_ptr
        if current_idx >= total_cards:
            st.markdown("<div style='text-align:center; padding:40px 10px; color:#6B7280;'><h3>🎉 Queue Clear!</h3></div>", unsafe_allow_html=True)
            if st.button("Reset Pointer"):
                st.session_state.queue_ptr = 0
                st.rerun()
        else:
            item = records[current_idx]
            st.markdown(f'<div class="queue-header"><div class="queue-title">Today\'s Queue</div><div class="queue-count">{total_cards - current_idx} left</div></div>', unsafe_allow_html=True)
            st.progress(current_idx / total_cards)
            
            card_html = f"""
            <div class="matrix-card">
                <div><span class="badge-priority">🚨 {item.get("Priority")}</span><span class="card-counter">{current_idx + 1}/{total_cards}</span></div>
                <div class="profile-section">
                    <div class="profile-avatar"></div>
                    <div>
                        <div class="profile-name">{item.get("FullName")}</div>
                        <div class="profile-loc">📍 {item.get("City")}, {item.get("Country")}</div>
                    </div>
                </div>
                <div class="ai-box">
                    <div class="ai-header">🔮 AI Summary</div>
                    <div class="ai-body">{item.get("AISummary")}</div>
                </div>
                <div class="action-box">
                    <div class="action-header">Recommended Action</div>
                    <div class="action-title">{item.get("RecommendedAction")}</div>
                    <div class="action-desc">{item.get("Objective")}</div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            c_cols = st.columns(4)
            with c_cols: st.button("💬 WA", key="c_wa", use_container_width=True)
            with c_cols: st.button("✈️ TG", key="c_tg", use_container_width=True)
            with c_cols: st.button("📞 Call", key="c_ph", use_container_width=True)
            with c_cols: st.button("📋 Copy", key="c_cp", use_container_width=True)
            
            st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
            act_cols = st.columns(3)
            with act_cols:
                if st.button("◀ Later", key="act_skip", use_container_width=True):
                    st.session_state.queue_ptr = (st.session_state.queue_ptr + 1) % total_cards
                    st.rerun()
            with act_cols:
                if st.button("🔼 More", key="act_drawer", use_container_width=True):
                    st.session_state.show_more = not st.session_state.show_more
                    st.rerun()
            with act_cols:
                st.button("🟢 Done", key="act_done", type="primary", use_container_width=True, on_click=handle_action_commit, args=(item.get("ActionID"), "Completed"))
            
            if st.session_state.show_more:
                st.markdown("---")
                dr_cols = st.columns(3)
                with dr_cols:
                    if st.button("💤 Snooze", use_container_width=True): handle_action_commit(item.get("ActionID"), "Snoozed")
                with dr_cols:
                    if st.button("🔄 Escalate", use_container_width=True): handle_action_commit(item.get("ActionID"), "Escalated")
                with dr_cols:
                    if st.button("❌ Drop", use_container_width=True): handle_action_commit(item.get("ActionID"), "Dropped")
    else:
        st.markdown(f"### Management: {st.session_state.active_tab}")
        
    st.markdown('<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)
    f_cols = st.columns(5)
    navs = [("🏠", "Home"), ("👥", "Leads"), ("✔", "Actions"), ("📂", "Programs"), ("⚙", "More")]
    for idx, (icon, name) in enumerate(navs):
        with f_cols[idx]:
            is_sel = st.session_state.active_tab == name
            txt = f"**{icon}\n{name}**" if is_sel else f"{icon}\n{name}"
            if st.button(txt, key=f"nav_{name}", use_container_width=True):
                st.session_state.active_tab = name
                st.rerun()

draw_viewport()
