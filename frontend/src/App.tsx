
import { useEffect, useState } from "react";
import axios from "axios";

interface Opcao {
  texto: string;
}

interface Questao {
  id: string;
  texto: string;
  opcoes: Opcao[];
  origem: string;
  imagem_url?: string;
}

function App() {
  const [questoes, setQuestoes] = useState<Questao[]>([]);
  const [selecionadas, setSelecionadas] = useState<string[]>([]);
  const [pdfUrl, setPdfUrl] = useState("");

  useEffect(() => {
    axios.get("http://localhost:8000/questoes/").then(res => setQuestoes(res.data));
  }, []);

  const gerarPDF = async () => {
    const res = await axios.post("http://localhost:8000/exportar-pdf/", selecionadas, {
      responseType: "blob"
    });
    const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
    setPdfUrl(url);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Lista de Questões</h1>
      <ul className="space-y-4">
        {questoes.map(q => (
          <li key={q.id} className="border p-4 rounded shadow">
            <input
              type="checkbox"
              onChange={e => {
                setSelecionadas(sel =>
                  e.target.checked ? [...sel, q.id] : sel.filter(id => id !== q.id)
                );
              }}
              className="mr-2"
            />
            <strong>{q.texto}</strong>
            <ul className="ml-6 mt-2 list-disc">
              {q.opcoes.map((o, i) => (
                <li key={i}>{String.fromCharCode(65 + i)}. {o.texto}</li>
              ))}
            </ul>
            {q.imagem_url && (
              <img src={q.imagem_url} alt="questao" className="mt-2 max-w-xs" />
            )}
          </li>
        ))}
      </ul>
      <button
        onClick={gerarPDF}
        className="mt-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Gerar PDF
      </button>
      {pdfUrl && (
        <div className="mt-4">
          <a href={pdfUrl} target="_blank" rel="noopener noreferrer" className="text-blue-500 underline">
            Baixar PDF
          </a>
        </div>
      )}
    </div>
  );
}

export default App;
