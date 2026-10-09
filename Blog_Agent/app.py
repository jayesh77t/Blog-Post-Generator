import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Blog Generator", page_icon="✍️", layout="wide"
)

MODEL = os.getenv("MODEL")

try:
  llm = ChatGroq(model=MODEL)
except Exception as e:
  st.error(f"Error initializing ChatGroq with model '{MODEL}': {e}")
  st.stop()

HUMAN_STYLE = """Write like a person, not like an AI:
- Vary your sentence length. Some short. Others longer, with a clause that earns its place.
- Use contractions (it's, don't, you'll) and talk straight to the reader as "you".
- Replace vague claims with a concrete example, a number, or a small story.
- Having an opinion is fine. Saying "I" is fine.
- Never use these words and phrases: "in today's fast-paced world", "delve", "moreover",
  "furthermore", "unlock", "leverage", "robust", "seamless", "game-changer",
  "it's worth noting", "navigate the landscape", "at the end of the day".
- Do not start every section the same way.
- Only use a bullet list when the content really is a list. Prefer paragraphs.
- Do not end with a summary of what you just said. End with one useful thought."""

OUTLINE_PROMPT = ChatPromptTemplate.from_template(
    "Write a short outline for a blog post.\n\n"
    "Topic: {topic}\n"
    "Tone: {tone}\n\n"
    "Give me:\n"
    "- one opening line that makes the reader curious\n"
    "- 4 section headings\n"
    "- 5 key points the post must cover\n\n"
    "Just the outline. Do not write the post."
)

DRAFT_PROMPT = ChatPromptTemplate.from_template(
    "Write a blog post from this outline.\n\n"
    "{outline}\n\n"
    + HUMAN_STYLE
    + "\n\n"
    "Tone: {tone}\n"
    "Output markdown, with the section headings as ###.\n"
    "Make it as long or as short as the topic actually needs."
)

POLISH_PROMPT = ChatPromptTemplate.from_template(
    "Improve this blog post without changing what it says.\n\n"
    + HUMAN_STYLE
    + "\n\n"
    "Also:\n"
    "- add a good # title at the top\n"
    "- keep the markdown\n\n"
    "Reply with the improved post only, no commentary.\n\n"
    "{draft}"
)

outline_chain = OUTLINE_PROMPT | llm | StrOutputParser()
draft_chain = DRAFT_PROMPT | llm | StrOutputParser()
final_chain = POLISH_PROMPT | llm | StrOutputParser()

# --- Header Section ---
st.markdown("## ✍️ AI Blog Generator")
st.caption(
    "Outline $\rightarrow$ Draft $\rightarrow$ Polish pipeline powered by"
    " LangChain and Groq."
)
st.markdown("---")

# --- Sidebar Controls ---
with st.sidebar:
  st.header("⚙️ Configuration")
  topic = st.text_input(
      "Blog Topic / Title", "Why we have to learn the Gen-AI in 2026"
  )
  tone = st.selectbox("Tone", ["direct", "normal", "friendly"])

  st.markdown("---")
  generate_btn = st.button(
      "🚀 Generate Blog Post", type="primary", use_container_width=True
  )

  st.markdown("### Pipeline Flow")
  st.info(
      "1. **Outline:** Structures the core points & hooks.\n2. **Draft:** Writes"
      " the initial conversational draft.\n3. **Polish:** Applies final style"
      " refinements & adds title."
  )

# --- Execution & State Handling ---
if generate_btn:
  if not topic.strip():
    st.warning("Please provide a valid topic.")
  else:
    with st.status("Executing AI Pipeline...", expanded=True) as status:
      st.write("Step 1/3: Generating structured outline...")
      outline = outline_chain.invoke({"topic": topic, "tone": tone})

      st.write("Step 2/3: Drafting the blog content...")
      draft = draft_chain.invoke({"outline": outline, "tone": tone})

      st.write("Step 3/3: Polishing and formatting final output...")
      final = final_chain.invoke({"draft": draft})

      status.update(
          label="✨ Blog generation complete!", state="complete", expanded=False
      )

    # Save to session state so tabs persist values
    st.session_state["outline"] = outline
    st.session_state["draft"] = draft
    st.session_state["final"] = final

# --- Display Results in Tabs ---
if "final" in st.session_state:
  tab1, tab2, tab3, tab4 = st.tabs(
      ["📖 Final Preview", "📋 Outline", "📝 Raw Draft", "💻 Markdown Code"]
  )

  with tab1:
    st.markdown("### Preview")
    st.markdown(st.session_state["final"])
    st.download_button(
        label="📥 Download Markdown File",
        data=st.session_state["final"],
        file_name="blog_post.md",
        mime="text/markdown",
    )

  with tab2:
    st.markdown("### Generated Outline")
    st.markdown(st.session_state["outline"])

  with tab3:
    st.markdown("### Initial Draft")
    st.markdown(st.session_state["draft"])

  with tab4:
    st.markdown("### Raw Source Code")
    st.code(st.session_state["final"], language="markdown")

else:
  # Empty state UI placeholder
  st.markdown(
      """
        <div style="text-align: center; padding: 3rem; background-color: rgba(128, 128, 128, 0.05); border-radius: 12px; border: 1px dashed rgba(128, 128, 128, 0.2);">
            <h3>Ready to create your next blog?</h3>
            <p style="color: gray;">Configure your topic and tone in the sidebar, then click <b>Generate Blog Post</b>.</p>
        </div>
        """,
      unsafe_allow_html=True,
  )