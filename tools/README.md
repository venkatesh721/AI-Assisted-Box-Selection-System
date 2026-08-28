# Conversation PDF generator

`generate_conversation_pdf.py` converts a UTF-8 Markdown/text file that **you manually create from your real conversation** into a paginated PDF. It does not download, extract, rewrite, or generate conversation content.

## Use

1. Create `conversation_input.md` in the repository root.
2. Paste the exact real conversation content into that file yourself.
3. Run:

```powershell
python tools/generate_conversation_pdf.py --input conversation_input.md --output chatgpt_conversation.pdf
```

The script rejects an empty input file and validates that the finished PDF has a PDF header, at least one page, and readable text.

`conversation_input.md` should not be committed unless the assignment explicitly asks for that source format. The output file is named `chatgpt_conversation.pdf` as requested. If the assignment specifically requires the filename `CHAT_TRANSCRIPT.pdf`, rename only the PDF produced from your genuine, manually copied/exported conversation.
