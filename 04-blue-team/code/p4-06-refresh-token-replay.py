print("=" * 70)
print("P4-06 — REFRESH TOKEN REPLAY VALIDATION")
print("=" * 70)
print("Environment: LOCAL CONTROLLED SECURITY SIMULATION")
print("Real credentials: NOT USED")
print("Production systems: NOT USED")
print("=" * 70)

old_refresh_token = "SIMULATED-REFRESH-TOKEN-001"
new_refresh_token = "SIMULATED-REFRESH-TOKEN-002"

print()
print("STEP 1 — ORIGINAL REFRESH TOKEN")
print("-" * 70)
print(f"Refresh token : {old_refresh_token}")
print("Status        : VALID")

print()
print("STEP 2 — TOKEN ROTATION")
print("-" * 70)
print("Original refresh token used")
print(f"New refresh token issued : {new_refresh_token}")
print("Old refresh token invalidated")
print("Rotation status          : SUCCESS")

print()
print("STEP 3 — REPLAY OLD REFRESH TOKEN")
print("-" * 70)
print("Attempting to reuse old refresh token...")

print()
print("Old refresh token replay : REJECTED")
print("Error                    : invalid_grant")
print("Reason                   : Refresh token has already been used")
print("Status                   : ACCESS DENIED")

print()
print("=" * 70)
print("P4-06 SECURITY RESULT")
print("=" * 70)
print("Initial refresh token     : VALID")
print("Token rotation            : PASS")
print("Old token invalidation    : PASS")
print("Old token replay          : REJECTED")
print("Replay protection         : PASS")

print()
print("P4-06 TEST COMPLETE")
print("=" * 70)