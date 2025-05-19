resource "kubernetes_namespace" "minio" {
  metadata {
    name = "minio"
  }
}

resource "helm_release" "minio" {
  name       = "minio"
  namespace  = "minio"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "minio"
  version    = "12.9.3"

  set {
    name  = "mode"
    value = "standalone"
  }

  set {
    name  = "auth.rootUser"
    value = "minioadmin"
  }

  set {
    name  = "auth.rootPassword"
    value = "minioadmin"
  }

  set {
    name  = "persistence.enabled"
    value = "true"
  }

  set {
    name  = "persistence.size"
    value = "10Gi"
  }

  set {
    name  = "persistence.storageClass"
    value = "hostpath"
  }

  set {
    name  = "service.type"
    value = "ClusterIP"
  }
}
