load '/opt/bats-support/load.bash'
load '/opt/bats-assert/load.bash'

@test "encrypt_with_gocd2 fails if variable_to_encrypt not set" {
  run /bin/bash -c "source src/secret-ops && encrypt_with_gocd2"
  assert_line --partial "variable_to_encrypt not set"
  # this is printed on test failure
  echo "output: $output"
  assert_equal "$status" 127
}

@test "encrypt_with_gocd2 fails if USER cannot read secret" {
  run /bin/bash -c "source src/secret-ops && USER=dummy encrypt_with_gocd2 mydata"
  # do not test for output, because it may be different on workstation and on
  # go-agent (due to different vault policies)
  assert_equal "$status" 1
}

@test "encrypt_with_gocd2 works if variable_to_encrypt set" {
  run /bin/bash -c "source src/secret-ops && encrypt_with_gocd2 mydata"
  refute_line --partial "variable_to_encrypt not set"
  assert_line --partial "AES:"
  assert_line --partial "Encrypting with gocd server: go.ai-traders.com"
  # this is printed on test failure
  echo "output: $output"
  assert_equal "$status" 0
}

@test "encrypt_with_gocd2 result can be saved to a variable" {
  run /bin/bash -c "source src/secret-ops && encrypt_with_gocd2 mydata 2>/dev/null"
  refute_line --partial "variable_to_encrypt not set"
  assert_line --partial "AES:"
  refute_line --partial "Encrypting with gocd server"
  # this is printed on test failure
  echo "output: $output"
  assert_equal "$status" 0
}

@test "encrypt_with_gocd_base fails if variable_to_encrypt not set" {
  run /bin/bash -c "source src/secret-ops && encrypt_with_gocd_base"
  assert_line --partial "variable_to_encrypt not set"
  # this is printed on test failure
  echo "output: $output"
  assert_equal "$status" 127
}

@test "encrypt_with_gocd_base works if variable_to_encrypt set" {
  run /bin/bash -c "source src/secret-ops && encrypt_with_gocd_base mydata"
  refute_line --partial "variable_to_encrypt not set"
  assert_line --partial "AES:"
  assert_line --partial "Encrypting with gocd server: go2.ai-traders.com"
  # this is printed on test failure
  echo "output: $output"
  assert_equal "$status" 0
}

@test "encrypt_with_gocd_base result can be saved to a variable" {
  run /bin/bash -c "source src/secret-ops && encrypt_with_gocd_base mydata 2>/dev/null"
  refute_line --partial "variable_to_encrypt not set"
  assert_line --partial "AES:"
  refute_line --partial "Encrypting with gocd server"
  # this is printed on test failure
  echo "output: $output"
  assert_equal "$status" 0
}
