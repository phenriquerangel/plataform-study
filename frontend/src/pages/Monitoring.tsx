import { useEffect, useState } from "react";
import axios from "axios";

const API = import.meta.env.VITE_API_URL || "http://backend.backend.svc.cluster.local:8000";

export default function Monitoring() {
  const [status, setStatus] = useState<"ok" | "erro" | "loading">("loading");
  const [mensagem, setMensagem] = useState("");
  const [dbOk, setDbOk] = useState(false);
  const [minioOk, setMinioOk] = useState(false);

  useEffect(() => {
    const verificar = async () => {
      setStatus("loading");
      try {
        const res = await axios.get(`${API}/monitorar`);
        setMensagem("Conexão com API OK");
        setDbOk(res.data.db === true);
        setMinioOk(res.data.minio === true);
        setStatus("ok");
      } catch (err: any) {
        console.error(err);
        setMensagem("❌ Falha ao conectar com a API.");
        setStatus("erro");
      }
    };

    verificar();
  }, []);

  return (
    <div className="p-6 max-w-xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Monitoramento</h1>
      <p className={status === "ok" ? "text-green-700" : "text-red-600"}>
        {mensagem}
      </p>
      {status === "ok" && (
        <div className="space-y-2">
          <p>
            🗄️ Banco de Dados:{" "}
            <span className={dbOk ? "text-green-600" : "text-red-600"}>
              {dbOk ? "Conectado" : "Erro de conexão"}
            </span>
          </p>
          <p>
            🗂️ MinIO:{" "}
            <span className={minioOk ? "text-green-600" : "text-red-600"}>
              {minioOk ? "Conectado" : "Erro de conexão"}
            </span>
          </p>
        </div>
      )}
    </div>
  );
}