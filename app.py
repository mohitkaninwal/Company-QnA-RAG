import streamlit as st
from src.utils.pinecone_utils import initialize_pinecone,initialize_vectorstore
from src.utils.llm_utils import initialize_llm,format_polite_response


def main():
    st.set_page_config(page_title="Nickelfox Knowledge Assistant", page_icon="🦊", layout="wide")
    st.title("🦊 Nickelfox Knowledge Assistant")
    st.markdown("*Your friendly AI assistant for company policies, procedures, and documentation*")

    # Initialize backend
    pc = initialize_pinecone()
    if not pc: st.stop()
    vectorstore = initialize_vectorstore(pc)
    if not vectorstore: st.stop()
    llm = initialize_llm()
    if not llm: st.stop()

    # Chat state/history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initial welcome message
    if not st.session_state.messages:
        welcome_message = (
            "👋 Hello! I'm here to help you with any questions about company policies, procedures, or documentation. "
            "How can I assist you today?"
        )
        st.session_state.messages.append({"role": "assistant", "content": welcome_message})

    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input only (no upload)
    if prompt := st.chat_input("Ask me anything about company policies, procedures, or documentation..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Searching company documents..."):
                try:
                    docs = vectorstore.similarity_search(prompt, k=5)
                    if not docs:
                        response = (
                            "I couldn't find any relevant information in our knowledge base for your question. "
                            "This might be because the information hasn't been added yet, or your question might need rephrasing.\n\n"
                            "I'd be happy to help if you try rephrasing your question or asking about another topic!"
                        )
                    else:
                        context = "\n\n".join([doc.page_content for doc in docs])
                        response = format_polite_response(context, prompt, llm)
                    st.markdown(response)

                    # Optional: View sources
                    if docs:
                        with st.expander("📚 View Source Documents"):
                            for i, doc in enumerate(docs, 1):
                                content = doc.page_content
                                st.write(f"**Source {i}:**")
                                st.write(content[:400] + "..." if len(content) > 400 else content)
                                if hasattr(doc, "metadata") and doc.metadata:
                                    st.write(f"*Document Info: {doc.metadata}*")
                                st.write("---")
                except Exception as e:
                    st.error(
                        "Sorry, I'm having technical issues at the moment. Please try again soon."
                        f"\n\nDetails: {e}"
                    )
                    response = "Sorry, I'm having technical issues at the moment. Please try again soon."
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Sidebar: help/tips and clear
    with st.sidebar:
        st.header("ℹ️ About This Assistant")
        st.info(
            "This AI assistant has access to your Nickelfox's knowledge base, including employee handbook, policies, SOPs, and HR guidelines. "
            "Simply ask your questions in natural language!"
        )
        st.header("💡 Tips for Better Results")
        st.markdown(
            "- Be specific in your questions\n"
            "- Use keywords related to your topic\n"
            "- Ask follow-up questions for clarification\n"
            "- Feel free to rephrase if needed"
        )
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        st.markdown("---\n*Built with ❤️ for NICKELFOX team*")

if __name__ == "__main__":
    main()
 