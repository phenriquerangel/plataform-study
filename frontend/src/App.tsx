import { useState } from "react";
import Lista from "./pages/Lista";
import Cadastro from "./pages/Cadastro";

function App() {
  const [tela, setTela] = useState<"lista" | "cadastro">("lista");

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <nav className="bg-white shadow mb-6">
        <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between">
          <h1 className="text-xl font-bold">Sistema de Questões</h1>
          <div className="space-x-4">
            <button
              onClick={() => setTela("lista")}
              className={`px-4 py-2 rounded ${tela === "lista" ? "bg-blue-600 text-white" : "bg-gray-200"}`}
            >
              Listar
            </button>
            <button
              onClick={() => setTela("cadastro")}
              className={`px-4 py-2 rounded ${tela === "cadastro" ? "bg-blue-600 text-white" : "bg-gray-200"}`}
            >
              Cadastrar
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto px-4">
        {tela === "lista" && <Lista />}
        {tela === "cadastro" && <Cadastro />}
      </main>
    </div>
  );
}

export default App;