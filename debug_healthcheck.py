#!/usr/bin/env python3
"""
Debug script to understand the healthcheck format that's causing the error.
"""

import json

def debug_healthcheck_format(healthcheck_test):
    print(f"Input: {healthcheck_test}")
    print(f"Type: {type(healthcheck_test)}")
    
    if isinstance(healthcheck_test, str):
        print("Processing as string -> CMD-SHELL")
        result = json.dumps(["CMD-SHELL", healthcheck_test])
        print(f"Result: {result}")
    elif isinstance(healthcheck_test, list):
        print("Processing as list")
        healthcheck_test = healthcheck_test.copy()
        first_item = healthcheck_test[0] if healthcheck_test else ""
        print(f"First item: '{first_item}'")
        
        if first_item == "NONE":
            healthcheck_test.pop(0)
            print("Processing as NONE")
        elif first_item == "CMD":
            healthcheck_test.pop(0)
            print("Processing as CMD")
            result = json.dumps(healthcheck_test)
            print(f"Result: {result}")
        elif first_item == "CMD-SHELL":
            healthcheck_test.pop(0)
            print("Processing as CMD-SHELL")
            print(f"Remaining items: {healthcheck_test}")
            print(f"Length: {len(healthcheck_test)}")
            if len(healthcheck_test) != 1:
                print("ERROR: CMD_SHELL takes a single string after it")
                return
            result = json.dumps(healthcheck_test)
            print(f"Result: {result}")
        else:
            print("Processing as exec-form CMD (no prefix)")
            result = json.dumps(healthcheck_test)
            print(f"Result: {result}")
    else:
        print("ERROR: healthcheck.test must be either a string or a list")

# Test cases
print("=== Test Case 1: String ===")
debug_healthcheck_format("cmd arg1 arg2")

print("\n=== Test Case 2: CMD format ===")
debug_healthcheck_format(["CMD", "cmd", "arg1", "arg2"])

print("\n=== Test Case 3: CMD-SHELL format (valid) ===")
debug_healthcheck_format(["CMD-SHELL", "cmd arg1 arg2"])

print("\n=== Test Case 4: CMD-SHELL format (invalid - multiple args) ===")
debug_healthcheck_format(["CMD-SHELL", "cmd", "arg1", "arg2"])

print("\n=== Test Case 5: Exec-form without prefix ===")
debug_healthcheck_format(["/bin/readeck", "serve", "-config", "config.toml"])

print("\n=== Test Case 6: Readeck-like CMD-SHELL (invalid) ===")
debug_healthcheck_format(["CMD-SHELL", "/bin/readeck", "serve", "-config", "config.toml"])
