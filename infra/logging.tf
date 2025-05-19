
resource "kubernetes_namespace" "logging" {
  metadata {
    name = "logging"
  }
}

resource "helm_release" "elasticsearch" {
  name       = "elasticsearch"
  namespace  = kubernetes_namespace.logging.metadata[0].name
  repository = "https://helm.elastic.co"
  chart      = "elasticsearch"
  version    = "7.17.3"

  set {
    name  = "replicas"
    value = "1"
  }

  set {
    name  = "minimumMasterNodes"
    value = "1"
  }
}

resource "helm_release" "kibana" {
  name       = "kibana"
  namespace  = kubernetes_namespace.logging.metadata[0].name
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "kibana"
  version    = "10.2.4"

  set {
    name  = "elasticsearch.hosts[0]"
    value = "elasticsearch.logging.svc.cluster.local"
  }
}

resource "helm_release" "fluentbit" {
  name       = "fluent-bit"
  namespace  = kubernetes_namespace.logging.metadata[0].name
  repository = "https://fluent.github.io/helm-charts"
  chart      = "fluent-bit"
  version    = "0.49.0"

  set {
    name  = "backend.type"
    value = "es"
  }

  set {
    name  = "backend.es.host"
    value = "elasticsearch.logging.svc.cluster.local"
  }

  set {
    name  = "backend.es.port"
    value = "9200"
  }

  set {
    name  = "backend.es.logstash_prefix"
    value = "k8s"
  }
}
