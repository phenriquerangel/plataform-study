from fastapi import APIRouter, Body
from fastapi.responses import FileResponse
from kubernetes import client, config
import uuid
import os

router = APIRouter(prefix="/questoes", tags=["PDF"])

@router.post("/pdf")
def gerar_pdf(ids: dict = Body(...)):
    nome_job = f"pdf-job-{uuid.uuid4().hex[:8]}"
    config.load_incluster_config()
    batch = client.BatchV1Api()

    job = client.V1Job(
        metadata=client.V1ObjectMeta(name=nome_job),
        spec=client.V1JobSpec(
            ttl_seconds_after_finished=30,
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="pdf-worker",
                            image="phenriquernagel/pdf-worker:latest",
                            command=["python", "generate.py"],
                            args=[",".join(map(str, ids.get("ids", [])))],
                            volume_mounts=[
                                client.V1VolumeMount(
                                    mount_path="/pdfs",
                                    name="shared-pdf-volume"
                                )
                            ]
                        )
                    ],
                    restart_policy="Never",
                    volumes=[
                        client.V1Volume(
                            name="shared-pdf-volume",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="shared-pdf-pvc"
                            )
                        )
                    ]
                )
            )
        )
    )
    batch.create_namespaced_job(namespace="api-questoes", body=job)
    return {"status": "PDF solicitado, será gerado em breve."}

@router.get("/pdf/{id}")
def baixar_pdf(id: int):
    pdf_path = f"/pdfs/prova_{id}.pdf"
    if os.path.exists(pdf_path):
        return FileResponse(pdf_path, media_type='application/pdf', filename=f"prova_{id}.pdf")
    return {"erro": "Arquivo não encontrado"}
