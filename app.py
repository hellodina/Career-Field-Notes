import streamlit as st
from datetime import datetime
from models import ENTRIES
from persistence import (
    create_student, get_student, get_entry_status,
    get_student_entries, save_entry_response, get_entry_response,
    update_student, add_resource, get_student_resources, delete_resource
)
# PDF export coming soon

st.set_page_config(
    page_title="Career Field Notes",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Init session state
if "student" not in st.session_state:
    st.session_state.student = None
if "page" not in st.session_state:
    st.session_state.page = "join"
if "current_entry" not in st.session_state:
    st.session_state.current_entry = None

# Custom CSS
st.markdown("""
<style>
    .big-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #2c3e50;
    }
    .subtitle {
        font-size: 1rem;
        color: #7f8c8d;
        margin-bottom: 1.5rem;
    }
    .vibe-check {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- PAGES ---

def show_join():
    """Join screen: name + date + avatar."""
    if "selected_avatar" not in st.session_state:
        st.session_state.selected_avatar = "🚀"

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="big-title">Career Field Notes</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Explore careers. Document your journey. Find your path.</div>', unsafe_allow_html=True)

        st.write("")
        st.write("**Let's Get Started**")
        name = st.text_input("Your name", placeholder="e.g., Alex", key="join_name")
        date = st.text_input("Internship season", placeholder="e.g., Summer 2026", key="join_date")

        st.write("**Pick your avatar:**")
        avatars = ["🚀", "🌟", "💡", "🎯", "⚡", "🌈", "🎨", "🔥"]
        cols = st.columns(len(avatars))
        for i, avatar in enumerate(avatars):
            with cols[i]:
                if st.button(avatar, use_container_width=True, key=f"avatar_{i}"):
                    st.session_state.selected_avatar = avatar

        st.write(f"Selected: {st.session_state.selected_avatar}")

        if st.button("Let's Go", use_container_width=True, type="primary"):
            if name.strip() and date.strip():
                avatar = st.session_state.selected_avatar
                student = create_student(name.strip(), date.strip())
                student.avatar = avatar
                update_student(student.id, avatar=avatar)
                st.session_state.student = student
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error("Gotta fill both fields, no cap.")

def show_home():
    """Trail home: 6 entries, unlock as you go."""
    student = st.session_state.student

    # Header with avatar + custom title
    col1, col2, col3 = st.columns([0.08, 0.85, 0.07])
    with col1:
        st.markdown(f'<div style="font-size: 2.5rem; margin-top: 0.2rem;">{student.avatar}</div>', unsafe_allow_html=True)
    with col2:
        title_text = student.custom_title or "My Journey to Becoming a..."
        st.markdown(f'<div class="big-title">{title_text}</div>', unsafe_allow_html=True)
    with col3:
        if st.button("✏️", key="edit_title_btn", help="Edit your journal title"):
            st.session_state.editing_title = True

    if st.session_state.get("editing_title", False):
        st.write("**Name your journal:**")
        new_title = st.text_input(
            "Your story",
            value=student.custom_title or "",
            placeholder="e.g., My Journey to Becoming a UX Designer",
            key="title_input"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save", use_container_width=True, type="primary", key="save_title"):
                if new_title.strip():
                    update_student(student.id, custom_title=new_title.strip())
                    st.session_state.student.custom_title = new_title.strip()
                    st.session_state.editing_title = False
                    st.rerun()
        with col2:
            if st.button("Cancel", use_container_width=True, key="cancel_title"):
                st.session_state.editing_title = False
                st.rerun()
        st.write("")

    st.write(f"**{student.display_name}** • {student.internship_date}")

    # Progress
    entries = get_student_entries(student.id)
    completed = sum(1 for e in entries.values() if e and e.status == "done")
    st.progress(completed / 6, text=f"{completed}/6 entries done")

    st.write("")

    # Entry cards
    for entry_num in range(1, 7):
        entry_template = ENTRIES[entry_num]
        status = get_entry_status(student.id, entry_num)

        col1, col2 = st.columns([0.85, 0.15])

        with col1:
            if st.button(
                f"📖 **{entry_template['title']}** — {entry_template['subtitle']}",
                use_container_width=True,
                key=f"btn_entry_{entry_num}"
            ):
                st.session_state.current_entry = entry_num
                st.session_state.page = "entry"
                st.rerun()

        with col2:
            if status == "done":
                st.success("✓")
            elif status == "in_progress":
                st.info("◐")

    st.write("")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("ℹ️ Help", use_container_width=True):
            st.info("Explore a career you're curious about through 6 guided entries. Each one unlocks when you finish the last. Your honest take helps us build better.")
    with col2:
        if st.button("📓 My Notebook", use_container_width=True):
            st.session_state.page = "notebook"
            st.rerun()
    with col3:
        if st.button("✨ My Finds", use_container_width=True):
            st.session_state.page = "finds"
            st.rerun()
    with col4:
        if st.button("Sign Out", use_container_width=True):
            st.session_state.student = None
            st.session_state.page = "join"
            st.rerun()

def show_entry():
    """Entry detail: read intro, fill prompts, save/complete."""
    student = st.session_state.student
    entry_num = st.session_state.current_entry
    entry_template = ENTRIES[entry_num]

    st.markdown(f'<div class="big-title">Entry {entry_num}</div>', unsafe_allow_html=True)
    st.write(f"### {entry_template['title']}")
    st.caption(f"✨ {entry_template['subtitle']}")

    st.write(f"**What You'll Do:** {entry_template['activity']}")
    st.write("")
    st.write("**Answer these prompts. Be real.**")
    st.write("")

    # Load existing
    existing = get_entry_response(student.id, entry_num)
    existing_fields = existing.fields if existing else {}

    responses = {}
    for i, prompt in enumerate(entry_template['prompts']):
        value = existing_fields.get(prompt, "")

        # Special rendering for quest selection prompt (Entry 1)
        if entry_num == 1 and "Take one quest" in prompt:
            st.markdown(f"**{i+1}. {prompt}**")
            st.markdown("""
- **[Career Safari](https://discover.hopestreetgroup.org/student-quest/career-safari?launchId=506)** — explore a specific career up close.
- **[Find Your Fit](https://discover.hopestreetgroup.org/student-quest/interest-inventory?launchId=507)** — discover careers that match your vibe and what you're into.
- **[Building Next Steps](https://discover.hopestreetgroup.org/student-quest/academic-planning?launchId=505)** — map your academics and post-high-school plan.
            """)
            responses[prompt] = st.text_input("Which quest did you pick?", value=value, key=f"prompt_{i}")
        else:
            st.markdown(f"**{i+1}. {prompt}**")
            responses[prompt] = st.text_area("", value=value, height=80, key=f"prompt_{i}", label_visibility="collapsed")

    st.write("")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("← Go Back", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    with col2:
        if st.button("💾 Save", use_container_width=True):
            save_entry_response(student.id, entry_num, responses, "in_progress")
            st.success("Saved. You can come back later.")

    with col3:
        if st.button("✨ Done With This", use_container_width=True, type="primary"):
            filled = sum(1 for r in responses.values() if r.strip())
            required = max(1, len(responses) // 3)
            if filled >= required:
                save_entry_response(student.id, entry_num, responses, "done")
                st.success("Entry complete! 🎉")
                st.balloons()
                import time
                time.sleep(1.5)
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error(f"Please fill in at least {required} prompts ({filled}/{required} done)")

def show_notebook():
    """Notebook: all entries + before/after + PDF export."""
    student = st.session_state.student
    entries = get_student_entries(student.id)

    st.markdown(f'<div class="big-title">My Notebook</div>', unsafe_allow_html=True)
    st.write(f"**{student.display_name}**")

    # Journey recap
    st.write("---")
    st.write("## Your Growth Story")
    col1, col2 = st.columns(2)

    with col1:
        st.write("### 🚀 Entry 1: First Contact")
        e1 = entries[1]
        if e1:
            for prompt, answer in e1.fields.items():
                st.write(f"**{prompt}**")
                st.write(f"_{answer}_")
                st.write("")
        else:
            st.info("Not started yet")

    with col2:
        st.write("### ✨ Entry 6: Your Plan")
        e6 = entries[6]
        if e6:
            for prompt, answer in e6.fields.items():
                st.write(f"**{prompt}**")
                st.write(f"_{answer}_")
                st.write("")
        else:
            st.info("Keep going, you got this")

    # All entries
    st.write("---")
    st.write("## Full Journey")
    for entry_num in range(1, 7):
        entry = entries[entry_num]
        if entry:
            with st.expander(f"Entry {entry_num}: {ENTRIES[entry_num]['title']} • {entry.status}"):
                for prompt, answer in entry.fields.items():
                    st.write(f"**{prompt}**")
                    st.write(answer)
                    st.write("")

    # PDF export coming soon
    st.write("---")
    st.info("📥 PDF export coming soon!")

    if st.button("← Back", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

def show_finds():
    """My Finds: resources, links, inspiration board."""
    student = st.session_state.student
    resources = get_student_resources(student.id)

    st.markdown(f'<div class="big-title">My Finds ✨</div>', unsafe_allow_html=True)
    st.write("Collect links, articles, videos, and inspiration as you explore.")

    st.write("---")
    st.write("## Add a Find")
    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("What did you find?", placeholder="e.g., UX Designer at Google", key="find_title")
        url = st.text_input("Link", placeholder="https://...", key="find_url")

    with col2:
        resource_type = st.selectbox("Type", ["link", "article", "video", "image", "note"], key="find_type")
        notes = st.text_area("Notes", placeholder="Why you liked it, what stood out...", height=80, key="find_notes")

    if st.button("Add to My Finds", use_container_width=True, type="primary"):
        if title.strip() and (url.strip() or resource_type == "note"):
            add_resource(student.id, title.strip(), url.strip() or "", resource_type, notes.strip())
            st.success("Added! 🎉")
            st.rerun()
        else:
            st.error("Need a title and link (or notes if it's a note).")

    st.write("---")
    st.write("## Your Finds")

    if resources:
        for resource in resources:
            with st.expander(f"**{resource.title}** • {resource.resource_type}"):
                if resource.url:
                    st.write(f"🔗 [{resource.url}]({resource.url})")
                if resource.notes:
                    st.write(f"**Notes:** {resource.notes}")
                st.caption(f"Added: {resource.added_date.strftime('%b %d, %Y')}")

                if st.button("Remove", key=f"delete_{resource.id}"):
                    delete_resource(student.id, resource.id)
                    st.rerun()
    else:
        st.info("No finds yet. Start collecting as you explore!")

    st.write("")
    if st.button("← Back to Trail", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

# --- ROUTER ---

if st.session_state.student is None:
    show_join()
else:
    if st.session_state.page == "home":
        show_home()
    elif st.session_state.page == "entry":
        show_entry()
    elif st.session_state.page == "notebook":
        show_notebook()
    elif st.session_state.page == "finds":
        show_finds()
