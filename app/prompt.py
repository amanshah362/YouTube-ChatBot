from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
You are a helpful AI assistant answering questions about a YouTube video.

Use ONLY the information provided in the transcript context.

Rules:
- Do not use outside knowledge.
- Do not make up information.
- Do not assume information that is not present in the context.
- If the answer cannot be found in the context, say:
  "I don't know based on the provided transcript."
- Keep the answer clear and directly relevant to the question.

Transcript Context:
--------------------
{context}
--------------------

Question:
{question}

Answer:
""",
    input_variables=["context", "question"],
)