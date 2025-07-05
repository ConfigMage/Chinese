import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Configure page
st.set_page_config(
    page_title="Chinese Dinner Vote Collector",
    page_icon="🥢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #DC2626, #F59E0B);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .food-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    .success-message {
        background: #10b981;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    .stats-card {
        background: #f3f4f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .must-have {
        background: #fef2f2;
        border-left: 4px solid #DC2626;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .popular {
        background: #fff7ed;
        border-left: 4px solid #F59E0B;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'votes' not in st.session_state:
    st.session_state.votes = []
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

# Guest names and food options with emojis
GUESTS = [
    "Marj",
    "Ron", 
    "Maya and Kaleb",
    "Mark and Nichole",
    "Quinn"
]

FOOD_OPTIONS = {
    "🍤 Sweet & Sour Shrimp": "Sweet & Sour Shrimp",
    "🍖 BBQ Pork": "BBQ Pork",
    "🍚 Pork Fried Rice": "Pork Fried Rice",
    "🍜 Pork Chow Mein": "Pork Chow Mein",
    "🥚 Egg Foo Young": "Egg Foo Young",
    "🦐 Shrimp Fried Rice": "Shrimp Fried Rice",
    "🍛 Curry Chicken Egg Foo Young": "Curry Chicken Egg Foo Young",
    "🍙 Steamed Rice": "Steamed Rice",
    "🥬 Green Bean Chicken": "Green Bean Chicken",
    "🌶️ Kung Pao Chicken": "Kung Pao Chicken",
    "🥦 Beef and Broccoli": "Beef and Broccoli",
    "🍊 Orange Chicken": "Orange Chicken",
    "🦀 Crab Puffs": "Crab Puffs"
}

PREFERENCE_OPTIONS = [
    "🔥 Gotta have it",
    "😋 I'd like some of this", 
    "❌ No thanks",
    "❓ What is that"
]

def submit_vote(guest_name, preferences):
    """Submit a vote and handle duplicates"""
    # Remove any existing votes from this guest
    st.session_state.votes = [vote for vote in st.session_state.votes if vote['guest'] != guest_name]
    
    # Add new votes
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for food_display, preference in preferences.items():
        food_name = FOOD_OPTIONS[food_display]
        vote = {
            'guest': guest_name,
            'food_item': food_name,
            'food_display': food_display,
            'preference': preference,
            'timestamp': timestamp
        }
        st.session_state.votes.append(vote)

def get_guest_previous_votes(guest_name):
    """Get previous votes for a guest"""
    guest_votes = {}
    for vote in st.session_state.votes:
        if vote['guest'] == guest_name:
            guest_votes[vote['food_display']] = vote['preference']
    return guest_votes

def get_vote_summary():
    """Generate voting analytics"""
    if not st.session_state.votes:
        return {}
    
    df = pd.DataFrame(st.session_state.votes)
    
    summary = {}
    summary['total_votes'] = len(df['guest'].unique())
    summary['total_responses'] = len(df)
    
    # Must-have items
    must_haves = df[df['preference'] == '🔥 Gotta have it']['food_item'].value_counts()
    summary['must_haves'] = must_haves.to_dict()
    
    # Popular items (gotta have + like some)
    popular_prefs = ['🔥 Gotta have it', '😋 I\'d like some of this']
    popular = df[df['preference'].isin(popular_prefs)]['food_item'].value_counts()
    summary['popular'] = popular.to_dict()
    
    # Items to skip
    skip_items = df[df['preference'] == '❌ No thanks']['food_item'].value_counts()
    summary['skip'] = skip_items.to_dict()
    
    # Items needing explanation
    explain_items = df[df['preference'] == '❓ What is that']['food_item'].value_counts()
    summary['explain'] = explain_items.to_dict()
    
    return summary

# Header
st.markdown("""
<div class="main-header">
    <h1>🥢 Chinese Dinner Vote Collector 🥡</h1>
    <p>Help us decide what to order for tonight's feast!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🧭 Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["🗳️ Cast Your Vote", "📊 View Results", "⚙️ Admin Panel"]
)

# Show current vote count in sidebar
vote_count = len(set(vote['guest'] for vote in st.session_state.votes))
st.sidebar.markdown(f"""
<div class="stats-card">
    <h3>📈 Current Status</h3>
    <p><strong>{vote_count}/{len(GUESTS)}</strong> guests have voted</p>
</div>
""", unsafe_allow_html=True)

if page == "🗳️ Cast Your Vote":
    st.header("🗳️ Cast Your Vote")
    
    # Guest selection
    selected_guest = st.selectbox(
        "👋 Who are you?",
        ["Select your name..."] + GUESTS,
        key="guest_selector"
    )
    
    if selected_guest != "Select your name...":
        # Check if guest has already voted
        previous_votes = get_guest_previous_votes(selected_guest)
        
        if previous_votes:
            st.info(f"✏️ {selected_guest}, you've already voted! You can update your preferences below.")
        
        st.subheader(f"🍽️ Food Preferences for {selected_guest}")
        st.write("Please select your preference for each dish:")
        
        # Create form for all food preferences
        with st.form(key="voting_form"):
            preferences = {}
            
            # Create columns for better layout
            col1, col2 = st.columns(2)
            
            food_items = list(FOOD_OPTIONS.keys())
            mid_point = len(food_items) // 2
            
            # Left column
            with col1:
                for food_display in food_items[:mid_point]:
                    default_index = 0
                    if food_display in previous_votes:
                        try:
                            default_index = PREFERENCE_OPTIONS.index(previous_votes[food_display])
                        except ValueError:
                            default_index = 0
                    
                    preference = st.radio(
                        food_display,
                        PREFERENCE_OPTIONS,
                        key=f"pref_{food_display}",
                        index=default_index
                    )
                    preferences[food_display] = preference
            
            # Right column
            with col2:
                for food_display in food_items[mid_point:]:
                    default_index = 0
                    if food_display in previous_votes:
                        try:
                            default_index = PREFERENCE_OPTIONS.index(previous_votes[food_display])
                        except ValueError:
                            default_index = 0
                    
                    preference = st.radio(
                        food_display,
                        PREFERENCE_OPTIONS,
                        key=f"pref_{food_display}",
                        index=default_index
                    )
                    preferences[food_display] = preference
            
            # Submit button
            submit_button = st.form_submit_button(
                "🎯 Submit My Votes",
                use_container_width=True
            )
            
            if submit_button:
                submit_vote(selected_guest, preferences)
                st.markdown("""
                <div class="success-message">
                    <h3>🎉 Thank you for voting!</h3>
                    <p>Your preferences have been recorded successfully.</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
                time.sleep(1)
                st.rerun()

elif page == "📊 View Results":
    st.header("📊 Voting Results")
    
    if not st.session_state.votes:
        st.warning("📭 No votes have been cast yet!")
    else:
        summary = get_vote_summary()
        
        # Overview stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <h3>👥 Total Voters</h3>
                <h2>{summary['total_votes']}/{len(GUESTS)}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            completion_rate = (summary['total_votes'] / len(GUESTS)) * 100
            st.markdown(f"""
            <div class="stats-card">
                <h3>📈 Completion Rate</h3>
                <h2>{completion_rate:.0f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-card">
                <h3>📝 Total Responses</h3>
                <h2>{summary['total_responses']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Must-have items
        if summary['must_haves']:
            st.subheader("🔥 Must-Have Items")
            for item, count in summary['must_haves'].items():
                st.markdown(f"""
                <div class="must-have">
                    <strong>{item}</strong> - {count} person(s) gotta have it!
                </div>
                """, unsafe_allow_html=True)
        
        # Popular items
        if summary['popular']:
            st.subheader("😋 Popular Items")
            for item, count in summary['popular'].items():
                st.markdown(f"""
                <div class="popular">
                    <strong>{item}</strong> - {count} positive vote(s)
                </div>
                """, unsafe_allow_html=True)
        
        # Items to explain
        if summary['explain']:
            st.subheader("❓ Items Needing Explanation")
            for item, count in summary['explain'].items():
                st.warning(f"**{item}** - {count} person(s) want to know what this is")
        
        # Items to avoid
        if summary['skip']:
            st.subheader("❌ Items to Consider Skipping")
            for item, count in summary['skip'].items():
                st.error(f"**{item}** - {count} person(s) said no thanks")
        
        # Detailed breakdown
        st.subheader("📋 Detailed Vote Breakdown")
        df = pd.DataFrame(st.session_state.votes)
        display_df = df[['guest', 'food_display', 'preference', 'timestamp']].copy()
        display_df.columns = ['Guest', 'Food Item', 'Preference', 'Time Voted']
        st.dataframe(display_df, use_container_width=True)

elif page == "⚙️ Admin Panel":
    st.header("⚙️ Admin Panel")
    
    if not st.session_state.admin_authenticated:
        st.subheader("🔐 Admin Authentication")
        password = st.text_input("Enter admin password:", type="password")
        if st.button("Login"):
            if password == "dinnertime":  # Simple password
                st.session_state.admin_authenticated = True
                st.success("✅ Successfully authenticated!")
                st.rerun()
            else:
                st.error("❌ Incorrect password!")
    else:
        st.success("✅ Authenticated as admin")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Reset All Votes", type="secondary"):
                if st.button("⚠️ Confirm Reset", type="primary"):
                    st.session_state.votes = []
                    st.success("All votes have been reset!")
                    st.rerun()
        
        with col2:
            if st.button("📤 Export Votes as CSV"):
                if st.session_state.votes:
                    df = pd.DataFrame(st.session_state.votes)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"chinese_dinner_votes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No votes to export!")
        
        # Manual vote entry
        st.subheader("✍️ Manual Vote Entry")
        with st.expander("Add vote manually"):
            manual_guest = st.selectbox("Guest:", GUESTS, key="manual_guest")
            manual_food = st.selectbox("Food item:", list(FOOD_OPTIONS.keys()), key="manual_food")
            manual_pref = st.selectbox("Preference:", PREFERENCE_OPTIONS, key="manual_pref")
            
            if st.button("➕ Add Manual Vote"):
                vote = {
                    'guest': manual_guest,
                    'food_item': FOOD_OPTIONS[manual_food],
                    'food_display': manual_food,
                    'preference': manual_pref,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.votes.append(vote)
                st.success(f"Added vote for {manual_guest}")
                st.rerun()
        
        if st.button("🚪 Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()

# Footer
st.markdown("---")
st.markdown("🥡 **Chinese Dinner Vote Collector** | Made with ❤️ and Streamlit")