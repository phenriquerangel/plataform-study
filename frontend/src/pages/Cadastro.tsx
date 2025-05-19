import { useState } from "react";
import axios from "axios";

const API = import.meta.env.VITE_API_URL || "http://backend.backend.svc.cluster.local:8000/docs";

export default function Cadastro() {
  const [texto, setTexto] = useState("");
  const [origem, setOrigem] = useState("");
  const [opcoes, setOpcoes] = useState(["", "", "", ""]);
  const [correta, setCorreta] = useState(0);
  const [imagem, setImagem] = useState<File | null>(null);
  const [mensagem, setMensagem] = useState("");
  const [tipo, setTipo] = useState<"erro" | "sucesso" | "">("");

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setMensagem("");
    setTipo("");

    try {
      let imagem_url: string | null = null;

      if (imagem) {
        try {
          const formData = new FormData();
          formData.append("file", imagem);
          const uploadRes = await axios.post(`${API}/upload-imagem/`, formData);
          imagem_url = uploadRes.data.url;
          console.log("✅ Imagem enviada:", imagem_url);
        } catch (uploadErr: any) {
          console.error("❌ Erro ao enviar imagem:", uploadErr);
          if (uploadErr.response) {
            console.error("Status:", uploadErr.response.status);
            console.error("Dados:", uploadErr.response.data);
          }
          setMensagem("Erro ao enviar imagem. Verifique e tente novamente.");
          setTipo("erro");
          return;
        }
      }

      const payload = {
        texto,
        origem,
        resposta_correta: correta,
        imagem_url,
        opcoes: opcoes.map(texto => ({ texto }))
      };

      console.log("📦 Enviando questão para:", `${API}/questoes/`);
      console.log("📝 Payload:", payload);

      const res = await axios.post(`${API}/questoes/`, payload);
      console.log("✅ Questão cadastrada:", res.data);

      setMensagem("✅ Questão cadastrada com sucesso!");
      setTipo("sucesso");
      setTexto("");
      setOrigem("");
      setOpcoes(["", "", "", ""]);
      setCorreta(0);
      setImagem(null);
    } catch (err: any) {
      console.error("❌ Erro ao cadastrar questão:", err);
      setTipo("erro");

      if (err.response) {
        console.error("🔗 URL:", err.config?.url);
        console.error("📡 Status:", err.response.status);
        console.error("📨 Dados:", err.response.data);
        setMensagem("Erro na API: " + err.response.status);
      } else if (err.request) {
        console.error("🚫 Sem resposta da API:", err.request);
        setMensagem("Sem resposta da API. Verifique a conexão.");
      } else {
        console.error("⚠️ Erro desconhecido:", err.message);
        setMensagem("Erro inesperado. Veja o console.");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-6 space-y-4 max-w-xl mx-auto">
      <h1 className="text-xl font-bold">Nova Questão</h1>
      {mensagem && (
        <div className={`text-center font-semibold \${tipo === "erro" ? "text-red-600" : "text-green-700"}`}>
          {mensagem}
        </div>
      )}
      <textarea required value={texto} className="w-full border p-2" placeholder="Texto da questão" onChange={e => setTexto(e.target.value)} />
      <input required maxLength={7} value={origem} className="w-full border p-2" placeholder="Origem (ex: MAT2024)" onChange={e => setOrigem(e.target.value)} />
      {opcoes.map((o, i) => (
        <input key={i} value={o} className="w-full border p-2" placeholder={\`Opção \${String.fromCharCode(65 + i)}`} onChange={e => {
          const nova = [...opcoes];
          nova[i] = e.target.value;
          setOpcoes(nova);
        }} />
      ))}
      <select value={correta} onChange={e => setCorreta(parseInt(e.target.value))} className="w-full border p-2">
        {[0,1,2,3].map(i => <option key={i} value={i}>Alternativa correta: {String.fromCharCode(65 + i)}</option>)}
      </select>
      <input type="file" accept="image/*" onChange={e => setImagem(e.target.files?.[0] || null)} />
      <button className="bg-blue-600 text-white px-4 py-2 rounded" type="submit">Salvar</button>
    </form>
  );
}