# etl_upload.py
 import os, glob, json, base64
 import pandasaspd
 fromsupabaseimport create_client
 fromopenaiimport OpenAI
 fromtiktoken import encoding_for_model
 supabase , 
python-docx , 
oai = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
 sp = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
 enc = encoding_for_model("text‑embedding‑3‑small")
 2
KB_PATH = "knowledge_base/**"
 for path in glob.glob(KB_PATH, recursive=True):
 if os.path.isdir(path):
 continue
 # 1. 抽取纯文本
if path.endswith('.docx'):
 fromdocximport Document
 txt = "\n".join([p.text for p in Document(path).paragraphs])
 elif path.endswith('.csv'):
 txt = pd.read_csv(path).to_csv(index=False)
 else:
 with open(path, 'r', errors='ignore') as f:
 txt = f.read()
 # 2. 拆分 800 token 块
tokens = enc.encode(txt)
 for i in range(0, len(tokens), 800):
 chunk_tokens = tokens[i:i+800]
 chunk_txt = enc.decode(chunk_tokens)
 # 3. 生成向量
emb = oai.embeddings.create(model="text‑embedding‑3‑small",
 input=chunk_txt).data[0].embedding
 # 4. 写入 Supabase
 sp.table('kb_chunks').insert({
 "chunk": chunk_txt,
 "embedding": emb,
 "metadata": {"file": os.path.basename(path)}
 }).execute()
