module "iosxe" {
  source  = "netascode/nac-iosxe/iosxe"
  version = "1.0.0"

  yaml_directories = ["${path.module}/data"]
}
