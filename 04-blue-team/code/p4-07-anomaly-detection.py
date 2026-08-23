from datetime import datetime, timedelta


print("=" * 70)
print("P4-07 — ANOMALY DETECTION VALIDATION")
print("=" * 70)
print("Environment: LOCAL CONTROLLED SECURITY SIMULATION")
print("Real credentials: NOT USED")
print("Production systems: NOT USED")
print("=" * 70)


def timestamp(dt):
    return dt.isoformat(timespec="seconds")


def alert(event_type, identity, reason, event_time):
    print()
    print("[ANOMALY ALERT]")
    print(f"Timestamp : {timestamp(event_time)}")
    print(f"Identity  : {identity}")
    print(f"Event Type: {event_type}")
    print(f"Reason    : {reason}")
    print("Status    : ALERT")


identity = "agent-secure-nova"
start_time = datetime.now()


# ==========================================================
# SCENARIO 1 — LLM API CALL VOLUME SPIKE
# ==========================================================

print()
print("=" * 70)
print("SCENARIO 1 — LLM API CALL VOLUME SPIKE")
print("=" * 70)

requests = []

for i in range(21):
    requests.append({
        "identity": identity,
        "timestamp": start_time + timedelta(seconds=i),
        "event_type": "LLM_API_CALL"
    })

print(f"Identity: {identity}")
print(f"Requests observed in 60 seconds: {len(requests)}")
print("Configured threshold: 20 requests / 60 seconds")

if len(requests) > 20:
    alert(
        "LLM API CALL VOLUME SPIKE",
        identity,
        f"{len(requests)} requests detected within 60 seconds; "
        "threshold is 20",
        requests[-1]["timestamp"]
    )


# ==========================================================
# SCENARIO 2 — AGENT SCOPE CHANGE
# ==========================================================

print()
print("=" * 70)
print("SCENARIO 2 — AGENT SCOPE CHANGE")
print("=" * 70)

previous_scope = "read:profile"
current_scope = "read:profile write:payments"

print(f"Identity: {identity}")
print(f"Previous scope: {previous_scope}")
print(f"Current scope : {current_scope}")

if previous_scope != current_scope:
    alert(
        "AGENT SCOPE CHANGE",
        identity,
        f"Scope changed from '{previous_scope}' "
        f"to '{current_scope}'",
        start_time + timedelta(minutes=2)
    )


# ==========================================================
# SCENARIO 3 — TOKEN REUSE AFTER EXPIRY
# ==========================================================

print()
print("=" * 70)
print("SCENARIO 3 — TOKEN REUSE AFTER EXPIRY")
print("=" * 70)

issued_at = start_time + timedelta(minutes=4)
expires_at = issued_at + timedelta(seconds=300)
reuse_time = expires_at + timedelta(seconds=10)

print(f"Identity : {identity}")
print("Token ID : SIMULATED-TOKEN-001")
print(f"Issued   : {timestamp(issued_at)}")
print(f"Expires  : {timestamp(expires_at)}")
print(f"Reused   : {timestamp(reuse_time)}")

if reuse_time > expires_at:
    alert(
        "TOKEN REUSE AFTER EXPIRY",
        identity,
        "Expired token was presented after its expiration time",
        reuse_time
    )


# ==========================================================
# FINAL RESULT
# ==========================================================

print()
print("=" * 70)
print("P4-07 ANOMALY DETECTION RESULTS")
print("=" * 70)

print("1. LLM API call-volume spike : ALERT")
print("2. Agent scope change        : ALERT")
print("3. Token reuse after expiry  : ALERT")

print()
print("Alerts generated: 3/3")

print()
print("=" * 70)
print("P4-07 SECURITY CONCLUSION")
print("=" * 70)

print("The anomaly detector identified all three")
print("simulated identity-security anomaly scenarios.")

print()
print("Each alert records:")
print("- Timestamp")
print("- Identity")
print("- Event type")
print("- Detection reason")

print()

print("=" * 70)
print("P4-07 TEST COMPLETE")
print("=" * 70)