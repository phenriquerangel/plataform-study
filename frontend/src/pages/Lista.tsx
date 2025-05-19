import { useEffect, useState } from "react";
import axios from "axios";

const API = import.meta.env.VITE_API_URL || "http://backend.backend.svc.cluster.local:8000/docs";

interface Opcao {
  texto: string;
}
interface Questao {
  id: string;
  texto: string;
  origem: string;
  imagem_url?: string;
  opcoes: Opcao[];
  resposta_correta: number;
}

export default function Lista() {
  const [questoes, setQuestoes] = useState<Questao[]>([]);
  const [selecionadas, setSelecionadas] = useState<string[]>([]);
  const [pdfUrl, setPdfUrl] = useState("");

  const carregar = () =>
    axios.get(`${API}/questoes/`).then(res => setQuestoes(res.data));

  useEffect(() => {
    carregar();
  }, []);

  const excluir = async (id: string) => {
    await axios.delete(`${API}/questoes/${id}`);
    carregar();
  };

  const gerarPDF = async () => {
    const res = await axios.post(`${API}/exportar-pdf/`, selecionadas, {
      responseType: "blob"
    });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    setPdfUrl(url);
  };

  return (
    <div className="p-6 space-y-4 max-w-3xl mx-auto">
      <h1 className="text-xl font-bold">Questões Cadastradas</h1>
      {questoes.map(q => (
        <div key={q.id} className="border p-4 rounded space-y-2">
          <div className="flex justify-between">
            <div>
              <input type="checkbox" className="mr-2"
                onChange={e =>
                  setSelecionadas(s =>
                    e.target.checked ? [...s, q.id] : s.filter(i => i !== q.id)
                  )
                }
              />
              <strong>{q.texto}</strong> ({q.origem})
            </div>
            <button onClick={() => excluir(q.id)} className="text-red-600">Excluir</button>
          </div>
          <ul className="list-disc ml-6">
            {q.opcoes.map((o, i) => (
              <li key={i} className={i === q.resposta_correta ? "font-bold" : ""}>
                {String.fromCharCode(65 + i)}. {o.texto}
              </li>
            ))}
          </ul>
          {q.imagem_url && (
            <img src={q.imagem_url} alt="imagem" className="max-w-xs rounded" />
          )}
        </div>
      ))}
      <button onClick={gerarPDF} className="bg-green-600 text-white px-4 py-2 rounded">
        Gerar PDF das Selecionadas
      </button>
      {pdfUrl && (
        <div className="mt-2">
          <a href={pdfUrl} target="_blank" rel="noopener noreferrer" className="text-blue-500 underline">
            Baixar PDF
          </a>
        </div>
      )}
    </div>
  );
}