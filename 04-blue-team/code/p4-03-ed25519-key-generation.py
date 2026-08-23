from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from pathlib import Path

print("=" * 70)
print("P4-03 — ED25519 AGENT IDENTITY KEY GENERATION")
print("=" * 70)
print("Environment: LOCAL CONTROLLED SECURITY SIMULATION")
print("Real credentials: NOT USED")
print("Production systems: NOT USED")
print("=" * 70)

# ---------------------------------------------------------
# 1. Generate Ed25519 private key
# ---------------------------------------------------------

private_key = ed25519.Ed25519PrivateKey.generate()

# ---------------------------------------------------------
# 2. Derive public key
# ---------------------------------------------------------

public_key = private_key.public_key()

# ---------------------------------------------------------
# 3. Serialize private key
# ---------------------------------------------------------

private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# ---------------------------------------------------------
# 4. Serialize public key
# ---------------------------------------------------------

public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# ---------------------------------------------------------
# 5. Save both key files
# ---------------------------------------------------------

private_file = Path("agent_ed25519_private.pem")
public_file = Path("agent_ed25519_public.pem")

private_file.write_bytes(private_bytes)
public_file.write_bytes(public_bytes)

# ---------------------------------------------------------
# 6. Validate that both files exist
# ---------------------------------------------------------

print()
print("KEY GENERATION RESULT")
print("-" * 70)

print("Algorithm          : Ed25519")
print("Private key        : GENERATED")
print("Public key         : GENERATED")

print()
print("FILES CREATED")
print("-" * 70)

print(f"Private key file   : {private_file}")
print(f"Public key file    : {public_file}")

print()
print("File verification")
print(f"Private key exists : {private_file.exists()}")
print(f"Public key exists  : {public_file.exists()}")

# ---------------------------------------------------------
# 7. Display file sizes
# ---------------------------------------------------------

print()
print("FILE DETAILS")
print("-" * 70)

print(f"Private key size   : {private_file.stat().st_size} bytes")
print(f"Public key size    : {public_file.stat().st_size} bytes")

# ---------------------------------------------------------
# 8. Security note
# ---------------------------------------------------------

print()
print("=" * 70)
print("P4-03 SECURITY RESULT")
print("=" * 70)

if private_file.exists() and public_file.exists():
    print("Ed25519 key pair generation : PASS")
    print("Private key file             : CREATED")
    print("Public key file              : CREATED")
    print("Cryptography library         : Python cryptography")
else:
    print("Ed25519 key pair generation : FAIL")

print()
print("Safety note:")
print("Keys are local simulation keys only.")
print("No real credentials were used.")
print("No production systems were accessed.")
print("=" * 70)
print("P4-03 TEST COMPLETE")
print("=" * 70)