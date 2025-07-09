provider "kubernetes" {
     config_path = "~/.kube/config"
   }

   resource "kubernetes_namespace" "ecommerce" {
     metadata {
       name = "ecommerce"
     }
   }