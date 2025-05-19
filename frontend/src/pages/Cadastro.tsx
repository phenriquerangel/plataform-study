import { useState } from "react";
import axios from "axios";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function Cadastro() {
  const [texto, setTexto] = useState("");
  const [origem, setOrigem] = useState("");
  const [opcoes, setOpcoes] = useState(["", "", "", ""]);
  const [correta, setCorreta] = useState(0);
  const [imagem, setImagem] = useState<File | null>(null);
  const [mensagem, setMensagem] = useState("");

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setMensagem("");

    try {
      let imagem_url: string | null = null;

      // Só faz upload se tiver imagem
      if (imagem) {
        const formData = new FormData();
        formData.append("file", imagem);
        const res = await axios.post(`${API}/upload-imagem/`, formData);
        imagem_url = res.data.url;
      }

      const payload = {
        texto,
        origem,
        resposta_correta: correta,
        imagem_url,
        opcoes: opcoes.map(texto => ({ texto }))
      };

      console.log("Enviando payload:", payload);

      await axios.post(`${API}/questoes/`, payload);

      setMensagem("✅ Questão cadastrada com sucesso!");
      setTexto("");
      setOrigem("");
      setOpcoes(["", "", "", ""]);
      setCorreta(0);
      setImagem(null);
    } catch (err) {
      console.error("Erro ao cadastrar:", err);
      setMensagem("❌ Erro ao cadastrar questão. Verifique os campos.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-6 space-y-4 max-w-xl mx-auto">
      <h1 className="text-xl font-bold">Nova Questão</h1>
      {mensagem && <div className="text-center font-semibold text-blue-600">{mensagem}</div>}
      <textarea required value={texto} className="w-full border p-2" placeholder="Texto da questão" onChange={e => setTexto(e.target.value)} />
      <input required maxLength={7} value={origem} className="w-full border p-2" placeholder="Origem (ex: MAT2024)" onChange={e => setOrigem(e.target.value)} />
      {opcoes.map((o, i) => (
        <input key={i} value={o} className="w-full border p-2" placeholder={`Opção ${String.fromCharCode(65 + i)}`} onChange={e => {
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