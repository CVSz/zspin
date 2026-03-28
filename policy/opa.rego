package zspin.policy

deny[msg] {
  input.action == "scale"
  input.service == "api"
  input.error_rate > 0.5
  msg := "Scaling denied: high error rate"
}

allow {
  not deny[_]
}
