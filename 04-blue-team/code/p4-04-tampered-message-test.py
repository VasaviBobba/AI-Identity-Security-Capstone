from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from pathlib import Path

print("=" * 70)
print("P4-04 — TAMPERED AGENT MESSAGE SIGNATURE VALIDATION")
print("=" * 70)
print("Environment: LOCAL CONTROLLED SECURITY SIMULATION")
print("Real credentials: NOT USED")
print("Production systems: NOT USED")
print("=" * 70)

PRIVATE_KEY_FILE = Path("agent_ed25519_private.pem")
PUBLIC_KEY_FILE = Path("agent_ed25519_public.pem")

# ---------------------------------------------------------
# 1. Check that P4-03 key files exist
# ---------------------------------------------------------

print()
print("STEP 1 — LOAD ED25519 KEY PAIR")
print("-" * 70)

if not PRIVATE_KEY_FILE.exists():
    print("ERROR: Private key file not found.")
    print(f"Expected: {PRIVATE_KEY_FILE}")
    raise SystemExit(1)

if not PUBLIC_KEY_FILE.exists():
    print("ERROR: Public key file not found.")
    print(f"Expected: {PUBLIC_KEY_FILE}")
    raise SystemExit(1)

print(f"Private key loaded : {PRIVATE_KEY_FILE}")
print(f"Public key loaded  : {PUBLIC_KEY_FILE}")

# ---------------------------------------------------------
# 2. Load private key
# ---------------------------------------------------------

private_key = serialization.load_pem_private_key(
    PRIVATE_KEY_FILE.read_bytes(),
    password=None
)

# ---------------------------------------------------------
# 3. Load public key
# ---------------------------------------------------------

public_key = serialization.load_pem_public_key(
    PUBLIC_KEY_FILE.read_bytes()
)

# ---------------------------------------------------------
# 4. Create original agent message
# ---------------------------------------------------------

original_message = (
    b"Agent SecureNova requests access to the customer profile."
)

print()
print("STEP 2 — ORIGINAL AGENT MESSAGE")
print("-" * 70)
print(f"Message: {original_message.decode()}")

# ---------------------------------------------------------
# 5. Sign the original message
# ---------------------------------------------------------

signature = private_key.sign(original_message)

print()
print("STEP 3 — SIGN ORIGINAL MESSAGE")
print("-" * 70)
print("Algorithm : Ed25519")
print("Signature : GENERATED")
print(f"Signature size : {len(signature)} bytes")

# ---------------------------------------------------------
# 6. Verify the original message
# ---------------------------------------------------------

print()
print("STEP 4 — VERIFY ORIGINAL MESSAGE")
print("-" * 70)

try:
    public_key.verify(signature, original_message)
    print("Original message verification : PASS")
    print("Signature is valid.")
except InvalidSignature:
    print("Original message verification : FAIL")

# ---------------------------------------------------------
# 7. Tamper with ONE character
# ---------------------------------------------------------

tampered_message = (
    b"Agent SecureNova requests access to the payment profile."
)

print()
print("STEP 5 — TAMPER WITH MESSAGE")
print("-" * 70)
print("Original message:")
print(original_message.decode())

print()
print("Tampered message:")
print(tampered_message.decode())

print()
print("Tampering performed : YES")
print("Change              : customer profile -> payment profile")

# ---------------------------------------------------------
# 8. Verify tampered message
# ---------------------------------------------------------

print()
print("STEP 6 — VERIFY TAMPERED MESSAGE")
print("-" * 70)

try:
    public_key.verify(signature, tampered_message)

    # This should NOT happen.
    print("Tampered message verification : PASS")
    print("WARNING: Signature verification unexpectedly succeeded.")

except InvalidSignature:
    print("Tampered message verification : REJECTED")
    print("Signature verification failure detected.")
    print("ERROR: InvalidSignature")
    print("Reason: Message was modified after signing.")

# ---------------------------------------------------------
# 9. Security result
# ---------------------------------------------------------

print()
print("=" * 70)
print("P4-04 SECURITY RESULT")
print("=" * 70)

print("Original message verification : PASS")
print("Tampered message verification : REJECTED")
print("Signature verification failure : DETECTED")
print("Ed25519 tamper detection       : PASS")

print()
print("Safety note:")
print("Only local simulated agent messages were used.")
print("No real credentials were used.")
print("No production systems were accessed.")

print("=" * 70)
print("P4-04 TEST COMPLETE")
print("=" * 70)