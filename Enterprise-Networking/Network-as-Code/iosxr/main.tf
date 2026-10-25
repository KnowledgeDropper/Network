module "iosxr" {
  source  = "netascode/nac-iosxr/iosxr"
  version = "0.1.1"

  yaml_directories = ["${path.module}/data"]
}
