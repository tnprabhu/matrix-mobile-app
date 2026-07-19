import streamlit as st

def inject_styles():
    st.markdown("""
        <style>
        /* Force desktop browsers to wrap the app in a realistic phone shell */
        .main .block-container {
            max-width: 420px !important;
            padding: 1rem 1rem 6rem 1rem !important;
            margin: 0 auto !important;
            background: #FFFFFF;
            min-height: 92vh;
            box-shadow: 0px 10px 40px rgba(0,0,0,0.12);
            border-radius: 40px;
            border: 8px solid #111827;
            position: relative;
        }
        
        /* Hide all default Streamlit headers, menus, and footers */
        #MainMenu, header, footer, [data-testid="stHeader"] { visibility: hidden !important; display: none !important; }
        
        /* Premium Typography & Global Resets */
        * { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important; }
        
        .app-header { display: flex; justify-content: space-between; align-items: center; padding: 10px 5px; margin-bottom: 15px; }
        .app-logo { font-size: 18px; font-weight: 900; color: #312E81; letter-spacing: 1px; text-transform: uppercase; }
        
        /* Progress Indicator Header styling */
        .queue-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 5px; }
        .queue-title { font-size: 16px; font-weight: 800; color: #1F2937; }
        .queue-count { font-size: 12px; color: #9CA3AF; font-weight: 500; }
        
        /* THE SWIPE CARD - Matches your mockup depth and curves */
        .matrix-card {
            background: #FFFFFF;
            border: 1px solid #F3F4F6;
            border-radius: 24px;
            padding: 24px;
            box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.04), 0px 5px 15px rgba(0, 0, 0, 0.02);
            margin-bottom: 20px;
            position: relative;
        }
        
        .badge-priority {
            background: #FFF1F2; color: #E11D48; font-size: 10px; font-weight: 800;
            padding: 4px 10px; border-radius: 20px; letter-spacing: 0.5px; border: 1px solid #FFE4E6;
        }
        .card-counter { float: right; color: #9CA3AF; font-size: 13px; font-weight: 600; }
        
        .profile-section { display: flex; align-items: center; margin: 18px 0; }
        .profile-avatar { width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #3B82F6, #8B5CF6); margin-right: 15px; }
        .profile-name { font-size: 22px; font-weight: 800; color: #111827; letter-spacing: -0.5px; }
        .profile-loc { font-size: 13px; color: #6B7280; font-weight: 500; margin-top: 2px; }
        
        /* AI Box - Clean container border styling */
        .ai-box { background: #FAF5FF; border: 1px solid #F3E8FF; border-radius: 16px; padding: 16px; margin-bottom: 16px; }
        .ai-header { font-size: 12px; font-weight: 800; color: #7C3AED; letter-spacing: 0.5px; text-transform: uppercase; }
        .ai-body { font-size: 14px; color: #4B5563; line-height: 1.5; margin-top: 6px; font-weight: 400; }
        
        /* Recommended Action Box - Premium soft accent backgrounds */
        .action-box { background: #F0FDF4; border: 1px solid #DCFCE7; border-radius: 16px; padding: 16px; }
        .action-header { font-size: 11px; font-weight: 800; color: #16A34A; text-transform: uppercase; letter-spacing: 0.5px; }
        .action-title { font-size: 18px; font-weight: 800; color: #14532D; margin-top: 4px; }
        .action-desc { font-size: 13px; color: #15803D; margin-top: 4px; font-weight: 500; }
        
        /* Fixed Bottom Device Menu Container styling */
        .bottom-nav {
            position: fixed; bottom: 0; left: 50%; transform: translateX(-50%);
            width: 100%; max-width: 420px; background: #FFFFFF;
            border-top: 1px solid #F3F4F6; padding: 10px 0; z-index: 999;
            box-shadow: 0px -10px 30px rgba(0,0,0,0.02);
        }
        </style>
    """, unsafe_allow_html=True)
